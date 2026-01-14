import flet as ft
from hashzap.config import Config, logger


def main(page: ft.Page):
    page.title = "Hashzap | Flet Chat"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.window_width = 400
    page.window_height = 650
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Elementos do Chat
    user_name = ft.TextField(
        label="Membro", width=200, border_radius=10, text_align=ft.TextAlign.CENTER
    )
    message_field = ft.TextField(
        hint_text="Mensagem...", expand=True, border_radius=25, content_padding=15
    )
    chat = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=10)

    def on_message_received(message):
        if message["type"] == "chat":
            is_me = message["user"] == user_name.value
            msg_bubble = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Você" if is_me else message["user"],
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLUE_700 if is_me else ft.colors.PRIMARY,
                        ),
                        ft.Text(message["text"], size=14),
                    ],
                    spacing=2,
                ),
                bgcolor=ft.colors.GREEN_100 if is_me else ft.colors.GREY_100,
                border_radius=10,
                padding=10,
                max_width=300,
            )
            chat.controls.append(
                ft.Row(
                    [msg_bubble],
                    alignment=(
                        ft.MainAxisAlignment.END
                        if is_me
                        else ft.MainAxisAlignment.START
                    ),
                )
            )
        elif message["type"] == "system":
            chat.controls.append(
                ft.Container(
                    content=ft.Text(
                        message["text"], size=12, italic=True, color=ft.colors.GREY_600
                    ),
                    alignment=ft.alignment.center,
                )
            )
        page.update()

    page.pubsub.subscribe(on_message_received)

    def send_click(e):
        if message_field.value.strip():
            page.pubsub.send_all(
                {
                    "type": "chat",
                    "user": user_name.value,
                    "text": message_field.value.strip(),
                }
            )
            message_field.value = ""
            page.update()

    message_field.on_submit = send_click

    def join_chat(e):
        if not user_name.value.strip():
            user_name.error_text = "Nome Obrigatório!"
            page.update()
            return

        page.clean()
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        page.vertical_alignment = ft.MainAxisAlignment.START

        page.pubsub.send_all(
            {"type": "system", "text": f"--- {user_name.value} entrou no chat ---"}
        )

        page.add(
            ft.AppBar(
                title=ft.Text("Hashzap"),
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.WHITE,
                center_title=True,
            ),
            ft.Container(
                content=chat,
                expand=True,
                bgcolor=ft.colors.BLUE_GREY_50,
                padding=20,
                background_image_src="https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png",
                background_image_fit=ft.ImageFit.COVER,
            ),
            ft.Container(
                content=ft.Row(
                    [
                        message_field,
                        ft.IconButton(
                            "send",
                            on_click=send_click,
                            icon_color=ft.colors.PRIMARY,
                        ),
                    ]
                ),
                padding=10,
                bgcolor=ft.colors.WHITE,
            ),
        )
        page.update()

    # Login Screen
    login_screen = ft.Container(
        expand=True,
        content=ft.Column(
            [
                ft.Icon("chat", size=50, color=ft.colors.PRIMARY),
                ft.Text("Hashzap", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Entrar na conversa", color=ft.colors.GREY_600),
                user_name,
                ft.FilledButton(
                    "Entrar",
                    on_click=join_chat,
                    width=200,
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.PRIMARY, color=ft.colors.WHITE
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        bgcolor=ft.colors.BLUE_GREY_50,
    )

    page.add(login_screen)


if __name__ == "__main__":
    logger.info(f"Iniciando app Flet na porta {Config.FLET_PORT}...")
    ft.app(target=main, port=Config.FLET_PORT)
