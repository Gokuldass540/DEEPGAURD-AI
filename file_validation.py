import os
import uuid
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename, allowed_types=None):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if allowed_types:
        return ext in allowed_types
    return ext in Config.ALLOWED_EXTENSIONS

def get_media_type(filename):
    if not filename or '.' not in filename:
        return 'Unknown'
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in Config.ALLOWED_IMAGE_EXTENSIONS:
        return 'Image'
    elif ext in Config.ALLOWED_VIDEO_EXTENSIONS:
        return 'Video'
    return 'Unknown'

def save_upload(file_obj, upload_folder=Config.UPLOAD_FOLDER):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)

    original_name = secure_filename(file_obj.filename)
    ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else ''
    unique_filename = f"{uuid.uuid4().hex[:12]}_{original_name}"
    
    file_path = os.path.join(upload_folder, unique_filename)
    file_obj.save(file_path)
    
    return unique_filename, original_name, file_path
