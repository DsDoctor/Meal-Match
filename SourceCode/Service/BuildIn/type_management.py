from Config.config import BASE_DIR
import os
import sqlite3
import pandas as pd
from Utils.get_time import time_now


def type_to_db(file, table):
    db = sqlite3.connect(os.path.join(BASE_DIR, 'DAO/DataBase/database.db'))
    cur = db.cursor()
    with open(os.path.join(BASE_DIR, file), 'r') as f:
        types = [line.strip() for line in f.readlines()]
        for t in types:
            sql = f"INSERT INTO {table} (name) VALUES ('{t}')"
            cur.execute(sql)
            db.commit()
    db.close()


def ing_to_db():
    db = sqlite3.connect(os.path.join(BASE_DIR, 'DAO/DataBase/database.db'))
    cur = db.cursor()
    data = pd.read_excel(os.path.join(BASE_DIR, 'DAO/data/ingredients.xlsx'))
    for i in data.index:
        name, t = data['name'][i].strip(), data['type'][i]
        sql = f"SELECT id from ing_type WHERE name = '{t}'"
        t_id = cur.execute(sql).fetchone()
        if t_id:
            sql = f"INSERT INTO ingredients (name) VALUES ('{name}')"
            cur.execute(sql)
            ing_id = cur.lastrowid
            sql = f"INSERT INTO relation_ing_type (ingredient, type) VALUES ('{ing_id}', '{t_id[0]}')"
            cur.execute(sql)
            db.commit()
        else:
            print(i, name)
    db.close()


def rec_to_db():
    db = sqlite3.connect(os.path.join(BASE_DIR, 'DAO/DataBase/database.db'))
    cur = db.cursor()
    data = pd.read_excel(os.path.join(BASE_DIR, 'DAO/data/recipes.xlsx'))
    for i in data.index:
        title = data['title'][i]
        sql = f"SELECT * from ScrapyData WHERE title = '{title}'"
        recipe = cur.execute(sql).fetchone()
        steps = recipe[4]
        img_link = recipe[5]
        time = time_now()
        author = 1
        cook_time = recipe[3]
        describe = recipe[-1]

        sql = f"INSERT INTO recipes (title, steps, img_link, update_time, author, cook_time, describe) " \
              f"""VALUES ('{title}', '{steps}', '{img_link}', '{time}', '{author}', '{cook_time}', "{describe}")"""
        cur.execute(sql)
        r_id = cur.lastrowid

        for r_type in data['type'][i].split(' '):
            sql = f"SELECT id from rec_type WHERE name = '{r_type}'"
            t_id = cur.execute(sql).fetchone()
            if t_id:
                sql = f"INSERT INTO relation_rec_type (r_id, t_id) VALUES ('{r_id}', '{t_id[0]}')"
                cur.execute(sql)

        for ing in data['ingredients'][i].split(', '):
            sql = f"SELECT id from ingredients WHERE name = '{ing.strip()}'"
            ing_id = cur.execute(sql).fetchone()
            if ing_id:
                sql = f"INSERT INTO rec_ing (recipe, ingredient) VALUES ('{r_id}', '{ing_id[0]}')"
                cur.execute(sql)
            else:
                print(i, ing)
        db.commit()
    db.close()


if __name__ == '__main__':
    # type_to_db('DAO/data/ing_type.txt', 'ing_type')
    type_to_db('DAO/data/recipe_type.txt', 'rec_type')
    # ing_to_db()
    # rec_to_db()
    pass
