from ..state import DataState
import reflex as rx

# data = [
#     {"name": "Page A", "pv": 2400, "uv": 4000},
#     {"name": "Page B", "pv": 1398, "uv": 2210},
#     {"name": "Page C", "pv": 9800, "uv": 2290},
#     {"name": "Page D", "pv": 3908, "uv": 2000},
#     {"name": "Page E", "pv": 4800, "uv": 2181},
#     {"name": "Page F", "pv": 3800, "uv": 2500},
#     {"name": "Page G", "pv": 4300, "uv": 2100},
# ]
data = [
    {"name": "08:00", "ldr": 78},
    {"name": "09:00", "ldr": 83},
    {"name": "10:00", "ldr": 87},
    {"name": "11:00", "ldr": 76},
    {"name": "12:00", "ldr": 76},
    {"name": "13:00", "ldr": 84},
    {"name": "14:00", "ldr": 90},
    {"name": "15:00", "ldr": 88},
    {"name": "16:00", "ldr": 97},
    {"name": "17:00", "ldr": 95},
    {"name": "18:00", "ldr": 86},
    {"name": "19:00", "ldr": 93},
]


def obtener_color_soil(valor):
    if valor > 70:
        return "#43a047"  # Verde
    elif 40 <= valor <= 70:
        return "#fbc02d"  # Amarillo
    else:
        return "#e53935"  # Rojo

soil_value = 78  # Ejemplo: toma el último valor de tus datos
data_2 = [
    {"name": "SOIL", "valor": soil_value, "fill": obtener_color_soil(soil_value)},
]

# def char_area_luz() -> rx.Component:
#     return rx.box(
#         rx.heading("Tendencia de Luz (LDR)", weight="regular", size="5", margin_left="10px"),
#         rx.recharts.area_chart(
#             rx.recharts.area(data_key="ldr", dot=True),
#             rx.recharts.x_axis(data_key="name"),
#             rx.recharts.y_axis(),
#             rx.recharts.graphing_tooltip(),
#             data=data,
#             width="100%",
#             height="100%",
#         ),
#         width="100%",
#         height="100%",
#         background="#FFFFFF",
#         border_radius="20px",
#         padding="20px"
#     )

def char_area_luz() -> rx.Component:
    return rx.box(
        rx.heading("Resumen del Día", weight="regular", size="5", margin_left="10px"),
        rx.recharts.bar_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.bar(data_key="hum", fill="#6F826A"),
            rx.recharts.bar(data_key="temp", fill="#9EC6F3"),
            rx.recharts.bar(data_key="SOIL", fill="#BF9264"),
            rx.recharts.bar(data_key="LDR", fill="#F0A04B"),
            rx.recharts.x_axis(data_key="timestamp"),
            rx.recharts.y_axis(),
            rx.recharts.brush(
                data_key="timestamp", stroke="#6F826A", fill="#F0F1C5"
            ),
            rx.recharts.legend(),
            data=DataState.resumen,
            width="100%",
            height="100%",
        ),
        width="100%",
        height="100%",
        background="#FFFFFF",
        border_radius="20px",
        padding="20px"
    )


# def linechart_dashboard_agua() -> rx.Component:
#     return rx.box(
#         rx.heading("Grafica 1", weight="regular", size="5", margin_left="10px"),
#         rx.recharts.line_chart(
#             rx.recharts.line(data_key="pv"),
#             rx.recharts.line(data_key="uv"),
#             rx.recharts.x_axis(data_key="name"),
#             rx.recharts.y_axis(),
#             data=data,
#             width="100%",
#             height="100%",
#         ),
#         width="50%",
#         height="100%",
#         background="#FFFFFF",
#         border_radius="20px",
#         padding="20px"
#     )

def radial_bar_advanced():
    return rx.box(
        rx.heading("Salud de la Planta", weight="regular", size="5", margin_left="10px"),
        rx.vstack(
            rx.box(
                rx.recharts.radial_bar_chart(
                    rx.recharts.radial_bar(
                        data_key="valor",
                        label={"position": "insideStart"},
                    ),
                    data=data_2,
                    inner_radius="30%",
                    outer_radius="100%",
                    start_angle=180,
                    end_angle=0,
                    width=300,
                    height=300,
                    #background="red"
                ),
                rx.text(
                    "Buena",
                    size="6",
                    weight="bold",
                    style={
                        "position": "absolute",
                        "top": "60%",
                        "left": "50%",
                        "transform": "translate(-50%, -50%)",
                        "pointer-events": "none",
                    },
                ),
                style={
                    "position": "relative",
                    "width": "300px",
                    "height": "300px",
                },
            ),
            align="center",
            justify="center",
        ),
        width="40%",
        height="100%",
        background="#FFFFFF",
        border_radius="20px",
        padding="20px"
    )