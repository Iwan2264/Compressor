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

    selected_files = []  # Changed from selected_file = None
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
        nonlocal selected_files
        if e.files:
            selected_files = e.files  # 🆕 Store list of selected files
            names = ", ".join([f.name for f in selected_files])
            status.value = f"✅ Selected: {names}"
            status.color = "green"
        else:
            selected_files = []
            status.value = "❌ No files selected."
            status.color = "red"
        page.update()

    def handle_compress(e):
        if not selected_files:
            status.value = "❌ Please select one or more PDF files."
            status.color = "red"
            page.update()
            return

        failed = []  

        for file in selected_files:
            folder = os.path.dirname(file.path)
            filename = os.path.splitext(file.name)[0]
            initial_output = os.path.join(folder, f"{filename}_compressed.pdf")
            output_path = get_unique_filename(initial_output)

            try:
                compress_pdf(file.path, output_path, quality=quality_value)
            except Exception:
                failed.append(file.name)

        if failed:
            status.value = f"⚠️ Some files failed: {', '.join(failed)}"
            status.color = "red"
        else:
            status.value = "✅ All PDFs compressed successfully!"
            status.color = "green"
            # Optionally open the folder after compressing
            subprocess.Popen(f'explorer "{os.path.dirname(selected_files[0].path)}"')

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

            ft.ElevatedButton("📁 Pick PDFs", on_click=lambda e: file_picker.pick_files(allowed_extensions=["pdf"], allow_multiple=True)),
            ft.ElevatedButton("Compress Now", on_click=handle_compress),
            status,
            ft.ElevatedButton("⬅️ Back", on_click=lambda e: page.go("/"))
        ],
        alignment="center",
        horizontal_alignment="center"
    )
