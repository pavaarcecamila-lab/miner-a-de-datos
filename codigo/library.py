import pandas as pd
from pathlib import Path
import unicodedata
# ============================================================
# FUNCIONES GENERALES
# ============================================================

def sin_tildes(texto):
    if pd.isna(texto):
        return texto

    texto = str(texto)

    return "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )


def normalizar_texto(texto):
    if pd.isna(texto):
        return texto

    texto = sin_tildes(texto)
    texto = texto.strip().upper()

    return texto


def normalizar_nombre_vehiculo(texto):
    if pd.isna(texto):
        return texto

    texto = normalizar_texto(texto)

    texto = texto.replace("_", " ")
    texto = texto.replace("-", " ")

    while "  " in texto:
        texto = texto.replace("  ", " ")

    return texto


# ============================================================
# EXTRACCIÓN
# ============================================================

class ExtractorDatos:

    def __init__(self, ruta):
        self.ruta = Path(ruta)

    def cargar_csv(self):
        return pd.read_csv(self.ruta)


# ============================================================
# DIAGNÓSTICO
# ============================================================

class DiagnosticoDatos:

    def __init__(self, df):
        self.df = df

    def dimensiones(self):
        return self.df.shape

    def primeras_filas(self):
        return self.df.head()

    def tipos_datos(self):
        return self.df.dtypes

    def valores_nulos(self):
        return self.df.isna().sum()

    def duplicados(self):
        return int(self.df.duplicated().sum())

    def valores_unicos(self, columna):
        return self.df[columna].value_counts()

    def cantidad_valores_unicos(self, columna):
        return int(self.df[columna].nunique())

    def rango_columna(self, columna):
        return {
            "minimo": self.df[columna].min(),
            "maximo": self.df[columna].max()
        }

    def registros_por_valor(self, columna, valor):
        return int((self.df[columna] == valor).sum())

    def frecuencia_columna(self, columna):
        return self.df[columna].value_counts().sort_index()

    def resumen(self):
        return {
            "filas": self.df.shape[0],
            "columnas": self.df.shape[1],
            "duplicados": int(self.df.duplicated().sum()),
            "nulos_totales": int(self.df.isna().sum().sum())
        }


# ============================================================
# BITÁCORA
# ============================================================

class BitacoraLimpieza:

    def __init__(self):
        self.registros = []

    def registrar(
        self,
        conjunto,
        paso,
        descripcion,
        registros_iniciales,
        registros_finales,
        descartados
    ):

        self.registros.append({
            "CONJUNTO": conjunto,
            "PASO": paso,
            "DESCRIPCION": descripcion,
            "REGISTROS_INICIALES": registros_iniciales,
            "REGISTROS_FINALES": registros_finales,
            "REGISTROS_DESCARTADOS": descartados
        })

    def obtener_dataframe(self):
        return pd.DataFrame(self.registros)


# ============================================================
# LIMPIADOR GENERAL
# ============================================================

class LimpiadorDatos:

    def __init__(self, df):
        self.df = df.copy()

    def eliminar_duplicados_exactos(self):

        cantidad_inicial = len(self.df)

        self.df = self.df.drop_duplicates().copy()

        cantidad_final = len(self.df)

        return cantidad_inicial - cantidad_final

    def normalizar_columnas_texto(self, columnas):

        for columna in columnas:

            if columna in self.df.columns:

                self.df[columna] = self.df[columna].apply(
                    normalizar_texto
                )

        return self.df

    def eliminar_columnas(self, columnas):

        columnas_existentes = [
            columna
            for columna in columnas
            if columna in self.df.columns
        ]

        self.df = self.df.drop(
            columns=columnas_existentes
        )

        return self.df

    def obtener_resultado(self):
        return self.df.copy()


# ============================================================
# LIMPIADOR RUNT
# ============================================================

