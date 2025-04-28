from .head import head_page
from .kpi import kpi
from .linechart_dash import char_area_luz, radial_bar_advanced
from .graficas import char_humtemp, char_soil, char_ldr, char_pump
import reflex as rx

def body() -> rx.Component:
    return rx.box(
        rx.vstack(
            head_page(),
            kpi(),
            rx.hstack(
                char_area_luz(),
                radial_bar_advanced(),
                width="100%",
                height="400px",
                margin_top="20px"
            ),
        ),
        width="100%",
        height="100vh",
        padding_left="40px",
        padding_right="40px",
        background="#E7F0DC"
    )

def body_analisis() -> rx.Component:
    return rx.box(
        rx.vstack(
            head_page(),
            rx.hstack(
                char_humtemp(),
                char_soil(),
                width="100%",
                height="300px",
                #margin_top="20px"
            ),
            rx.hstack(
                char_ldr(),
                char_pump(),
                width="100%",
                height="300px",
                #margin_top="20px"
            ),
        ),
        width="100%",
        height="100vh",
        padding_left="40px",
        padding_right="40px",
        background="#E7F0DC"
    )