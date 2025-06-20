import flet as ft  # type: ignore

from ui.home_page import home_page as HomePage
from ui.file_compressor import file_compressor_page as FileCompressorPage
from ui.compress_page import compress_page as CompressPage
from ui.decompress_page import decompress_page as DecompressPage
from ui.image_page import image_page as ImagePage
from ui.pdf_page import pdf_page as PDFPage

def main(page: ft.Page):
    page.title = "UniversalCompressor"
    page.theme_mode = "Dark"

    def route_change(e):
        page.views.clear()

        routes = {
            "/": HomePage,
            "/compress": CompressPage,
            "/decompress": DecompressPage,
            "/file-compressor": FileCompressorPage,
            "/image": ImagePage,
            "/pdf": PDFPage,
        }

        route_handler = routes.get(page.route)
        if route_handler:
            page.views.append(ft.View(page.route, [route_handler(page)]))
        else:
            page.views.append(ft.View("/", [HomePage(page)]))  # fallback

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