class LimpiadorRUNT(LimpiadorDatos):

    def eliminar_duplicados(self):

        self.df = self.df.drop_duplicates().copy()

        return self.df

    def normalizar(self):

        columnas = [
            "NOMBRE_DEPARTAMENTO",
            "NOMBRE_MUNICIPIO",
            "NOMBRE_SERVICIO",
            "ESTADO_DEL_VEHICULO",
            "NOMBRE_DE_LA_CLASE"
        ]

        self.normalizar_columnas_texto(columnas)

        return self.df

    def filtrar_activos(self):

        self.df = self.df[
            self.df["ESTADO_DEL_VEHICULO"] == "ACTIVO"
        ].copy()

        return self.df

    def limpiar_fecha_registro(self):

        self.df["FECHA DE REGISTRO"] = pd.to_numeric(
            self.df["FECHA DE REGISTRO"],
            errors="coerce"
        )

        return self.df

    def limpiar_cantidad(self):

        self.df["CANTIDAD"] = pd.to_numeric(
            self.df["CANTIDAD"],
            errors="coerce"
        )

        self.df = self.df[
            self.df["CANTIDAD"].notna()
            & (self.df["CANTIDAD"] > 0)
        ].copy()

        return self.df

    def eliminar_informacion_publicacion(self):

        columnas = [
            "MES DE PUBLICACION",
            "AÑO DE PUBLICACIÓN"
        ]

        return self.eliminar_columnas(columnas)

    def obtener_resultado(self):

        return self.df.copy()


# ============================================================
# LIMPIADOR HURTO
# ============================================================

class LimpiadorHurto(LimpiadorDatos):

    def eliminar_duplicados(self):

        self.df = self.df.drop_duplicates().copy()

        return self.df

    def normalizar(self):

        columnas = [
            "DEPARTAMENTO",
            "MUNICIPIO",
            "TIPO DELITO",
            "ZONA"
        ]

        self.normalizar_columnas_texto(columnas)

        return self.df

    def limpiar_fecha(self):

        self.df["FECHA HECHO"] = pd.to_datetime(
            self.df["FECHA HECHO"],
            errors="coerce",
            dayfirst=True
        )

        return self.df

    def limpiar_cantidad(self):

        self.df["CANTIDAD"] = pd.to_numeric(
            self.df["CANTIDAD"],
            errors="coerce"
        )

        self.df = self.df[
            self.df["CANTIDAD"].notna()
            & (self.df["CANTIDAD"] > 0)
        ].copy()

        return self.df

    def obtener_resultado(self):

        return self.df.copy()


# ============================================================
# LIMPIADOR RECUPERACIÓN
# ============================================================

class LimpiadorRecuperacion(LimpiadorDatos):

    def eliminar_duplicados(self):

        self.df = self.df.drop_duplicates().copy()

        return self.df

    def normalizar(self):

        columnas = [
            "DEPARTAMENTO",
            "MUNICIPIO",
            "CLASE BIEN"
        ]

        self.normalizar_columnas_texto(columnas)

        self.df["CLASE BIEN"] = self.df[
            "CLASE BIEN"
        ].apply(normalizar_nombre_vehiculo)

        return self.df

    def limpiar_fecha(self):
        self.df["FECHA HECHO"] = pd.to_datetime(
            self.df["FECHA HECHO"],
            errors="coerce",
            format="mixed",
            dayfirst=True
        )
        return self.df

    def limpiar_codigo_dane(self):

        self.df["CODIGO DANE"] = (
            self.df["CODIGO DANE"]
            .astype(str)
            .str.strip()
            .str.zfill(5)
        )

        self.df["CODIGO DANE"] = self.df[
            "CODIGO DANE"
        ].apply(
            lambda codigo:
            codigo[:5]
            if len(codigo) >= 6
            else codigo
        )

    def limpiar_cantidad(self):

        self.df["CANTIDAD"] = pd.to_numeric(
            self.df["CANTIDAD"],
            errors="coerce"
        )

        self.df = self.df[
            self.df["CANTIDAD"].notna()
            & (self.df["CANTIDAD"] > 0)
        ].copy()

        return self.df

    def obtener_resultado(self):

        return self.df.copy()


# ============================================================
# CLASIFICACIÓN DE VEHÍCULOS
# ============================================================

