make sure order table has the follwiung schema exactly

CREATE TABLE IF NOT EXISTS "Order" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pizza_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    promo_code_id INTEGER NULL,
    FOREIGN KEY (pizza_id) REFERENCES Pizza (id),
    FOREIGN KEY (promo_code_id) REFERENCES PromoCode (id)
)

make sure the promocode table has the following schema exactly

CREATE TABLE IF NOT EXISTS PromoCode (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    discount_percent REAL NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    usage_limit INTEGER NULLABLE,
    times_used INTEGER NOT NULL DEFAULT 0
)