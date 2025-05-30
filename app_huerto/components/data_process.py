from pymongo import MongoClient
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def conexion():
    try:
        URL = "mongodb+srv://alexis:Chokart$2978@cluster0.dx3fa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(URL)
        print("Conexion Exitosa...")
        return client
    except:
        print("Conexion Fallida")

def generar_dataframe(client):
    # Extracción de los datos de la base de datos con el nombre "lecturas"
    db = client["sensores_db"]
    collection = db["lecturas"]

    # Busqueda con filtro para no obtener la columna "_id"
    resultados = collection.find({}, {"DHT.temp":1, "DHT.hum":1, "SOIL":1, "LDR":1, "PUMP":1, "timestamp":1, "_id":0})
    datos = list(resultados)

    # Convertir en dataframe
    df = pd.DataFrame(datos)

    return df

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

    return df

def verificar_calidad(df:pd.DataFrame):
    # Revisa la estructura
    print(df.head())

    # Revisa los tipos de datos
    print(df.dtypes)

    # Nulos
    if df.isnull().values.any():
        print("Hay datos nulos en el DataFrame.")
    else:
        print("No hay datos nulos en el DataFrame.")
    
    # Duplicados
    if df.duplicated().any():
        print("Hay filas duplicadas en el DataFrame.")
    else:
        print("No hay filas duplicadas en el DataFrame.")

    return df

def columna_pump(df:pd.DataFrame):
    # Añadir columna "pump_satus" si es 0 apagado, si es 1 encendido
    df['pump_status'] = df['PUMP'].apply(lambda x: 'apagado' if x == 0 else 'encendido')
    print(df)
    return df

def estadistica_basica(df:pd.DataFrame):
    # Estadísticas básicas
    # print("Estadísticas básicas:")
    # print(df.describe())

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

def eda(df:pd.DataFrame):
    # Calcula matriz de correlación
    corr = df[['temp', 'hum', 'SOIL', 'LDR', 'PUMP']].corr()

    # Dibuja heatmap
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Matriz de correlación')
    plt.show(block=True)

if __name__ == "__main__":
    conexion = conexion()
    if conexion:
        df = generar_dataframe(conexion)
        df = transformacion_columnas(df)
        df = verificar_calidad(df)
        df = columna_pump(df)
        df = estadistica_basica(df)
        df = eda(df)