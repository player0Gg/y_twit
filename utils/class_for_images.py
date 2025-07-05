import io
from fastapi import HTTPException
from PIL import Image
import os
from datetime import datetime

async def save_image(file, upload_dir, max_width,
                     max_height, quality) -> str:
        
        UPLOAD_DIR = f"images/{upload_dir}"
        if not file.filename.lower().endswith(("png","jpg","jpeg","jfif","webp","tiff","gif")):
            raise HTTPException(status_code=400, detail="You can send only fotos with 'png', 'jpg', 'svg', 'webp' format.")

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        _, file_extension = os.path.splitext(file.filename)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{timestamp}{file_extension}"
        image_path = os.path.join(UPLOAD_DIR, unique_filename)

        try:
            contents=await file.read() 
            image = Image.open(file.file)

            # Создаем объект изображения из байтов
            image = Image.open(io.BytesIO(contents))

            # Изменяем размер
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Определяем формат для сохранения
            save_format = "JPEG" if file_extension.lower() in [".jpg", ".jpeg", ".jfif"] else image.format
            
            # Сохраняем файл
            image.save(image_path, format=save_format, quality=quality)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"For save images need this format : {str(e)}")

        return unique_filename