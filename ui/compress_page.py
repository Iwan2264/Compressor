import flet as ft  # type: ignore
from services.zip_service import compress_files
import os
import subprocess

TAR_GZ_FORMAT = "tar.gz"
TAR_FORMAT = "tar"

def set_format(fmt, selected_format_ref, status, page, format_label):
    selected_format_ref[0] = fmt
    labels = {
        "zip": "📦 Selected Format: ZIP",
        TAR_GZ_FORMAT: "📦 Selected Format: TAR.GZ",
        TAR_FORMAT: "📦 Selected Format: TAR",
        "7z": "📦 Selected Format: 7Z"
    }
    format_label.value = labels.get(fmt, f"📦 Selected Format: {fmt.upper()}")
    status.value = ""
    status.color = "green"
    page.update()

def handle_compress(selected_files_ref, selected_format_ref, status, page):
    selected_files = selected_files_ref[0]
    selected_format = selected_format_ref[0]

    if not selected_files:
        status.value = "❌ Please select files or a folder to compress."
        status.color = "red"
        page.update()
        return

    folder = os.path.dirname(selected_files[0])
    ext = TAR_GZ_FORMAT if selected_format == TAR_GZ_FORMAT else selected_format
    output_name = f"compressed.{ext}"
    output_path = os.path.join(folder, output_name)

    # Avoid overwrite
    counter = 1
    while os.path.exists(output_path):
        output_name = f"compressed({counter}).{ext}"
        output_path = os.path.join(folder, output_name)
        counter += 1

    try:
        compress_files(selected_files, output_path, selected_format)
        status.value = f"✅ Saved to: {output_path}"
        status.color = "green"
        subprocess.Popen(f'explorer /select,"{output_path}"')
    except Exception as ex:
        status.value = f"❌ Compression failed: {ex}"
        status.color = "red"

    page.update()

def compress_page(page: ft.Page):
    status = ft.Text("", color="green", size=16)
    file_picker = ft.FilePicker()
    folder_picker = ft.FilePicker()
    selected_files_ref = [[]]
    selected_format_ref = ["zip"]

    page.overlay.extend([file_picker, folder_picker])

    format_label = ft.Text("📦 Selected Format: ZIP", size=14)

    def on_files_selected(e):
        if file_picker.result and file_picker.result.files:
            selected_files_ref[0] = [f.path for f in file_picker.result.files]
            status.value = f"✅ {len(selected_files_ref[0])} file(s) selected."
        else:
            selected_files_ref[0] = []
            status.value = "❌ No files selected."
        status.color = "green" if selected_files_ref[0] else "red"
        page.update()

    def on_folder_selected(e):
        if folder_picker.result and folder_picker.result.path:
            selected_files_ref[0] = [folder_picker.result.path]
            status.value = f"📁 Folder selected: {os.path.basename(folder_picker.result.path)}"
        else:
            selected_files_ref[0] = []
            status.value = "❌ No folder selected."
        status.color = "green" if selected_files_ref[0] else "red"
        page.update()

    file_picker.on_result = on_files_selected
    folder_picker.on_result = on_folder_selected

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("🔒 Compress Files or Folder", size=24, weight="bold"),
                ft.Row([
                    ft.ElevatedButton("ZIP", on_click=lambda e: set_format("zip", selected_format_ref, status, page, format_label)),
                    ft.ElevatedButton("TAR.GZ", on_click=lambda e: set_format(TAR_GZ_FORMAT, selected_format_ref, status, page, format_label)),
                    ft.ElevatedButton("TAR", on_click=lambda e: set_format(TAR_FORMAT, selected_format_ref, status, page, format_label)),
                    ft.ElevatedButton("7Z", on_click=lambda e: set_format("7z", selected_format_ref, status, page, format_label)),
                ], alignment="center"),
                format_label,
                ft.Row([
                    ft.ElevatedButton("📄 Pick Files", on_click=lambda e: file_picker.pick_files(allow_multiple=True)),
                    ft.ElevatedButton("📁 Pick Folder", on_click=lambda e: folder_picker.get_directory_path())
                ], alignment="center"),
                ft.ElevatedButton("🗜️ Compress Now", on_click=lambda e: handle_compress(selected_files_ref, selected_format_ref, status, page)),
                status,
                ft.ElevatedButton("⬅️ Back", on_click=lambda e: page.go("/"))
            ],
            alignment="center",
            horizontal_alignment="center"
        ),
        alignment=ft.alignment.center,
        expand=True
    )
