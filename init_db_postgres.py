# init_db_postgres.py
import psycopg2
from psycopg2.extras import execute_values

# Conexão hard-coded (você pode voltar a usar variável de ambiente se preferir)
DATABASE_URL = "postgresql://juventude:rR7breZTAQ5qEPhzYfmgT0dYQhn5rweS@" \
               "dpg-d055kj9r0fns73d3dokg-a.oregon-postgres.render.com:5432/pastel"

# Conecta e aplica o schema atualizado
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()
with open('schema.sql', 'r') as f:
    cur.execute(f.read())

# Insere produtos iniciais já com preço
produtos = [
    ('Pastel de Queijo', 'pastel', 50,  5.00),
    ('Pastel de Carne',  'pastel', 50,  6.00),
    ('Pastel de Frango', 'pastel', 50,  6.50),
    ('Refrigerante',     'bebida', 30,  4.00),
    ('Suco',             'bebida', 30,  3.50)
]
sql = """
    INSERT INTO inventory (product_name, category, quantity, price)
    VALUES %s
"""
execute_values(cur, sql, produtos)

print("✅ Banco PostgreSQL inicializado com sucesso!")
cur.close()
conn.close()
