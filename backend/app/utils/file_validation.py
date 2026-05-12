ALLOWED_EXTENSIONS = [".pdf"]


def validate_extension(filename: str):
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)
