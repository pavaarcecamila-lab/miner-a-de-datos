def diagnosticar_datos(df, nombre):
    print(f"\n===== DIAGNÓSTICO: {nombre} =====")

    print("Dimensiones:", df.shape)

    print("\nPrimeras filas:")
    print(df.head())

    print("\nTipos de datos:")
    print(df.dtypes)

    print("\nValores nulos:")
    print(df.isna().sum())

    print("\nDuplicados exactos:", df.duplicated().sum())

    print("\nValores únicos:")
    for columna in df.columns:
        print(f"\n{columna}:")
        print(df[columna].unique()[:20])

        df = pd.read_csv(ruta)

jj=diagnosticar_datos(df, "Parque Automotor RUNT")