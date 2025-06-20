import os
import zipfile
import tarfile
import subprocess

SEVEN_ZIP_EXE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin", "7z.exe"))

if not os.path.exists(SEVEN_ZIP_EXE):
    raise FileNotFoundError(f"7z.exe not found at: {SEVEN_ZIP_EXE}")


def compress_files(file_paths, output_path, format_type="zip"):
    format_type = format_type.lower()
    if not isinstance(file_paths, list) or not file_paths:
        raise ValueError("file_paths must be a non-empty list")

    if format_type == "zip":
        _compress_zip(file_paths, output_path)
    elif format_type == "tar.gz":
        _compress_tar(file_paths, output_path, gzipped=True)
    elif format_type == "tar":
        _compress_tar(file_paths, output_path, gzipped=False)
    elif format_type == "7z":
        _compress_7z(file_paths, output_path)
    else:
        raise ValueError("Unsupported format")


def _compress_zip(file_paths, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path in file_paths:
            if os.path.isdir(path):
                _add_directory_to_zip(zipf, path)
            else:
                arcname = os.path.basename(path)
                zipf.write(path, arcname)


def _add_directory_to_zip(zipf, dir_path):
    for root, dirs, files in os.walk(dir_path):
        if not files and not dirs:
            # Add empty folder
            zip_info = zipfile.ZipInfo(os.path.relpath(root, os.path.dirname(dir_path)) + "/")
            zipf.writestr(zip_info, "")
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, os.path.dirname(dir_path))
            zipf.write(full_path, arcname)


def _compress_tar(file_paths, output_path, gzipped=False):
    mode = "w:gz" if gzipped else "w"
    with tarfile.open(output_path, mode) as tar:
        for path in file_paths:
            arcname = os.path.basename(path.rstrip(os.sep))
            tar.add(path, arcname=arcname)


def _compress_7z(file_paths, output_path):
    normalized_paths = [os.path.normpath(p) for p in file_paths]
    result = subprocess.run([SEVEN_ZIP_EXE, "a", output_path] + normalized_paths, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"7z compression failed:\n{result.stderr}")


def get_full_extension(file_path):
    base, ext = os.path.splitext(file_path)
    if ext == ".gz" and base.endswith(".tar"):
        return ".tar.gz"
    return ext


def is_within_directory(directory, target):
    abs_dir = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    return os.path.commonpath([abs_dir]) == os.path.commonpath([abs_dir, abs_target])


def safe_extract_tar(tar, path="."):
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not is_within_directory(path, member_path):
            raise ValueError("Attempted Path Traversal in Tar File")
    tar.extractall(path)


def decompress_file(file_path, output_dir):
    ext = get_full_extension(file_path).lower()

    if ext == ".zip":
        with zipfile.ZipFile(file_path, 'r') as zipf:
            zipf.extractall(output_dir)

    elif ext in [".tar.gz", ".tar"]:
        with tarfile.open(file_path, 'r:*') as tar:
            safe_extract_tar(tar, output_dir)

    elif ext in [".7z", ".rar"]:
        result = subprocess.run(
            [SEVEN_ZIP_EXE, "x", file_path, f"-o{output_dir}", "-y"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"7z decompression failed:\n{result.stderr}")

    elif ext == ".gz":
        raise ValueError("GZ format is not supported standalone. Use TAR.GZ instead.")

    else:
        raise ValueError("Unsupported format for decompression")
