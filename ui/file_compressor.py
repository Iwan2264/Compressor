import flet as ft  # type: ignore

def file_compressor_page(page: ft.Page):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("🗜️ File Compressor", size=28, weight="bold"),
                ft.Text("What would you like to do?", size=18),

                ft.ElevatedButton("🗜️ Compress Files", on_click=lambda e: page.go("/compress")),
                ft.Text("Bundle multiple files into one archive (ZIP, TAR.GZ, 7Z)", size=12),

                ft.ElevatedButton("📤 Decompress Files", on_click=lambda e: page.go("/decompress")),
                ft.Text("Extract files from a compressed archive", size=12),

                ft.ElevatedButton("⬅️ Back to Home", on_click=lambda e: page.go("/")),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10
        ),
        alignment=ft.alignment.center,
        expand=True
    )