class ClasificadorVehiculos:

    CLASES_AUTOMOTOR = {
        "AUTOMOVIL",
        "BUS",
        "BUSETA",
        "CAMION",
        "CAMIONETA",
        "CAMPERO",
        "MICROBUS",
        "TAXI",
        "TRACTO CAMION",
        "TRACTOMULA",
        "VEHICULO PANEL",
        "VOLQUETA"
    }

    def clasificar_recuperacion(self, clase):

        if pd.isna(clase):
            return None

        clase = normalizar_nombre_vehiculo(clase)

        if clase == "MOTOCICLETA":
            return "MOTOCICLETA"

        if clase in self.CLASES_AUTOMOTOR:
            return "AUTOMOTOR"

        return None

    def clasificar_hurto(self, tipo_delito):

        if pd.isna(tipo_delito):
            return None

        tipo_delito = normalizar_texto(tipo_delito)

        if "HURTO MOTOCICLETAS" in tipo_delito:
            return "MOTOCICLETA"

        if "HURTO AUTOMOTORES" in tipo_delito:
            return "AUTOMOTOR"

        return None

    def clasificar_runt(self, clase):

        if pd.isna(clase):
            return None

        clase = normalizar_nombre_vehiculo(clase)

        if clase == "MOTOCICLETA":
            return "MOTOCICLETA"

        if clase in self.CLASES_AUTOMOTOR:
            return "AUTOMOTOR"

        return None


# ============================================================
# DIAGNÓSTICO DE VALORES ATÍPICOS
# ============================================================

class AnalizadorAtipicos:

    def __init__(self, df):
        self.df = df

    def calcular_iqr(self, columna):

        serie = pd.to_numeric(
            self.df[columna],
            errors="coerce"
        ).dropna()

        if serie.empty:
            return {}

        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)

        iqr = q3 - q1

        limite_inferior = q1 - (1.5 * iqr)
        limite_superior = q3 + (1.5 * iqr)

        cantidad = int(
            (
                (serie < limite_inferior)
                | (serie > limite_superior)
            ).sum()
        )

        return {
            "Q1": q1,
            "Q3": q3,
            "IQR": iqr,
            "LIMITE_INFERIOR": limite_inferior,
            "LIMITE_SUPERIOR": limite_superior,
            "VALORES_ATIPICOS": cantidad
        }


# ============================================================
# AGREGACIÓN
# ============================================================

class AgregadorDatos:

    def agregar(self, df, columnas_clave, columna_cantidad):

        resultado = (
            df.groupby(
                columnas_clave,
                as_index=False
            )[columna_cantidad]
            .sum()
        )

        return resultado


# ============================================================
# INTEGRACIÓN
# ============================================================

class IntegradorDatos:

    def cruzar(self, registrados, hurtados, recuperados):

        claves = [
            "AÑO",
            "CODIGO_DANE_MUNICIPIO",
            "TIPO_VEHICULO"
        ]

        resultado = pd.merge(
            registrados,
            hurtados,
            on=claves,
            how="outer",
            indicator=False
        )

        resultado = pd.merge(
            resultado,
            recuperados,
            on=claves,
            how="outer",
            indicator=False
        )

        return resultado

    def completar_ceros(self, df, columnas):

        for columna in columnas:

            if columna in df.columns:

                df[columna] = df[columna].fillna(0)

        return df


# ============================================================
# VALIDACIÓN
# ============================================================

