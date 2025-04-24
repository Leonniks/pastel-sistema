from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
import urllib.parse
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta')

WHATSAPP_NUMBER = os.getenv('WHATSAPP_NUMBER', '5511999998888')

def get_db_connection():
    DATABASE_URL = os.getenv('DATABASE_URL',
        'postgresql://juventude:rR7breZTAQ5qEPhzYfmgT0dYQhn5rweS@dpg-d055kj9r0fns73d3dokg-a.oregon-postgres.render.com:5432/pastel'
    )
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

@app.route('/')
def inventory():
    conn = get_db_connection()
    cur = conn.cursor()
    # exemplo de select em order()
    cur.execute('SELECT id, product_name, category, quantity, price FROM inventory ORDER BY product_name')
    produtos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('inventory.html', produtos=produtos)

@app.route('/order', methods=['GET', 'POST'])
def order():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, product_name, category, quantity, price FROM inventory ORDER BY product_name')
    produtos = cur.fetchall()

    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        takeaway      = request.form.get('takeaway', 'Sim')
        order_details = {}
        erros = False

        for prod in produtos:
            qtd = int(request.form.get(f'produto_{prod["id"]}', 0))
            if qtd < 0 or qtd > prod['quantity']:
                flash(f"Quantidade inválida p/ {prod['product_name']}. Disponível: {prod['quantity']}.", "error")
                erros = True
            elif qtd > 0:
                order_details[prod['product_name']] = qtd

        if erros or not order_details:
            cur.close(); conn.close()
            return redirect(url_for('order'))

        # Atualiza estoque com transação
        for prod in produtos:
            qtd = int(request.form.get(f'produto_{prod["id"]}', 0))
            if qtd > 0:
                cur.execute(
                    "UPDATE inventory SET quantity = quantity - %s WHERE id = %s AND quantity >= %s",
                    (qtd, prod['id'], qtd)
                )
                if cur.rowcount == 0:
                    flash(f"Estoque insuficiente p/ {prod['product_name']}.", "error")
                    conn.rollback()
                    cur.close(); conn.close()
                    return redirect(url_for('order'))

        # Registra pedido
        cur.execute(
            "INSERT INTO orders (customer_name, details) VALUES (%s, %s)",
            (customer_name, json.dumps(order_details))
        )
        conn.commit()
        cur.close()
        conn.close()

        # Monta e envia WhatsApp
        linhas = [f"*Pedido de:* {customer_name}", f"*Para levar:* {takeaway}", ""]
        for nome, qtd in order_details.items():
            linhas.append(f"- {qtd} x {nome}")
        texto = urllib.parse.quote("\n".join(linhas))
        wa_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={texto}"
        return redirect(wa_url)

    cur.close()
    conn.close()
    return render_template('order.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)
