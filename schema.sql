DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS orders;

CREATE TABLE inventory (
  id           SERIAL PRIMARY KEY,
  product_name TEXT    NOT NULL,
  category     TEXT,
  quantity     INTEGER NOT NULL,
  price        NUMERIC(10,2) NOT NULL DEFAULT 0
);

CREATE TABLE orders (
  id            SERIAL PRIMARY KEY,
  customer_name TEXT,
  order_date    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  details       TEXT,
  total         NUMERIC(10,2) NOT NULL DEFAULT 0
);
