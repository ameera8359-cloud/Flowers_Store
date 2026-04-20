{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "01c8567f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Created flowers_store.db with sample data\n"
     ]
    }
   ],
   "source": [
    "import sqlite3\n",
    "\n",
    "connection = sqlite3.connect('flowers_store.db')\n",
    "cursor = connection.cursor()\n",
    "\n",
    "cursor.execute('''CREATE TABLE IF NOT EXISTS Categories (\n",
    "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
    "    name TEXT NOT NULL,\n",
    "    description TEXT\n",
    ")''')\n",
    "\n",
    "cursor.execute('''CREATE TABLE IF NOT EXISTS Flowers (\n",
    "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
    "    name TEXT NOT NULL,\n",
    "    category_id INTEGER NOT NULL,\n",
    "    price REAL NOT NULL,\n",
    "    stock INTEGER NOT NULL,\n",
    "    color TEXT,\n",
    "    FOREIGN KEY(category_id) REFERENCES Categories(id)\n",
    ")''')\n",
    "\n",
    "cursor.executemany('INSERT INTO Categories (name, description) VALUES (?, ?)', [\n",
    "    ('Bouquets', 'ชุดดอกไม้จัดพร้อมสำหรับมอบเป็นของขวัญ'),\n",
    "    ('Roses', 'ดอกกุหลาบหลากสีสำหรับโอกาสต่างๆ'),\n",
    "    ('Indoor Plants', 'ต้นไม้ในร่มสำหรับตกแต่งภายในบ้าน')\n",
    "])\n",
    "\n",
    "cursor.executemany('INSERT INTO Flowers (name, category_id, price, stock, color) VALUES (?, ?, ?, ?, ?)', [\n",
    "    ('Rose Bouquet', 1, 799.0, 10, 'Red'),\n",
    "    ('Pink Roses', 2, 650.0, 8, 'Pink'),\n",
    "    ('Sunflower Mix', 1, 420.0, 5, 'Yellow'),\n",
    "    ('Aloe Vera', 3, 220.0, 12, 'Green'),\n",
    "    ('Orchid Pot', 3, 520.0, 6, 'Purple')\n",
    "])\n",
    "\n",
    "connection.commit()\n",
    "connection.close()\n",
    "print('Created flowers_store.db with sample data')\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.14.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
