import os
import mimetypes


def get_file_info(file_path):
    size = os.path.getsize(file_path)

    file_type, _ = mimetypes.guess_type(file_path)

    return {
        "file_name": os.path.basename(file_path),
        "file_size": size,
        "file_type": file_type or "Unknown"
    }
