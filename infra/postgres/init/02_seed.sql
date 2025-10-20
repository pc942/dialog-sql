
INSERT INTO customers (name, region) VALUES
  ('Acme Corp', 'NA'),
  ('Globex',    'EU'),
  ('Initech',   'NA');

INSERT INTO orders (customer_id, product_line, amount, created_at) VALUES
  (1, 'Gadgets', 120.00, '2025-01-15'),
  (1, 'Widgets', 200.00, '2025-02-20'),
  (2, 'Gadgets',  95.50, '2025-03-03'),
  (3, 'Widgets',  33.33, '2025-03-21'),
  (3, 'Gadgets',  60.00, '2025-04-01');
