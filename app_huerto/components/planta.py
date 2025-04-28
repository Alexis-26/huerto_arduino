import reflex as rx

def lista_plantas() -> rx.Component:
    return rx.box(
        rx.heading("Lista de plantas", weight="medium", size="4", color="#FFFFFF"),
        rx.vstack(
            rx.hstack(
                rx.avatar(src="/tomates.jpg", radius="full", size="4", background_color="#FFFFFF"),
                rx.heading("Tomates", weight="medium", size="4"),
                align="center",
                background="#BBD8A3",
                width="100%",
                height="80px",
                border_radius="10px",
                padding_left="10px"
            ),
            rx.hstack(
                rx.avatar(src="/papa.jpg", radius="full", size="4", background_color="#FFFFFF"),
                rx.heading("Papa", weight="medium", size="4"),
                align="center",
                background="#BBD8A3",
                width="100%",
                height="80px",
                border_radius="10px",
                padding_left="10px"
            ),
            rx.hstack(
                rx.avatar(src="/aloe.jpg", radius="full", size="4", background_color="#FFFFFF"),
                rx.heading("Aloe Vera", weight="medium", size="4"),
                align="center",
                background="#BBD8A3",
                width="100%",
                height="80px",
                border_radius="10px",
                padding_left="10px"
            ),
            width="100%",
            spacing="6",
            margin_top="20px",
            #background="green"
        ),
        margin="20px",
        #background="blue"
    )

def planta() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.box(
                rx.flex(
                    rx.box(
                        rx.image(src="/girasol.gif"),
                    ),
                    #background="red",
                    align="center",
                    justify="center",
                    width="100%",
                    height="100%"
                ),
                background="center/cover url('/fondo_cosecha1.jpg')",
                width="100%",
                height="40%"
            ),
            rx.box(
                lista_plantas(),
                #background="red",
                width="100%"
            ),
            width="100%",
            height="100%"
        ),
        height="100vh",
        width="30em",
        background="#6F826A"
    )