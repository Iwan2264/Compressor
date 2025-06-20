import flet as ft  # type: ignore
from services.pdf_service import compress_pdf
import os
import subprocess

def get_unique_filename(filepath):
    base, ext = os.path.splitext(filepath)
    counter = 1
    new_filepath = filepath

    while os.path.exists(new_filepath):
        new_filepath = f"{base}({counter}){ext}"
        counter += 1

    return new_filepath

def pdf_page(page: ft.Page):
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    selected_file = None
    status = ft.Text("", color="green", size=16)
    selected_quality = ft.Text("📺 Selected: Printer (Medium Compression)", size=14)

    quality_value = "printer"  # Default

    def set_quality(q):
        nonlocal quality_value
        quality_value = q
        quality_labels = {
            "screen": "📺 Selected: Screen (Very High Compression)",
            "ebook": "📖 Selected: eBook (High Compression)",
            "printer": "🖨️ Selected: Printer (Medium Compression)",
            "prepress": "🏭 Selected: Prepress (Low Compression)",
        }
        selected_quality.value = quality_labels[q]
        page.update()

    def on_file_selected(e):
        nonlocal selected_file
        if e.files:
            selected_file = e.files[0]
            status.value = f"✅ Selected: {selected_file.name}"
            status.color = "green"
        else:
            selected_file = None
            status.value = "❌ No file selected."
            status.color = "red"
        page.update()

    def handle_compress(e):
        if not selected_file:
            status.value = "❌ Please select a PDF file."
            status.color = "red"
            page.update()
            return

        folder = os.path.dirname(selected_file.path)
        filename = os.path.splitext(selected_file.name)[0]
        initial_output = os.path.join(folder, f"{filename}_compressed.pdf")
        output_path = get_unique_filename(initial_output)

        try:
            compress_pdf(selected_file.path, output_path, quality=quality_value)
            status.value = f"✅ Compressed PDF saved to:\n{output_path}"
            status.color = "green"
            subprocess.Popen(f'explorer /select,"{output_path}"')
        except Exception as ex:
            status.value = f"❌ Compression failed: {ex}"
            status.color = "red"
        page.update()

    file_picker.on_result = on_file_selected

    return ft.Column(
        [
            ft.Text("📄 PDF Compressor", size=28, weight="bold"),
            ft.Text("Reduce PDF size without losing visible quality.", size=16),
            
            ft.Row([
                ft.ElevatedButton("📺 Screen", on_click=lambda e: set_quality("screen")),
                ft.ElevatedButton("📖 eBook", on_click=lambda e: set_quality("ebook")),
                ft.ElevatedButton("🖨️ Printer", on_click=lambda e: set_quality("printer")),
                ft.ElevatedButton("🏭 Prepress", on_click=lambda e: set_quality("prepress")),
            ], alignment="center"),

            selected_quality,

            ft.ElevatedButton("📁 Pick PDF", on_click=lambda e: file_picker.pick_files(allowed_extensions=["pdf"])),
            ft.ElevatedButton("Compress Now", on_click=handle_compress),
            status,
            ft.ElevatedButton("⬅️ Back", on_click=lambda e: page.go("/"))
        ],
        alignment="center",
        horizontal_alignment="center"
    )
