from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import update
from sqlalchemy.future import select
from model.user import User
from func.images import create_image_url, get_user_avatar
from utils.unicom import check_fr, is_friend


async def add_user_subs_func(subs: dict, db):
    username = subs.username
    fr_username = subs.subs.username

    # Получаем текущего пользователя
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user:
        return {"error": "Пользователь не найден"}

    # Получаем целевого пользователя
    fr_result = await db.execute(select(User).where(User.username == fr_username))
    fr_user = fr_result.scalar_one_or_none()
    if not fr_user:
        return {"error": "Друг не найден"}

    # Текущий список подписок
    current_subs = user.subs or []

    # Собираем информацию о друге
    friend = jsonable_encoder(subs.subs)
    friend["avatar_url"] = await create_image_url("ava", avatar=await get_user_avatar(fr_username, db))
    friend["display_name"] = fr_user.display_name if fr_user.display_name else fr_username

    # Проверка: уже добавлен?
    if await check_fr(current_subs, friend, username, fr_username):
        return {"error": "Уже есть в друзьях"}

    # Добавляем
    current_subs.append(friend)

    # Обновляем в БД
    await db.execute(
        update(User).where(User.username == username).values(subs=current_subs)
    )

    # Проверка на взаимную дружбу
    friend_or_not = await is_friend(fr_user, user)
    if friend_or_not:
        await db.execute(
            update(User).where(User.username==username).values(friends=current_subs)
        )

        # Обновляем friends у второго
        fr_friends = fr_user.friends or []
        if username not in fr_friends:
            fr_friends.append({
                "username": username,
                "avatar_url": await create_image_url("ava", avatar=await get_user_avatar(username, db)),
                "display_name": user.display_name or username
            })

            await db.execute(
                update(User).where(User.username == fr_username).values(friends=fr_friends)
            )

    await db.commit()

    return {
        "message": "Friend created",
        "friend": friend,
        "friend_or_not": friend_or_not
    }



async def delete_user_subs_func(subs, db):
    try:
        # Получаем пользователя
        user_result = await db.execute(
            select(User).where(User.username == subs.username)
        )
        user = user_result.scalar_one_or_none()
       
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
       
        # Проверяем существование друга
        friend_result = await db.execute(
            select(User).where(User.username == subs.subs.username)
        )
        friend_user = friend_result.scalar_one_or_none()
       
        if not friend_user:
            raise HTTPException(status_code=404, detail="Пользователь для удаления не найден")
       
        # Работа со списком подписок
        current_subs = user.subs if user.subs else []
        initial_count_subs = len(current_subs)
       
        # Работа со списком друзей
        current_friends = user.friends if user.friends else []
        initial_count_fr = len(current_friends)
        
        # Удаляем пользователя из списка подписок (исправлено имя переменной)
        updated_subs = [
            sub_item for sub_item in current_subs
            if sub_item.get("username") != subs.subs.username
        ]
        
        # Удаляем пользователя из списка друзей (исправлено имя переменной)
        updated_friends = [
            friend_item for friend_item in current_friends
            if friend_item.get("username") != subs.subs.username
        ]
       
        # Проверяем, был ли пользователь найден хотя бы в одном из списков
        subs_changed = len(updated_subs) != initial_count_subs
        friends_changed = len(updated_friends) != initial_count_fr
        
        if not subs_changed and not friends_changed:
            raise HTTPException(
                status_code=400,
                detail="Указанный пользователь не найден ни в списке подписок, ни в списке друзей"
            )
       
        # Обновляем базу данных только если были изменения
        if subs_changed:
            stmt = update(User).where(User.username == subs.username).values(subs=updated_subs)
            await db.execute(stmt)
            
        if friends_changed:
            stmt = update(User).where(User.username == subs.username).values(friends=updated_friends)
            await db.execute(stmt)
        
        # Проверка на взаимную дружбу
        friend_or_not = await is_friend(friend_user, user)
        if friend_or_not==False:
            # Обновляем friends у второго
            # Удаляем пользователя из списка друзей (исправлено имя переменной)
            current_friends_fr = user.friends if user.friends else []
            updated_friends_fr = [
                friend_item for friend_item in current_friends_fr
                if friend_item.get("username") != subs.username
            ]
            initial_count_fr_fr = len(current_friends)
            friends_changed_fr = len(updated_friends_fr) != initial_count_fr_fr

            if friends_changed_fr:
                stmt = update(User).where(User.username == subs.subs.username).values(friends=updated_friends_fr)
                await db.execute(stmt)

        await db.commit()
       
        removed_count_subs = initial_count_subs - len(updated_subs)
        removed_count_friends = initial_count_fr - len(updated_friends)
       
        return {
            "success": True,
            "message": f"Пользователь '{subs.subs.username}' успешно удален",
            "removed_count_subs": removed_count_subs,
            "removed_count_friends": removed_count_friends,  # Исправлено дублирование ключа
            "remaining_subs_count": len(updated_subs),
            "remaining_friends_count": len(updated_friends)
        }
       
    except HTTPException:
        await db.rollback()  # Добавлен rollback для HTTPException
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )
    