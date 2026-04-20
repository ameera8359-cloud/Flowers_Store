import sqlite3

conn = sqlite3.connect('flowers_store.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS Flowers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    color TEXT,
    FOREIGN KEY(category_id) REFERENCES Categories(id)
)''')

c.executemany('INSERT INTO Categories (name, description) VALUES (?, ?)', [
    ('Bouquets', 'ชุดดอกไม้จัดพร้อมสำหรับมอบเป็นของขวัญ'),
    ('Roses', 'ดอกกุหลาบหลากสีสำหรับโอกาสต่างๆ'),
    ('Indoor Plants', 'ต้นไม้ในร่มสำหรับตกแต่งภายในบ้าน')
])

c.executemany('INSERT INTO Flowers (name, category_id, price, stock, color) VALUES (?, ?, ?, ?, ?)', [
    ('Rose Bouquet', 1, 799.0, 10, 'Red'),
    ('Pink Roses', 2, 650.0, 8, 'Pink'),
    ('Sunflower Mix', 1, 420.0, 5, 'Yellow'),
    ('Aloe Vera', 3, 220.0, 12, 'Green'),
    ('Orchid Pot', 3, 520.0, 6, 'Purple')
])

conn.commit()
conn.close()
print('flowers_store.db created successfully')
