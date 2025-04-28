from ..state import StateSidebar
import reflex as rx

def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.avatar(src="/logo-ecode.png", size="5", radius="full", background_color="#FFFFFF"),
                rx.heading("ECODE"),
                margin_top="40px",
                align="center"
            ),
            rx.vstack(
                rx.link(
                    rx.button(rx.icon("layout-dashboard"), rx.text("Dashboard"), width="100%", height="50px", border_radius="40px", 
                              background=rx.cond(StateSidebar.current_path == "/", "#FFFFFF", "#BBD8A3"), color="#000000"),
                    href="/",
                    width="100%"
                ),
                rx.link(
                    rx.button(rx.icon("chart-column"), rx.text("Analisis"), width="100%", height="50px", border_radius="40px", 
                              background=rx.cond(StateSidebar.current_path == "/analisis", "#FFFFFF", "#BBD8A3"), color="#000000"),
                    href="/analisis",
                    width="100%"
                ),
                rx.link(
                    rx.button(rx.icon("user-round"), rx.text("Perfil"), width="100%", height="50px", border_radius="40px", background="#BBD8A3", color="#000000"),
                    width="100%"
                ),
                rx.link(
                    rx.button(rx.icon("cog"), rx.text("Configuracion"), width="100%", height="50px", border_radius="40px", background="#BBD8A3", color="#000000"),
                    width="100%"
                ),
                #background="red",
                width="80%",
                spacing="5",
            ),
            gap="60px",
            width="100%",
            align="center"
        ),
        height="100vh",
        width="20em",
        background="#BBD8A3"
    )