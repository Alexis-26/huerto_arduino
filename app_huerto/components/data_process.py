from pymongo import MongoClient # Para el manejo de la base de datos en MongoDB
import pandas as pd                      # Para manejo de datos
import matplotlib.pyplot as plt          # Para gráficos
import seaborn as sns                    # Para gráficos bonitos
from sklearn.model_selection import train_test_split  # Para dividir datos
from sklearn.ensemble import RandomForestClassifier   # El modelo random forest
from sklearn.metrics import classification_report, confusion_matrix  # Para métricas

"""
Realiza la conexión a la base de datos.
"""
def conexion():
    try:
        URL = "mongodb+srv://alexis:Chokart$2978@cluster0.dx3fa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(URL)
        print("Conexion Exitosa...")
        return client
    except Exception as e:
        print(f"Conexion Fallida: {e}")

"""
Genera un Dataframe con todos los datos de la base de datos consultada.
"""

def generar_dataframe(client):
    # Extracción de los datos de la base de datos con el nombre "lecturas"
    db = client["sensores_db"]
    collection = db["lecturas"]

    # Busqueda con filtro para no obtener la columna "_id"
    resultados = collection.find({}, {"DHT.temp":1, "DHT.hum":1, "SOIL":1, "LDR":1, "PUMP":1, "timestamp":1, "_id":0})
    datos = list(resultados)

    # Convertir en dataframe
    df = pd.DataFrame(datos)

    #print(df)
    return df

"""
Realiza la transformación de los datos pertenecientes al sensor DHT para hacer una separación.
Además se realizar la conversión de la columna "timestap" a tipo datetime.
Por último elimina las columnas que no son útiles y reordena.
"""
def transformacion_columnas(df:pd.DataFrame):
    # Expandir las columnas DHT.temp y DHT.hum en columnas separadas
    df['temp'] = df['DHT'].apply(lambda x: x.get('temp') if x else None)
    df['hum'] = df['DHT'].apply(lambda x: x.get('hum') if x else None)

    # Convertir timestamp a datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Elimina la columa DHT
    df = df.drop(columns=['DHT'])

    # Reordenar columnas para que temp y hum estén al inicio
    cols = ['temp', 'hum'] + [col for col in df.columns if col not in ['temp', 'hum']]
    df = df[cols]

    print(df)
    return df

"""
Verifica la estructura de datos, revisión de datos nulos y duplicados para su posterior eliminación.
"""
def verificar_calidad(df:pd.DataFrame):
    # Revisa la estructura
    print(df.head())

    # Revisa los tipos de datos
    print(df.dtypes)

    # Nulos
    if df.isnull().values.any():
        print("Hay datos nulos en el DataFrame.")
        print(df.isnull().sum())
    else:
        print("No hay datos nulos en el DataFrame.")
        print(df.isnull().sum())
    
    # Duplicados
    if df.duplicated().any():
        print("Hay filas duplicadas en el DataFrame.")
    else:
        print("No hay filas duplicadas en el DataFrame.")

    return df

"""
Crea una nueva columna a partir de la existente PUMP para categorizar de forma más comprensible.
Además se generan nuevos datos a partir de un dato existente para tener un balance y permita construir un modelo.
"""
def columna_pump(df:pd.DataFrame):
    # Añadir columna "pump_satus" si es 0 apagado, si es 1 encendido
    df['pump_status'] = df['PUMP'].apply(lambda x: 'apagado' if x == 0 else 'encendido')

    import numpy as np

    def add_noise(df, columns, noise_level=0.1):
        df_noisy = df.copy()
        for col in columns:
            df_noisy[col] = df_noisy[col] + np.random.normal(0, noise_level, size=df_noisy.shape[0])
        return df_noisy

    # Filas con PUMP = 1
    df_minority = df[df['PUMP'] == 1]

    # Genera 100 copias con ruido
    synthetic_minority = pd.concat([add_noise(df_minority, ['temp', 'hum', 'SOIL', 'LDR']) for _ in range(100)], ignore_index=True)

    # Junta con los datos originales
    df_balanced = pd.concat([df, synthetic_minority], ignore_index=True)

    print(df_balanced)
    return df_balanced

"""
Genera estadística básica de cada columna.
"""
def estadistica_basica(df:pd.DataFrame):
    # Estadísticas de la columna 'temp'
    print("\nEstadísticas de la columna 'temp':")
    print(df['temp'].describe())

    # Estadísticas de la columna 'hum'
    print("\nEstadísticas de la columna 'hum':")
    print(df['hum'].describe())

    # Estadísticas de la columna 'SOIL'
    print("\nEstadísticas de la columna 'SOIL':")
    print(df['SOIL'].describe())

    # Estadísticas de la columna 'LDR'
    print("\nEstadísticas de la columna 'LDR':")
    print(df['LDR'].describe())
    return df

"""
Ayuda a realizar un EDA (Analisis Exploratorio de los Datos) para identificar relaciones.
"""
def eda(df:pd.DataFrame):
    # Calcula matriz de correlación
    corr = df[['temp', 'hum', 'SOIL', 'LDR', 'PUMP']].corr()

    # Dibuja heatmap
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Matriz de correlación')
    plt.show()

    sns.pairplot(df, vars=['temp', 'hum', 'SOIL', 'LDR'], hue='pump_status')
    plt.show()
    return df

"""
Crea un modelo random forest a partir de los datos obtenidos. 
Además muestra información para evaluar el modelo.
"""
def modelo(df:pd.DataFrame):
    # --- Features y target ---
    X = df[['temp', 'hum', 'SOIL', 'LDR']]
    y = df['PUMP']  # Ya es 0 y 1

    # --- Dividir en train/test ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    # --- RandomForest con balanceo ---
    rf = RandomForestClassifier(class_weight='balanced', random_state=42)
    rf.fit(X_train, y_train)

    # --- Predicciones ---
    y_pred = rf.predict(X_test)

    # --- Reporte ---
    print("\n--- Reporte de Clasificación ---")
    print(classification_report(y_test, y_pred))

    print("\n--- Matriz de Confusión ---")
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicho')
    plt.ylabel('Real')
    plt.show()

    # --- Importancia de variables ---
    importances = pd.Series(rf.feature_importances_, index=X.columns)
    importances.sort_values().plot(kind='barh')
    plt.title('Importancia de las variables')
    plt.show()

    return rf

"""
Esta función permite útilizar el modelo creado para probar el funcionamiento de la predicción.
Obteniendo como resultado una simulación de predicción según los paramétros insertados.
"""
def prediccion_manual(rf_model):
    # Pedir valores al usuario
    temp = float(input("Ingresa temperatura (temp): "))
    hum = float(input("Ingresa humedad (hum): "))
    soil = float(input("Ingresa humedad del suelo (SOIL): "))
    ldr = float(input("Ingresa luz (LDR): "))
    
    # Crear DataFrame con un solo registro
    nuevo_dato = pd.DataFrame([[temp, hum, soil, ldr]], columns=['temp', 'hum', 'SOIL', 'LDR'])
    
    # Predecir
    prediccion = rf_model.predict(nuevo_dato)[0]
    
    # Mostrar resultado
    if prediccion == 1:
        print("💧 Encender la bomba (PUMP = 1)")
    else:
        print("✅ No es necesario encender la bomba (PUMP = 0)")
    

if __name__ == "__main__":
    conexion = conexion()
    if conexion:
        df = generar_dataframe(conexion)
        df = transformacion_columnas(df)
        df = verificar_calidad(df)
        df = columna_pump(df)
        df = estadistica_basica(df)
        df = eda(df)
        rf = modelo(df)
        prediccion_manual(rf)
