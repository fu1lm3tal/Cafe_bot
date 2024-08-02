import sqlite3 as sq


async def db_connection() -> None:
    db = sq.connect('cafe.db')
    cur = db.cursor()
    db.commit()


async def cmd_start_id(user_id, user_name, user_email, user_age):
    db = sq.connect('cafe.db')
    cur = db.cursor()

    user = cur.execute("SELECT * FROM user WHERE tg_id == ?", (user_id,)).fetchone()
    if not user:
        name = user_name
        email = user_email
        age = user_age

        cur.execute("INSERT INTO user (tg_id, name, email, age) VALUES (?, ?, ?, ?)",
                    (user_id, name, email, age))
        db.commit()


async def get_id(user_id):
    db = sq.connect('cafe.db')
    cur = db.cursor()

    user = cur.execute("SELECT tg_id FROM user WHERE (tg_id) == ?", (user_id,)).fetchone()
    if user:
        return True
    else:
        return False


async def get_category():
    db = sq.connect('cafe.db')
    cur = db.cursor()

    category = cur.execute("SELECT category FROM menu").fetchall()
    categories = [cat[0] for cat in category]
    result = " ".join(categories)
    array = result.split()

    return array


async def get_items(name):
    db = sq.connect('cafe.db')
    cur = db.cursor()

    items = cur.execute("SELECT items.name, items.price FROM items JOIN menu ON menu.id = items.item_id WHERE (category) == ?", (name,)).fetchall()
    result = [f"{item[0]}: {item[1]} руб." for item in items]
    db.close()

    return result
