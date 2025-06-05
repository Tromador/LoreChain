# lc_input_interface/input_providers/manual.py

from .base import InputProvider

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB max file size
ALLOWED_EXTENSIONS = ('.txt', '.jsonl', '.md')

class ManualInputProvider(InputProvider):
    def __init__(self, text_input, file_input):
        self.text_input = text_input
        self.file_input = file_input

    def get_next_chunk(self):
        # Prioritise text input if provided
        if self.text_input:
            cleaned_text = self.text_input.strip()
            if not cleaned_text:
                return "Error: Text input is empty."
            if len(cleaned_text.encode('utf-8')) > MAX_FILE_SIZE:
                return "Error: Text input exceeds maximum size (1MB)."
            return cleaned_text

        # If file input, process allowed extensions
        if self.file_input:
            if self.file_input.filename.endswith(ALLOWED_EXTENSIONS):
                try:
                    content = self.file_input.read()
                    if len(content) > MAX_FILE_SIZE:
                        return "Error: Uploaded file exceeds maximum size (1MB)."
                    content_decoded = content.decode('utf-8').strip()
                    if not content_decoded:
                        return "Error: Uploaded file is empty."
                    if self.file_input.filename.endswith('.jsonl'):
                        lines = [line.strip() for line in content_decoded.splitlines() if line.strip()]
                        return '\n'.join(lines)
                    else:
                        return content_decoded
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            else:
                return f"Error: Unsupported file type. Only {ALLOWED_EXTENSIONS} allowed."

        return "Error: No input provided."
