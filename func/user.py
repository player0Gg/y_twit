from func.images import create_image_url
from model.user import User
from sqlalchemy.future import select
from sqlalchemy import update
from utils.token import get_password_hash
from utils.token import access_token_for_func
from utils.unicom import get_unicom


async def get_all_users_func(username, db):
    # Строим запрос
    if username:
        query = select(User).where(User.username.ilike(f"%{username}%"))
    else:
        query = select(User)

    # Выполняем запрос
    result = await db.execute(query)
    users = result.scalars().all()

    # Возвращаем список словарей
    return [
        {
            "username": user.username,
            "avatar_url": await create_image_url("ava", user.avatar)
        }
        for user in users
    ]

async def get_user_by_username(username, db):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if user is None:
        return None

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar_url": await create_image_url("ava", avatar=user.avatar),
        "banner_url": await create_image_url("banner",banner=user.banner),
        "display_name": user.display_name,
        "role": user.role,
        "friends": user.friends,
        "subs": user.subs,
        "about_me": user.about_me
    }


async def create_user(form, db):
    unicom = await get_unicom(form, db)
    if unicom is None:
        access_token = await access_token_for_func(form, db)
        user = User(
                username=form.username,
                email=form.email,
                password=get_password_hash(form.password),
                token=access_token['access_token'],
                avatar='default_avatar.jpg',
                banner='default_banner.jpg',
                role=0
            )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return {"message":"User be create success"}
    else:
        return {"error":"Пользователь c таким логином или почтой уже существует"}


async def update_user(form, db):
    # access_token= await access_token_for_func(form, db)
    query = update(User).where(User.username == form.username).values(
        # email=form.email,
        display_name=form.display_name,
        about_me=form.about_me
    )
    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount == 0:
        return None
    
    return await get_user_by_username(form.username, db)

# async def delete_user(user_id, db):
    # query = delete(User).where(User.id == user_id)
    # result = await db.execute(query)ЁЁ
    # await db.commit()
    # 
    # if result.rowcount == 0:
        # return None
    # 
    # return {"message": "User deleted successfully"}