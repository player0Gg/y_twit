from model.user import User
from sqlalchemy.future import select
from sqlalchemy import or_


async def get_unicom(form, db):
    query = select(User).where(or_(User.email == form.email, User.username == form.username))
    result = await db.execute(query)
    user = result.scalars().first()
    
    if user is None:
        return None
    
    return user