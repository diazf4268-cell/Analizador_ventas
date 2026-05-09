def calcular_kpis(df):

    ventas_totales = df["ventas"].sum()
    promedio = df["ventas"].mean()
    maximo = df["ventas"].max()
    minimo = df["ventas"].min()

    return (
        ventas_totales,
        promedio,
        maximo,
        minimo
    )