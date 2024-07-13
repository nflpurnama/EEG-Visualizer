from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

def createTempEdfFile(file: FileStorage):
    