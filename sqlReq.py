import sqlite3

conn = sqlite3.connect('items.db')

conn.execute('CREATE TABLE IF NOT EXISTS objects (name TEXT PRIMARY KEY, avg TEXT, mincost INTEGER)')

def insert_or_update_object(name, avg, mincost):
    cursor = conn.execute('SELECT name FROM objects WHERE name=?', (name,))
    row = cursor.fetchone()
    if row:
        conn.execute('UPDATE objects SET avg=?, mincost=? WHERE name=?', (avg, mincost, name))
    else:
        conn.execute('INSERT INTO objects (name, avg, mincost) VALUES (?, ?, ?)', (name, avg, mincost))

def get_object_data(name):
    cursor = conn.execute('SELECT avg, mincost FROM objects WHERE name=?', (name,))
    row = cursor.fetchone()
    if row:
        avg, mincost = row
        return {'name': name, 'avg': avg, 'mincost': mincost}
    else:
        return None

def get_all_objects():
    cursor = conn.execute('SELECT name FROM objects')
    rows = cursor.fetchall()
    return [row[0] for row in rows]
'''
insert_or_update_object('object1', "1,2,3", 10)
insert_or_update_object('object2', "4,5,6", 20)

print(get_object_data('object1')) # {'name': 'object1', 'avg': [1, 2, 3], 'mincost': 10}
print(get_object_data('object2')) # {'name': 'object2', 'avg': [4, 5, 6], 'mincost': 20}

print(get_all_objects()) # ['object1', 'object2']

conn.close()
'''