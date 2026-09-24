import os
import uuid
from werkzeug.utils import secure_filename
from config.config import Config
from PIL import Image

class ImageService:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ImageService.ALLOWED_EXTENSIONS

    @staticmethod
    def save_image(file, folder_type='lost'):
        if not file or not ImageService.allowed_file(file.filename):
            return None

        # generate secure unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        filename = secure_filename(unique_filename)
        
        folder_path = os.path.join(Config.UPLOAD_FOLDER, folder_type)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, filename)
        
        # Save and potentially compress/resize if needed. For now just save.
        try:
            image = Image.open(file)
            image.thumbnail((800, 800)) # Simple resize to keep sizes manageable
            image.save(file_path)
            return filename
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
