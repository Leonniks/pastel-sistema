import os
import psycopg2
from psycopg2.extras import execute_values

# Lê a URL do banco da variável de ambiente
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("postgresql://juventude:rR7breZTAQ5qEPhzYfmgT0dYQhn5rweS@dpg-d055kj9r0fns73d3dokg-a.oregon-postgres.render.com/pastel")

# Conecta ao PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

# 1) Executa o schema (reaproveite seu schema.sql, mas sem DROP IF EXISTS se preferir)
with open('schema.sql', 'r') as f:
    cur.execute(f.read())

# 2) Insere dados iniciais (ajuste quantidades conforme desejar)
produtos = [
    ('Pastel de Queijo', 'pastel', 50),
    ('Pastel de Carne',  'pastel', 50),
    ('Pastel de Frango','pastel', 50),
    ('Refrigerante',    'bebida', 30),
    ('Suco',            'bebida', 30)
]
sql = """
    INSERT INTO inventory (product_name, category, quantity)
    VALUES %s
"""
execute_values(cur, sql, produtos)

print("Banco PostgreSQL inicializado com sucesso!")
cur.close()
conn.close()
