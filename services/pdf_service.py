import subprocess

def compress_pdf(input_path, output_path, quality="screen"):
    """
    Compress a PDF using Ghostscript.
    
    quality:
        - screen (low quality, smallest size)
        - ebook  (medium quality)
        - printer (good quality)
        - prepress (high quality)
    """
    try:
        subprocess.check_call([
            "gswin64c",  # Change if needed depending on your OS
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{quality}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            input_path
        ])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ghostscript compression failed: {e}")
