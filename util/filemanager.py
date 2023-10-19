from tempfile import NamedTemporaryFile
from werkzeug.datastructures import FileStorage

def createTempEdfFile(file: FileStorage):
    bytes = file.read()

    with NamedTemporaryFile(delete=False, suffix=".edf") as temp_file:
        temp_file.write(bytes)
        temp_file_path = temp_file.name

        return temp_file_path