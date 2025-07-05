from utils.class_for_images import save_image
# from fastapi.responses import FileResponse

UPLOAD_DIR = "images/avatars"


async def save_avatar(file,  upload_dir: str='avatars', max_width: int=1024,
                     max_height: int=1024, quality: int=85) -> str:
    return await save_image(file, upload_dir, max_width=max_width,
                      max_height=max_height, quality=quality)


async def save_banner(file,  upload_dir: str='banners', max_width: int=1024,
                     max_height: int=1024, quality: int=85) -> str:
    return await save_image(file, upload_dir, max_width=max_width,
                      max_height=max_height, quality=quality)


async def save_com_image(file,  upload_dir: str='com_image', max_width: int=1024,
                     max_height: int=1024, quality: int=85) -> str:
    return await save_image(file, upload_dir, max_width=max_width,
                      max_height=max_height, quality=quality)

async def create_image_url(ava_or_banner, avatar=None, banner=None):
    if ava_or_banner=="ava":
        if avatar!=None:
            avatar_url = f"/api/image/avatars/{avatar}"
        else:
            avatar_url = "/api/image/avatars/default_avatar.jpg"
        return avatar_url
    elif ava_or_banner=="banner":
        if banner!=None:
            banner_url = f"/api/image/banners/{banner}"
        else:
            banner_url = "/api/image/banners/default_banner.jpg"

        return banner_url


async def get_user_avatar(username: str, db):
    """Получение аватара пользователя"""
    from model.user import User
    from sqlalchemy.future import select
    
    query = select(User.avatar).where(User.username == username)
    result = await db.execute(query)
    avatar_filename = result.scalar()

    return avatar_filename


# async def list_images():
#     """Получение списка всех изображений"""
#     if not os.path.exists(UPLOAD_DIR):
#         return []
    
#     images = []
#     for filename in os.listdir(UPLOAD_DIR):
#         if filename.lower().endswith(("png", "jpg", "jpeg", "jfif", "webp", "tiff", "gif", "svg")):
#             file_path = os.path.join(UPLOAD_DIR, filename)
#             file_size = os.path.getsize(file_path)
            
#             images.append({
#                 "filename": filename,
#                 "url": f"/api/image/{filename}",
#                 "size": file_size
#             })
    
#     return images