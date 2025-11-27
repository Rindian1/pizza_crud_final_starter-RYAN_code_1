# Database Schema Changes

## Order Table Changes

### Current Schema:
```sql
CREATE TABLE IF NOT EXISTS "Order" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pizza_id INTEGER,
    quantity INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pizza_id) REFERENCES Pizza (id)
)
```

### Required Changes:
1. **pizza_id**: Add NOT NULL constraint
2. **Add customer_name**: TEXT NOT NULL
3. **Add timestamp**: TEXT NOT NULL (ISO 8601 format)
4. **Add promo_code_id**: INTEGER NULLABLE (foreign key to PromoCode)
5. **Remove order_date**: Delete this column

### Final Order Schema:
```sql
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
```

## New PromoCode Table

### Schema:
```sql
CREATE TABLE IF NOT EXISTS PromoCode (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    discount_percent REAL NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    usage_limit INTEGER NOT NULL,
    times_used INTEGER NOT NULL DEFAULT 0
)
```

## Implementation Tasks:
- Update `init_db()` function to create PromoCode table and modify Order table
- Update `save_order()` function to handle new columns (customer_name, timestamp, promo_code_id)
- Add ISO 8601 timestamp generation for new orders
- Add promo code validation and application logic