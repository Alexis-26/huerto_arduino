import reflex as rx
from collections import Counter
from ..state import DataState

# data = [
#     {"name": "08:00", "hum": 78, "temp": 35},
#     {"name": "09:00", "hum": 83, "temp": 32},
#     {"name": "10:00", "hum": 87, "temp": 30},
#     {"name": "11:00", "hum": 76, "temp": 34},
#     {"name": "12:00", "hum": 76, "temp": 30},
#     {"name": "13:00", "hum": 84, "temp": 31},
#     {"name": "14:00", "hum": 90, "temp": 29},
#     {"name": "15:00", "hum": 88, "temp": 33},
#     {"name": "16:00", "hum": 97, "temp": 36},
#     {"name": "17:00", "hum": 95, "temp": 34},
#     {"name": "18:00", "hum": 86, "temp": 31},
#     {"name": "19:00", "hum": 93, "temp": 30},
# ]

# data1 = [
#     {"name": "08:00", "soil": 78},
#     {"name": "09:00", "soil": 83},
#     {"name": "10:00", "soil": 87},
#     {"name": "11:00", "soil": 76},
#     {"name": "12:00", "soil": 76},
#     {"name": "13:00", "soil": 84},
#     {"name": "14:00", "soil": 90},
#     {"name": "15:00", "soil": 88},
#     {"name": "16:00", "soil": 97},
#     {"name": "17:00", "soil": 95},
#     {"name": "18:00", "soil": 86},
#     {"name": "19:00", "soil": 93},
# ]
# data2 = [
#     {"name": "08:00", "ldr": 78},
#     {"name": "09:00", "ldr": 83},
#     {"name": "10:00", "ldr": 87},
#     {"name": "11:00", "ldr": 76},
#     {"name": "12:00", "ldr": 76},
#     {"name": "13:00", "ldr": 84},
#     {"name": "14:00", "ldr": 90},
#     {"name": "15:00", "ldr": 88},
#     {"name": "16:00", "ldr": 97},
#     {"name": "17:00", "ldr": 95},
#     {"name": "18:00", "ldr": 86},
#     {"name": "19:00", "ldr": 93},
# ]

# data3 = [
#     {"name": "08:00", "pump": 0},
#     {"name": "09:00", "pump": 0},
#     {"name": "10:00", "pump": 1},
#     {"name": "11:00", "pump": 0},
#     {"name": "12:00", "pump": 0},
#     {"name": "13:00", "pump": 0},
#     {"name": "14:00", "pump": 1},
#     {"name": "15:00", "pump": 0},
#     {"name": "16:00", "pump": 0},
#     {"name": "17:00", "pump": 1},
#     {"name": "18:00", "pump": 0},
#     {"name": "19:00", "pump": 0},
# ]


def char_humtemp() -> rx.Component:
    return rx.box(
        rx.heading("Humedad y Temperatura vs. Tiempo", weight="regular", size="5", margin_left="10px"),
        #grafica
        rx.recharts.line_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.line(data_key="hum", dot = True, stroke="#6F826A", stroke_width=4),
            rx.recharts.line(data_key="temp", dot=True, stroke="#9EC6F3", stroke_width=4),
            rx.recharts.x_axis(data_key="timestamp"),
            rx.recharts.y_axis(),
            rx.recharts.brush(
                data_key="timestamp", stroke="#6F826A", fill="#F0F1C5"
            ),
            data=DataState.temp_hum,
            width="100%",
            height="100%",
        ),
        width="50%",
        height="100%",
        background="#FFFFFF",
        border_radius="20px",
        padding="20px"
    )

def char_soil() -> rx.Component:
    return rx.box(
        rx.heading("Humedad del Suelo (SOIL) vs. Tiempo", weight="regular", size="5", margin_left="10px"),
        #grafica
        rx.recharts.area_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.area(data_key="SOIL", dot=True, stroke="#BF9264", stroke_width=4, fill="#BBD8A3"),
            rx.recharts.x_axis(data_key="timestamp"),
            rx.recharts.y_axis(),
            rx.recharts.brush(
                data_key="timestamp", stroke="#6F826A", fill="#F0F1C5"
            ),
            data=DataState.soil,
            width="100%",
            height="100%",
        ),
        width="50%",
        height="100%",
        background="#FFFFFF",
        border_radius="20px",
        padding="20px"
    )

def char_ldr() -> rx.Component:
    return rx.box(
        rx.heading("Luz (LDR) vs. Tiempo", weight="regular", size="5", margin_left="10px"),
        #grafica
        rx.recharts.bar_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.bar(data_key="LDR", fill="#F0A04B"),
            rx.recharts.x_axis(data_key="timestamp"),
            rx.recharts.y_axis(),
            rx.recharts.brush(
                data_key="timestamp", stroke="#6F826A", fill="#F0F1C5"
            ),
            data=DataState.ldr,
            width="100%",
            height="100%",
        ),
        width="50%",
        height="100%",
        background="#FFFFFF",
        border_radius="20px",
        padding="20px"
    )

# def char_pump() -> rx.Component:
#     return rx.box(
#         rx.heading("Estado de la Bomba (PUMP) vs. Tiempo", weight="regular", size="5", margin_left="10px"),
#         #grafica
#         rx.recharts.scatter_chart(
#             rx.recharts.scatter(data=data3, fill="#8884d8"),
#             rx.recharts.x_axis(data_key="name"),
#             rx.recharts.y_axis(data_key="pump"),
#             rx.recharts.graphing_tooltip(),
#             width="100%",
#             height="100%",
#         ),
#         width="50%",
#         height="100%",
#         background="#FFFFFF",
#         border_radius="20px",
#         padding="20px"
#     )

def char_pump() -> rx.Component:
    return rx.box(
        rx.heading("Cantidad de veces utilizada la Bomba (PUMP) durante el día", weight="regular", size="5", margin_left="10px"),
        #grafica
        rx.recharts.bar_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.bar(data_key="frecuencia", fill="#9EC6F3"),
            rx.recharts.x_axis(data_key="valor"),
            rx.recharts.y_axis(),
            data=DataState.pump,
            width="100%",
            height="100%",
        ),
        width="50%",
        height="100%",
        background="#FFFFFF",
        border_radius="20px",
        padding="20px"
    )