from model.user import User
from sqlalchemy.future import select
from sqlalchemy import update, delete
from router.login import get_password_hash

async def get_user_by_id(current_user, db):
    query = select(User).where(User.id == current_user)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def create_user(form, db):
    user = User(
        username=form.username,
        email=form.email,
        password=get_password_hash(form.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(form, current_user, db):
    query = update(User).where(User.id == current_user).values(
        username=form.username,
        email=form.email,
        password=get_password_hash(form.password)
    )
    result = await db.execute(query)
    await db.commit()
    
    if result.rowcount == 0:
        return None
    
    return await get_user_by_id(current_user, db)

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