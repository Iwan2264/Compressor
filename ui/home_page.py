import flet as ft  # type: ignore
from datetime import datetime

def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

def home_page(page: ft.Page):
    greeting = get_greeting()
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"{greeting}", size=26, weight="bold"),
                ft.Text("👋 Welcome to UniversalCompressor", size=22),
                ft.Text("Choose a tool below:", size=18),

                ft.ElevatedButton("📸 Image Compressor", on_click=lambda e: page.go("/image")),
                ft.ElevatedButton("📄 PDF Compressor", on_click=lambda e: page.go("/pdf")),
                
                ft.ElevatedButton("🗜️ File Compressor", on_click=lambda e: page.go("/file-compressor")),
            ],
            alignment="center",
            horizontal_alignment="center",
        ),
        alignment=ft.alignment.center,
        expand=True,
    )
