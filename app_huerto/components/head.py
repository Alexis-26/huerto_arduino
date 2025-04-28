from ..state import MomentState
import reflex as rx

def head_page() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.heading("Bienvenido Usuario", weight="medium", size="8"),
                rx.hstack(
                    rx.icon("calendar"),
                    rx.heading("Fecha:", weight="regular", size="4"),
                    rx.heading(rx.moment(MomentState.date_now, format="DD-MM-YYYY"), weight="regular", size="4"),
                    align="center"
                )
            ),
            align="center",
            justify="start",
            width="100%",
            height="100%"
        ),
        width="100%",
        height="150px",
    )