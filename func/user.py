from model.user import User
from sqlalchemy.future import select
from sqlalchemy import update
from utils.token import get_password_hash
from utils.token import access_token_for_func
from utils.unicom import get_unicom


async def get_user_by_username(username, db):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if user is None:
        return None
    
    return user

async def create_user(form, db):
    unicom = await get_unicom(form, db)
    if unicom is None:
        access_token = await access_token_for_func(form, db)
        user = User(
                username=form.username,
                email=form.email,
                password=get_password_hash(form.password),
                token=access_token['access_token']
            )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    else:
        return {"error":"Пользователь c таким логином или почтой уже существует"}


async def update_user(form, current_user, db):
    access_token= await access_token_for_func(form, db)
    query = update(User).where(User.id == current_user.id).values(
        username=form.username,
        email=form.email,
        password=get_password_hash(form.password),
        token=access_token['access_token']
    )
    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount == 0:
        return None
    
    return await get_user_by_username(current_user, db)

# 
# async def delete_user(user_id, db):
    # query = delete(User).where(User.id == user_id)
    # result = await db.execute(query)
    # await db.commit()
    # 
    # if result.rowcount == 0:
        # return None
    # 
    # return {"message": "User deleted successfully"}