class ValidadorDatos:

    def __init__(self, df):
        self.df = df

    def validar_nulos(self):

        return self.df.isna().sum()

    def validar_duplicados(self):

        return int(self.df.duplicated().sum())

    def validar_claves(self, columnas):

        return int(
            self.df.duplicated(
                subset=columnas
            ).sum()
        )

    def validar_anio(self):

        if "AÑO" not in self.df.columns:
            return {}

        anios = pd.to_numeric(
            self.df["AÑO"],
            errors="coerce"
        )

        return {
            "NULOS": int(anios.isna().sum()),
            "MINIMO": anios.min(),
            "MAXIMO": anios.max()
        }

    def validar_dane(self):

        if "CODIGO_DANE_MUNICIPIO" not in self.df.columns:
            return {}

        codigo = (
            self.df["CODIGO_DANE_MUNICIPIO"]
            .astype(str)
            .str.strip()
        )

        return {
            "NULOS": int(
                self.df[
                    "CODIGO_DANE_MUNICIPIO"
                ].isna().sum()
            ),
            "LONGITUDES_INVALIDAS": int(
                (~codigo.str.fullmatch(r"\d{5}")).sum()
            )
        }

    def validar_tipos_vehiculo(self):

        permitidos = {
            "MOTOCICLETA",
            "AUTOMOTOR"
        }

        if "TIPO_VEHICULO" not in self.df.columns:
            return {}

        valores = set(
            self.df["TIPO_VEHICULO"]
            .dropna()
            .unique()
        )

        return {
            "VALORES_ENCONTRADOS": valores,
            "VALORES_NO_PERMITIDOS": valores - permitidos
        }

    def validar_cantidades(self):

        columnas = [
            "VEHICULOS_REGISTRADOS",
            "VEHICULOS_HURTADOS",
            "VEHICULOS_RECUPERADOS"
        ]

        resultado = {}

        for columna in columnas:

            if columna in self.df.columns:

                serie = pd.to_numeric(
                    self.df[columna],
                    errors="coerce"
                )

                resultado[columna] = {
                    "NULOS": int(serie.isna().sum()),
                    "MINIMO": serie.min(),
                    "MAXIMO": serie.max()
                }

        return resultado

    def validar_limpieza(self, nombre, df):

        resultado = {
            "DATASET": nombre,
            "FILAS": len(df),
            "COLUMNAS": len(df.columns),
            "DUPLICADOS_EXACTOS": int(
                df.duplicated().sum()
            ),
            "NULOS_TOTALES": int(
                df.isna().sum().sum()
            )
        }

        return resultado

    def validar_fecha(self, columna):

        if columna not in self.df.columns:
            return {}

        fechas = pd.to_datetime(
            self.df[columna],
            errors="coerce"
        )

        return {
            "NULOS_DESPUES_CONVERSION": int(
                fechas.isna().sum()
            ),
            "FECHA_MINIMA": fechas.min(),
            "FECHA_MAXIMA": fechas.max()
        }

    def validar_cantidad_positiva(self, columna):

        if columna not in self.df.columns:
            return {}

        cantidad = pd.to_numeric(
            self.df[columna],
            errors="coerce"
        )

        return {
            "NULOS": int(cantidad.isna().sum()),
            "VALORES_CERO_O_NEGATIVOS": int(
                (cantidad <= 0).sum()
            ),
            "MINIMO": cantidad.min(),
            "MAXIMO": cantidad.max()
        }

    def validar_limpieza_completa(self, nombre, df):

        resultado = {
            "DATASET": nombre,
            "FILAS": len(df),
            "COLUMNAS": len(df.columns),
            "DUPLICADOS_EXACTOS": int(
                df.duplicated().sum()
            ),
            "NULOS_TOTALES": int(
                df.isna().sum().sum()
            )
        }

        if "CANTIDAD" in df.columns:

            cantidad = pd.to_numeric(
                df["CANTIDAD"],
                errors="coerce"
            )

            resultado["CANTIDAD_NULOS"] = int(
                cantidad.isna().sum()
            )

            resultado["CANTIDAD_NO_POSITIVA"] = int(
                (cantidad <= 0).sum()
            )

        if "FECHA HECHO" in df.columns:

            fechas = pd.to_datetime(
                df["FECHA HECHO"],
                errors="coerce"
            )

            resultado["FECHAS_INVALIDAS"] = int(
                fechas.isna().sum()
            )

        if "FECHA DE REGISTRO" in df.columns:

            anios = pd.to_numeric(
                df["FECHA DE REGISTRO"],
                errors="coerce"
            )

            resultado["ANIOS_INVALIDOS"] = int(
                anios.isna().sum()
            )

            resultado["REGISTROS_ANIO_1900"] = int(
                (anios == 1900).sum()
            )

        return resultado

    def validar_todo(self):

        resultado = {
            "FILAS": len(self.df),
            "COLUMNAS": len(self.df.columns),
            "NULOS": self.validar_nulos(),
            "DUPLICADOS_EXACTOS": self.validar_duplicados(),
            "CLAVES_DUPLICADAS": self.validar_claves([
                "AÑO",
                "CODIGO_DANE_MUNICIPIO",
                "TIPO_VEHICULO"
            ]),
            "ANIO": self.validar_anio(),
            "DANE": self.validar_dane(),
            "TIPOS_VEHICULO": self.validar_tipos_vehiculo(),
            "CANTIDADES": self.validar_cantidades()
        }

        return resultado