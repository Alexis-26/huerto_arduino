from ..state import DataState
import reflex as rx

def kpi() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.hstack(
                    rx.avatar(src="/tomates.jpg", radius="full", size="4"),
                    rx.heading("Tomates", weight="regular", size="6"),
                    align="center"
                ),
                margin_top="20px"
            ),
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.avatar(src="/planta.png", radius="full", size="4", background_color="#FFFFFF"),
                        rx.heading(DataState.hum_tierra, weight="regular", size="6", color="#FFFFFF"),
                        rx.hstack(
                            rx.icon("circle-alert", color="#FFFFFF"),
                            rx.text("Humedad de la tierra", color="#FFFFFF")
                        ),
                        width="100%",
                        align="center"
                    ), 
                    width="250px", 
                    height="150px",
                    background="#6F826A",
                    border_radius="20px",
                    padding="10px"
                    ),
                rx.box(
                    rx.vstack(
                        rx.avatar(src="/energia-verde.png", radius="full", size="4", background_color="#FFFFFF"),
                        rx.heading(DataState.luz, weight="regular", size="6", color="#FFFFFF"),
                        rx.hstack(
                            rx.icon("circle-alert", color="#FFFFFF"),
                            rx.text("Luz recibida", color="#FFFFFF")
                        ),
                        width="100%",
                        align="center"
                    ), 
                    width="250px", 
                    height="150px",
                    background="#6F826A",
                    border_radius="20px",
                    padding="10px"
                    ),
                rx.box(
                    rx.vstack(
                        rx.avatar(src="dia-nublado.png", radius="full", size="4", background_color="#FFFFFF"),
                        rx.heading(DataState.temp, weight="regular", size="6", color="#FFFFFF"),
                        rx.hstack(
                            rx.icon("circle-alert", color="#FFFFFF"),
                            rx.text("Temperatura ambiental", color="#FFFFFF")
                        ),
                        width="100%",
                        align="center"
                    ),  
                    width="250px", 
                    height="150px",
                    background="#6F826A",
                    border_radius="20px",
                    padding="10px"
                    ),
                justify="between",
                width="100%"
            ),
            margin_left="40px",
            margin_right="40px",
            spacing="5"
        ),
        width="100%",
        height="250px",
        background="#FFFFFF",
        border_radius="20px"
    )