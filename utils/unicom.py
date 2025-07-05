from fastapi import HTTPException
from model.user import User
from sqlalchemy.future import select
from sqlalchemy import or_, update


async def get_unicom(form, db):
    query = select(User).where(or_(User.email == form.email, User.username == form.username))
    result = await db.execute(query)
    user = result.scalars().first()
    
    if user is None:
        return None
    
    return user

async def check_fr(current_friends, friend, username, fr_username):
    check_fr=False
    for i in current_friends:
        if friend==i or username==fr_username:
            check_fr=True
            break

    return check_fr


async def is_friend(user, fr_user):
    # Проверяем оба пользователя на None
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not fr_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Извлекаем только имена из подписок
    user_sub_usernames = [s["username"] for s in (user.subs or [])]
    fr_user_sub_usernames = [s["username"] for s in (fr_user.subs or [])]

    is_friend = (
        fr_user.username in user_sub_usernames and
        user.username in fr_user_sub_usernames
    )

    return is_friend