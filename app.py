import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'flowers_store.db')


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM Categories ORDER BY name').fetchall()
    conn.close()
    return categories


def get_flowers():
    conn = get_db_connection()
    flowers = conn.execute(
        'SELECT F.*, C.name AS category_name FROM Flowers F JOIN Categories C ON F.category_id = C.id ORDER BY F.name'
    ).fetchall()
    conn.close()
    return flowers


def get_category(category_id):
    conn = get_db_connection()
    category = conn.execute('SELECT * FROM Categories WHERE id = ?', (category_id,)).fetchone()
    conn.close()
    return category


def get_flower(flower_id):
    conn = get_db_connection()
    flower = conn.execute('SELECT * FROM Flowers WHERE id = ?', (flower_id,)).fetchone()
    conn.close()
    return flower


@app.route('/')
def home():
    return render_template('index.html', view='home', flowers=get_flowers(), categories=get_categories())


@app.route('/categories')
def categories():
    return render_template('index.html', view='categories', categories=get_categories())


@app.route('/flowers/add', methods=['GET', 'POST'])
def add_flower():
    categories = get_categories()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category_id = request.form.get('category_id')
        price = request.form.get('price', '0').strip()
        stock = request.form.get('stock', '0').strip()
        color = request.form.get('color', '').strip()
        image_url = request.form.get('image_url', '').strip()

        if not name or not category_id:
            abort(400)

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO Flowers (name, category_id, price, stock, color, image_url) VALUES (?, ?, ?, ?, ?, ?)',
            (name, int(category_id), float(price) if price else 0.0, int(stock) if stock else 0, color, image_url),
        )
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    return render_template(
        'index.html',
        view='flower_form',
        form_action=url_for('add_flower'),
        title='Add New Flower',
        button_label='Create Flower',
        categories=categories,
        flower=None,
    )


@app.route('/flowers/edit/<int:flower_id>', methods=['GET', 'POST'])
def edit_flower(flower_id):
    flower = get_flower(flower_id)
    if flower is None:
        abort(404)

    categories = get_categories()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category_id = request.form.get('category_id')
        price = request.form.get('price', '0').strip()
        stock = request.form.get('stock', '0').strip()
        color = request.form.get('color', '').strip()
        image_url = request.form.get('image_url', '').strip()

        if not name or not category_id:
            abort(400)

        conn = get_db_connection()
        conn.execute(
            'UPDATE Flowers SET name = ?, category_id = ?, price = ?, stock = ?, color = ?, image_url = ? WHERE id = ?',
            (name, int(category_id), float(price) if price else 0.0, int(stock) if stock else 0, color, image_url, flower_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    return render_template(
        'index.html',
        view='flower_form',
        form_action=url_for('edit_flower', flower_id=flower_id),
        title='Edit Flower',
        button_label='Update Flower',
        categories=categories,
        flower=flower,
    )


@app.route('/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Flowers WHERE id = ?', (flower_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not name:
            abort(400)

        conn = get_db_connection()
        conn.execute('INSERT INTO Categories (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        conn.close()
        return redirect(url_for('categories'))

    return render_template(
        'index.html',
        view='category_form',
        form_action=url_for('add_category'),
        title='Add New Category',
        button_label='Create Category',
        category=None,
    )


@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = get_category(category_id)
    if category is None:
        abort(404)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not name:
            abort(400)

        conn = get_db_connection()
        conn.execute('UPDATE Categories SET name = ?, description = ? WHERE id = ?', (name, description, category_id))
        conn.commit()
        conn.close()
        return redirect(url_for('categories'))

    return render_template(
        'index.html',
        view='category_form',
        form_action=url_for('edit_category', category_id=category_id),
        title='Edit Category',
        button_label='Update Category',
        category=category,
    )


@app.route('/categories/delete/<int:category_id>')
def delete_category(category_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('categories'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
