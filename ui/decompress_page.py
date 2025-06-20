import flet as ft  # type: ignore
from services.zip_service import decompress_file, get_full_extension
import os
import subprocess
from pathlib import Path

def get_unique_folder(base_path):
    """Append counter to folder name if it exists already."""
    counter = 1
    unique_path = Path(base_path)
    while unique_path.exists():
        unique_path = Path(f"{base_path}({counter})")
        counter += 1
    return str(unique_path)

def decompress_page(page: ft.Page):
    status = ft.Text("", color="green", size=16)
    file_picker = ft.FilePicker()
    selected_file = None

    page.overlay.append(file_picker)

    def on_file_selected(e):
        nonlocal selected_file
        selected_file = file_picker.result.files[0] if file_picker.result.files else None

        if selected_file:
            status.value = f"✅ Selected: {selected_file.path}"
            status.color = "green"
        else:
            status.value = "❌ No file selected."
            status.color = "red"
        page.update()

    def handle_decompress(e):
        if not selected_file:
            status.value = "❌ Please select a compressed file."
            status.color = "red"
            page.update()
            return

        try:
            ext = get_full_extension(selected_file.path).lower()
            supported = [".zip", ".tar", ".tar.gz", ".7z", ".rar"]
            if ext not in supported:
                status.value = f"❌ Unsupported format: {ext}"
                status.color = "red"
                page.update()
                return

            folder = Path(selected_file.path).parent
            stem = Path(selected_file.path).stem
            if ext == ".tar.gz":
                stem = Path(stem).stem  # Strip `.tar` too

            base_output_dir = folder / f"{stem}_decompressed"
            output_dir = get_unique_folder(base_output_dir)

            decompress_file(selected_file.path, output_dir)

            status.value = f"✅ Extracted to: {output_dir}"
            status.color = "green"
            subprocess.Popen(f'explorer "{output_dir}"')

        except Exception as ex:
            status.value = f"❌ Decompression failed: {ex}"
            status.color = "red"
        page.update()

    file_picker.on_result = on_file_selected

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("📂 Decompress Files", size=24, weight="bold"),
                ft.ElevatedButton("📁 Pick Compressed File", on_click=lambda e: file_picker.pick_files(allow_multiple=False)),
                ft.ElevatedButton("Decompress Now", on_click=handle_decompress),
                status,
                ft.ElevatedButton("⬅️ Back", on_click=lambda e: page.go("/"))
            ],
            alignment="center",
            horizontal_alignment="center"
        ),
        alignment=ft.alignment.center,
        expand=True
    )
