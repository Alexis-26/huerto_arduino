from .components.sidebar import sidebar
from .components.body import body, body_analisis
from .components.planta import planta
from .state import DataState
import reflex as rx


def index() -> rx.Component:
    return rx.box(
        rx.hstack(
            sidebar(),
            body(),
            planta(),
            gap="0"
        ),
        #background="green",
        height="100%"
    )

def analisis() -> rx.Component:
    return rx.box(
        rx.hstack(
            sidebar(),
            body_analisis(),
            planta(),
            gap="0"
        ),
        #background="green",
        height="100%"
    )


app = rx.App(theme=rx.theme(color_mode="light"))
app.add_page(index, route="/", on_load=DataState.load_data)
app.add_page(analisis, route="/analisis")
