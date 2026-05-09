from sklearn.ensemble import IsolationForest

def detectar_anomalias(df):

    modelo = IsolationForest(
        contamination=0.1,
        random_state=42
    )

    df["anomalia"] = modelo.fit_predict(
        df[["ventas"]]
    )

    anomalias = df[df["anomalia"] == -1]

    return anomalias