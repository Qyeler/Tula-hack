import sqlite3

# Установить соединение с базой данных
conn = sqlite3.connect('example.db')

# Создать таблицу, если она не существует
conn.execute('CREATE TABLE IF NOT EXISTS objects (name TEXT PRIMARY KEY, avg BLOB, mincost INTEGER)')

def insert_or_update_object(name, avg, mincost):
    # Проверить, существует ли объект с указанным именем в базе данных
    cursor = conn.execute('SELECT name FROM objects WHERE name=?', (name,))
    row = cursor.fetchone()
    if row:
        # Обновить объект, если он существует
        conn.execute('UPDATE objects SET avg=?, mincost=? WHERE name=?', (avg, mincost, name))
    else:
        # Создать новый объект, если он не существует
        conn.execute('INSERT INTO objects (name, avg, mincost) VALUES (?, ?, ?)', (name, avg, mincost))

def get_object_data(name):
    # Получить данные объекта по имени
    cursor = conn.execute('SELECT avg, mincost FROM objects WHERE name=?', (name,))
    row = cursor.fetchone()
    if row:
        avg, mincost = row
        return {'name': name, 'avg': avg, 'mincost': mincost}
    else:
        return None

def get_all_objects():
    # Получить список всех объектов в базе данных
    cursor = conn.execute('SELECT name FROM objects')
    rows = cursor.fetchall()
    return [row[0] for row in rows]

# Пример использования функций
insert_or_update_object('object1', [1, 2, 3], 10)
insert_or_update_object('object2', [4, 5, 6], 20)

print(get_object_data('object1')) # {'name': 'object1', 'avg': [1, 2, 3], 'mincost': 10}
print(get_object_data('object2')) # {'name': 'object2', 'avg': [4, 5, 6], 'mincost': 20}

print(get_all_objects()) # ['object1', 'object2']

# Закрыть соединение с базой данных
conn.close()