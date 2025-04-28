import reflex as rx
from datetime import datetime, timezone
from pymongo import MongoClient
from collections import Counter
import pandas as pd

def conexion():
    URL = "mongodb+srv://alexis:Chokart$2978@cluster0.dx3fa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(URL)
    return client

def consulta(filtro:dict, columnas:dict):
    client = conexion()
    db = client["sensores_db"]
    collection = db["lecturas"]
    resultados = collection.find(filtro, columnas)
    # for documento in resultados:
    #     print(documento)
    # client.close()
    return list(resultados)

# def add_horas(datos, columnas:dict):
#     # Lo pasamos a un DataFrame
#     df = pd.DataFrame(datos)

#     # Creamos una nueva columna con la hora
#     df["hour"] = df["timestamp"].dt.strftime('%H:00')

#     # Ahora agrupamos, por ejemplo, sacando el promedio de temperatura y humedad por hora
#     df_por_hora = df.groupby("hour").agg({"temp": "mean", "hum": "mean"}).reset_index()

#     # Redondeamos si quieres
#     df_por_hora["temp"] = df_por_hora["temp"].round(2)
#     df_por_hora["hum"] = df_por_hora["hum"].round(2)

#     # Formateamos al estilo que necesitas
#     data_final = [{"timestamp": row["hour"], "temp": row["temp"], "hum": row["hum"]} for idx, row in df_por_hora.iterrows()]


class MomentState(rx.State):
    date_now: datetime = datetime.now(timezone.utc)

    @rx.event
    def update(self):
        self.date_now = datetime.now(timezone.utc)

class StateSidebar(rx.State):
    @rx.var
    def current_path(self) -> str:
        return self.router.page.path
    
class DataState(rx.State):
    temp_hum:list = []
    soil:list = []
    ldr:list = []
    pump:list = []
    resumen:list = []
    hum_tierra:str = ""
    luz:str = ""
    temp:str = ""
    fecha_inicio = datetime(2025, 4, 27, 0, 0, 0)
    fecha_fin = datetime(2025, 4, 27, 23, 59, 59)


    def load_data(self):
        self.temp_hum = []
        self.soil = []
        self.ldr = []
        self.pump = []
        self.resumen = []
        
        resultados = consulta({"timestamp":{"$gte":self.fecha_inicio, "$lte":self.fecha_fin}}, {"DHT.temp":1, "DHT.hum":1, "SOIL":1, "LDR":1, "timestamp":1, "_id":0})
        for d in resultados:
            nuevo = d['DHT'].copy()  # copiamos temp y hum
            nuevo["SOIL"] = d["SOIL"]
            nuevo["LDR"] = d["LDR"]
            nuevo['timestamp'] = d["timestamp"]  # añadimos el timestamp
            self.resumen.append(nuevo)
                # Lo pasamos a un DataFrame
        df = pd.DataFrame(self.resumen)

        # Creamos una nueva columna con la hora
        df["hour"] = df["timestamp"].dt.strftime('%H:00')

        # Ahora agrupamos, por ejemplo, sacando el promedio de temperatura y humedad por hora
        df_por_hora = df.groupby("hour").agg({"temp": "mean", "hum": "mean", "SOIL":"mean", "LDR":"mean"}).reset_index()

        # Redondeamos si quieres
        df_por_hora["temp"] = df_por_hora["temp"].round(2)
        df_por_hora["hum"] = df_por_hora["hum"].round(2)
        # Formateamos al estilo que necesitas
        data_final = [{"timestamp": row["hour"], "temp": row["temp"], "hum": row["hum"], "SOIL": row["SOIL"], "LDR": row["LDR"]} for idx, row in df_por_hora.iterrows()]
        self.resumen = data_final

        ultimo_dato = self.resumen[-1]
        humtierra = ultimo_dato["SOIL"]
        luzd = ultimo_dato["LDR"]
        tempd = ultimo_dato["temp"]
        self.hum_tierra = f"{str(humtierra)}%"
        self.luz = f"{str(luzd)}"
        self.temp = f"{str(tempd)}°C"


        resultados = consulta({"timestamp":{"$gte":self.fecha_inicio, "$lte":self.fecha_fin}}, {"DHT.temp":1, "DHT.hum":1, "timestamp":1, "_id":0})
        #print(resultados)
        for d in resultados:
            nuevo = d['DHT'].copy()  # copiamos temp y hum
            nuevo['timestamp'] = d['timestamp']  # añadimos el timestamp
            self.temp_hum.append(nuevo)

        df = pd.DataFrame(self.temp_hum)
        # Creamos una nueva columna con la hora
        df["hour"] = df["timestamp"].dt.strftime('%H:00')
        # Ahora agrupamos, por ejemplo, sacando el promedio de temperatura y humedad por hora
        df_por_hora = df.groupby("hour").agg({"temp": "mean", "hum": "mean"}).reset_index()
        data_final = [{"timestamp": row["hour"], "temp": row["temp"], "hum": row["hum"]} for idx, row in df_por_hora.iterrows()]
        self.temp_hum = data_final

        resultados = consulta({"timestamp":{"$gte":self.fecha_inicio, "$lte":self.fecha_fin}}, {"SOIL":1, "timestamp":1, "_id":0})
        df = pd.DataFrame(resultados)
        # Creamos una nueva columna con la hora
        df["hour"] = df["timestamp"].dt.strftime('%H:00')
        # Ahora agrupamos, por ejemplo, sacando el promedio de temperatura y humedad por hora
        df_por_hora = df.groupby("hour").agg({"SOIL": "mean"}).reset_index()
        data_final = [{"timestamp": row["hour"], "SOIL": row["SOIL"]} for idx, row in df_por_hora.iterrows()]
        self.soil = data_final

        resultados = consulta({"timestamp":{"$gte":self.fecha_inicio, "$lte":self.fecha_fin}}, {"LDR":1, "timestamp":1, "_id":0})
        df = pd.DataFrame(resultados)
        # Creamos una nueva columna con la hora
        df["hour"] = df["timestamp"].dt.strftime('%H:00')
        # Ahora agrupamos, por ejemplo, sacando el promedio de temperatura y humedad por hora
        df_por_hora = df.groupby("hour").agg({"LDR": "mean"}).reset_index()
        data_final = [{"timestamp": row["hour"], "LDR": row["LDR"]} for idx, row in df_por_hora.iterrows()]
        self.ldr = data_final

        # Contar la frecuencia de los valores 0 y 1 en el campo "pump"
        resultados = consulta({"timestamp":{"$gte":self.fecha_inicio, "$lte":self.fecha_fin}}, {"PUMP":1, "timestamp":1, "_id":0})
        conteo = Counter(item["PUMP"] for item in resultados)
        etiquetas = {0: "apagada", 1: "encendida"}
        data_freq = [{"valor": etiquetas[k], "frecuencia": v} for k, v in conteo.items()]
        self.pump = data_freq
