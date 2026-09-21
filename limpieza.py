from pathlib import Path
import pandas as pd
from library import (
    LimpiadorRUNT,
    LimpiadorHurto,
    LimpiadorRecuperacion,
    BitacoraLimpieza,
    AnalizadorAtipicos,
    ValidadorDatos,
    ExtractorDatos
)


class ProcesoLimpieza:

    def __init__(self, carpeta_originales, carpeta_limpios):

        self.carpeta_originales = Path(carpeta_originales)
        self.carpeta_limpios = Path(carpeta_limpios)

        self.carpeta_limpios.mkdir(
            parents=True,
            exist_ok=True
        )

        self.bitacora = BitacoraLimpieza()
        self.validaciones = []

    # ========================================================
    # RUNT
    # ========================================================

    def limpiar_runt(self):

        ruta = (
            self.carpeta_originales
            / "CrecimientoParqueAutomotor.csv"
        )

        df = ExtractorDatos(ruta).cargar_csv()
        inicial = len(df)

        # ----------------------------------------------------
        # 1. DUPLICADOS
        # ----------------------------------------------------

        duplicados = int(df.duplicated().sum())

        limpiador = LimpiadorRUNT(df)

        limpiador.eliminar_duplicados()

        despues_duplicados = len(limpiador.df)

        self.bitacora.registrar(
            "RUNT",
            "DUPLICADOS",
            "Eliminación de duplicados exactos.",
            inicial,
            despues_duplicados,
            duplicados
        )

        # ----------------------------------------------------
        # 2. NORMALIZACIÓN
        # ----------------------------------------------------

        limpiador.normalizar()

        self.bitacora.registrar(
            "RUNT",
            "NORMALIZACION",
            "Normalización de textos: mayúsculas, espacios "
            "y eliminación de tildes.",
            len(limpiador.df),
            len(limpiador.df),
            0
        )

        # ----------------------------------------------------
        # 3. CATEGORÍA ESTADO
        # ----------------------------------------------------

        antes_activos = len(limpiador.df)

        limpiador.filtrar_activos()

        despues_activos = len(limpiador.df)

        self.bitacora.registrar(
            "RUNT",
            "CATEGORIAS_ESTADO",
            "Se conservaron únicamente los registros "
            "con estado ACTIVO. Los registros "
            "INCONSISTENTE no se utilizan para "
            "representar vehículos registrados.",
            antes_activos,
            despues_activos,
            antes_activos - despues_activos
        )

        # ----------------------------------------------------
        # 4. FECHA
        # ----------------------------------------------------

        antes_fecha = len(limpiador.df)

        limpiador.limpiar_fecha_registro()

        despues_fecha = len(limpiador.df)

        nulos_fecha = int(
            limpiador.df["FECHA DE REGISTRO"].isna().sum()
        )

        anios_1900 = int(
            (
                limpiador.df["FECHA DE REGISTRO"] == 1900
            ).sum()
        )

        self.bitacora.registrar(
            "RUNT",
            "FECHAS",
            f"Conversión de FECHA DE REGISTRO a "
            f"formato numérico. Se conservaron los "
            f"{anios_1900} registros con año 1900 para "
            f"su posterior revisión.",
            antes_fecha,
            despues_fecha,
            0
        )

        # ----------------------------------------------------
        # 5. CANTIDAD
        # ----------------------------------------------------

        antes_cantidad = len(limpiador.df)

        cantidad_original = limpiador.df["CANTIDAD"].copy()

        limpiador.limpiar_cantidad()

        despues_cantidad = len(limpiador.df)

        eliminados_cantidad = (
            antes_cantidad - despues_cantidad
        )

        self.bitacora.registrar(
            "RUNT",
            "VALORES_CANTIDAD",
            "Conversión de CANTIDAD a numérico y "
            "eliminación únicamente de valores nulos "
            "o menores o iguales a cero.",
            antes_cantidad,
            despues_cantidad,
            eliminados_cantidad
        )

        # ----------------------------------------------------
        # 6. ATÍPICOS
        # ----------------------------------------------------

        datos_atipicos = AnalizadorAtipicos(
            limpiador.df
        ).calcular_iqr("CANTIDAD")

        cantidad_atipicos = datos_atipicos.get(
            "VALORES_ATIPICOS",
            0
        )

        self.bitacora.registrar(
            "RUNT",
            "ATIPICOS",
            f"Se detectaron {cantidad_atipicos} "
            "posibles valores atípicos mediante IQR. "
            "No se eliminaron porque CANTIDAD representa "
            "cantidades agregadas y deben evaluarse "
            "según el contexto.",
            len(limpiador.df),
            len(limpiador.df),
            0
        )

        # ----------------------------------------------------
        # 7. COLUMNAS DE PUBLICACIÓN
        # ----------------------------------------------------

        columnas_antes = len(limpiador.df.columns)

        limpiador.eliminar_informacion_publicacion()

        columnas_despues = len(limpiador.df.columns)

        self.bitacora.registrar(
            "RUNT",
            "COLUMNAS_INFORMATIVAS",
            "Se eliminaron MES DE PUBLICACION y "
            "AÑO DE PUBLICACIÓN porque no representan "
            "el año de análisis de los vehículos.",
            len(limpiador.df),
            len(limpiador.df),
            0
        )

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        resultado = limpiador.obtener_resultado()

        self.validar_dataset(
            "RUNT",
            resultado
        )

        ruta_salida = (
            self.carpeta_limpios
            / "CrecimientoParqueAutomotor_limpio.csv"
        )

        resultado.to_csv(
            ruta_salida,
            index=False,
            encoding="utf-8-sig"
        )

        return resultado, datos_atipicos

    # ========================================================
    # HURTO
    # ========================================================

    def limpiar_hurto(self):

        ruta = (
            self.carpeta_originales
            / "HurtoVehiculos.csv"
        )

        df = ExtractorDatos(ruta).cargar_csv()
        inicial = len(df)

        # ----------------------------------------------------
        # 1. DUPLICADOS
        # ----------------------------------------------------

        duplicados = int(df.duplicated().sum())

        limpiador = LimpiadorHurto(df)

        limpiador.eliminar_duplicados()

        despues = len(limpiador.df)

        self.bitacora.registrar(
            "HURTO",
            "DUPLICADOS",
            "Eliminación de duplicados exactos.",
            inicial,
            despues,
            duplicados
        )

        # ----------------------------------------------------
        # 2. NORMALIZACIÓN
        # ----------------------------------------------------

        limpiador.normalizar()

        self.bitacora.registrar(
            "HURTO",
            "NORMALIZACION",
            "Normalización de departamentos, municipios, "
            "tipo de delito y zona.",
            len(limpiador.df),
            len(limpiador.df),
            0
        )

        # ----------------------------------------------------
        # 3. FECHA
        # ----------------------------------------------------

        antes_fecha = len(limpiador.df)

        limpiador.limpiar_fecha()

        despues_fecha = len(limpiador.df)

        fechas_invalidas = int(
            limpiador.df["FECHA HECHO"].isna().sum()
        )

        self.bitacora.registrar(
            "HURTO",
            "FECHAS",
            "Conversión de FECHA HECHO a formato fecha "
            "utilizando interpretación día/mes/año.",
            antes_fecha,
            despues_fecha,
            0
        )

        # ----------------------------------------------------
        # 4. CANTIDAD
        # ----------------------------------------------------

        antes_cantidad = len(limpiador.df)

        limpiador.limpiar_cantidad()

        despues_cantidad = len(limpiador.df)

        self.bitacora.registrar(
            "HURTO",
            "VALORES_CANTIDAD",
            "Conversión de CANTIDAD a numérico y "
            "eliminación únicamente de valores nulos "
            "o menores o iguales a cero.",
            antes_cantidad,
            despues_cantidad,
            antes_cantidad - despues_cantidad
        )

        # ----------------------------------------------------
        # 5. ATÍPICOS
        # ----------------------------------------------------

        datos_atipicos = AnalizadorAtipicos(
            limpiador.df
        ).calcular_iqr("CANTIDAD")

        cantidad_atipicos = datos_atipicos.get(
            "VALORES_ATIPICOS",
            0
        )

        self.bitacora.registrar(
            "HURTO",
            "ATIPICOS",
            f"Se detectaron {cantidad_atipicos} "
            "posibles valores atípicos mediante IQR. "
            "No se eliminaron automáticamente.",
            len(limpiador.df),
            len(limpiador.df),
            0
        )

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        resultado = limpiador.obtener_resultado()

        self.validar_dataset(
            "HURTO",
            resultado
        )

        ruta_salida = (
            self.carpeta_limpios
            / "HurtoVehiculos_limpio.csv"
        )

        resultado.to_csv(
            ruta_salida,
            index=False,
            encoding="utf-8-sig"
        )

        return resultado, datos_atipicos

    # ========================================================
    # RECUPERACIÓN
    # ========================================================

    def limpiar_recuperacion(self):

        ruta = (
            self.carpeta_originales
            / "RecuperacionPoliciaNacional.csv"
        )

        df = ExtractorDatos(ruta).cargar_csv()
        inicial = len(df)

        # ----------------------------------------------------
        # 1. DUPLICADOS
        # ----------------------------------------------------

        duplicados = int(df.duplicated().sum())

        limpiador = LimpiadorRecuperacion(df)

        limpiador.eliminar_duplicados()

        despues = len(limpiador.df)

        self.bitacora.registrar(
            "RECUPERACION",
            "DUPLICADOS",
            "Eliminación de duplicados exactos.",
            inicial,
            despues,
            duplicados
        )

        # ----------------------------------------------------
        # 2. NORMALIZACIÓN
        # ----------------------------------------------------

        limpiador.normalizar()

        self.bitacora.registrar(
            "RECUPERACION",
            "NORMALIZACION",
            "Normalización de departamentos, municipios "
            "y clase del bien.",
            len(limpiador.df),
            len(limpiador.df),
            0
        )

        # ----------------------------------------------------
        # 3. FECHA
        # ----------------------------------------------------

        antes_fecha = len(limpiador.df)

        limpiador.limpiar_fecha()

        despues_fecha = len(limpiador.df)

        self.bitacora.registrar(
            "RECUPERACION",
            "FECHAS",
            "Conversión de FECHA HECHO a formato fecha "
            "utilizando interpretación día/mes/año.",
            antes_fecha,
            despues_fecha,
            0
        )

        # ----------------------------------------------------
        # 4. CÓDIGO DANE
        # ----------------------------------------------------

        limpiador.limpiar_codigo_dane()

        self.bitacora.registrar(
            "RECUPERACION",
            "CODIGO_DANE",
            "Normalización del código DANE conservándolo "
            "como texto.",
            len(limpiador.df),
            len(limpiador.df),
            0
        )

        # ----------------------------------------------------
        # 5. CANTIDAD
        # ----------------------------------------------------

        antes_cantidad = len(limpiador.df)

        limpiador.limpiar_cantidad()

        despues_cantidad = len(limpiador.df)

        self.bitacora.registrar(
            "RECUPERACION",
            "VALORES_CANTIDAD",
            "Conversión de CANTIDAD a numérico y "
            "eliminación únicamente de valores nulos "
            "o menores o iguales a cero.",
            antes_cantidad,
            despues_cantidad,
            antes_cantidad - despues_cantidad
        )

        # ----------------------------------------------------
        # 6. ATÍPICOS
        # ----------------------------------------------------

        datos_atipicos = AnalizadorAtipicos(
            limpiador.df
        ).calcular_iqr("CANTIDAD")

        cantidad_atipicos = datos_atipicos.get(
            "VALORES_ATIPICOS",
            0
        )

        self.bitacora.registrar(
            "RECUPERACION",
            "ATIPICOS",
            f"Se detectaron {cantidad_atipicos} "
            "posibles valores atípicos mediante IQR. "
            "No se eliminaron automáticamente.",
            len(limpiador.df),
            len(limpiador.df),
            0
        )

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        resultado = limpiador.obtener_resultado()

        self.validar_dataset(
            "RECUPERACION",
            resultado
        )

        ruta_salida = (
            self.carpeta_limpios
            / "RecuperacionPoliciaNacional_limpio.csv"
        )

        resultado.to_csv(
            ruta_salida,
            index=False,
            encoding="utf-8-sig"
        )

        return resultado, datos_atipicos

    # ========================================================
    # VALIDACIÓN FINAL DE CADA DATASET
    # ========================================================

    def validar_dataset(self, nombre, df):

        validador = ValidadorDatos(df)

        resultado = validador.validar_limpieza_completa(
            nombre,
            df
        )

        self.validaciones.append(resultado)

        return resultado

    # ========================================================
    # GUARDAR BITÁCORA
    # ========================================================

    def guardar_bitacora(self):

        ruta = (
            self.carpeta_limpios
            / "bitacora_limpieza.csv"
        )

        self.bitacora.obtener_dataframe().to_csv(
            ruta,
            index=False,
            encoding="utf-8-sig"
        )

        return ruta

    # ========================================================
    # GUARDAR VALIDACIÓN
    # ========================================================

    def guardar_validacion(self):

        ruta = (
            self.carpeta_limpios
            / "validacion_limpieza.csv"
        )

        pd.DataFrame(self.validaciones).to_csv(
            ruta,
            index=False,
            encoding="utf-8-sig"
        )

        return ruta