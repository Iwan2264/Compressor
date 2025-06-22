import flet as ft  # type: ignore
from services.image_service import compress_image
import os
import subprocess

def image_page(page: ft.Page):
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    selected_files = []
    status = ft.Text("", color="green", size=16)
    
    quality_slider = ft.Slider(
        min=10,
        max=100,
        divisions=18,  
        label="{value}%",
        value=70,
        width=250, 
        thumb_color="blue", 
        inactive_color="grey"
    )

    def on_files_selected(e):
        nonlocal selected_files
        selected_files = file_picker.result.files
        status.value = f"{len(selected_files)} image(s) selected." if selected_files else "❌ No files selected."
        status.color = "green" if selected_files else "red"
        page.update()

    def handle_compress(e):
        if not selected_files:
            status.value = "❌ Please select image(s) to compress."
            status.color = "red"
            page.update()
            return

        for file in selected_files:
            folder = os.path.dirname(file.path)
            filename, ext = os.path.splitext(file.name)
            compressed_path = get_unique_filename(os.path.join(folder, f"{filename}_compressed{ext}"))
            compress_image(file.path, compressed_path, quality=int(quality_slider.value))
            subprocess.Popen(f'explorer /select,"{compressed_path}"')

        status.value = "✅ Compressed and saved in source folder."
        status.color = "green"
        page.update()

    def get_unique_filename(path):
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = path
        while os.path.exists(new_path):
            new_path = f"{base}({counter}){ext}"
            counter += 1
        return new_path

    file_picker.on_result = on_files_selected

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("📸 Image Compressor", size=28, weight="bold"),
                ft.Text("Select image(s) and adjust quality below:", size=16),
                quality_slider,
                ft.ElevatedButton("📁 Pick Images", on_click=lambda e: file_picker.pick_files(
                    allow_multiple=True, allowed_extensions=["jpg", "jpeg", "png", "webp"])),
                ft.ElevatedButton("Compress Now", on_click=handle_compress),
                status,
                ft.ElevatedButton("⬅️ Back", on_click=lambda e: page.go("/")),
            ],
            alignment="center",
            horizontal_alignment="center"
        ),
        alignment=ft.alignment.center,
        expand=True
    )
