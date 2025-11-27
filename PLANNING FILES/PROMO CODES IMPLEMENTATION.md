## 1) Seed Promo Code Table Data

Add the following promotional codes to the PromoCode table during database initialization:

### Promo Codes to Seed:
- **WELCOME10**: 10% discount, unlimited usage
- **MIDEWEEK15**: 15% discount, 200 usage limit  
- **FAMILY20**: 20% discount, 150 usage limit

### Implementation Details:
```sql
INSERT INTO PromoCode (code, discount_percent, start_date, end_date, usage_limit, times_used) VALUES 
('WELCOME10', 0.10, '2024-01-01T00:00:00', '2025-12-31T23:59:59', NULL, 0),
('MIDEWEEK15', 0.15, '2024-01-01T00:00:00', '2025-12-31T23:59:59', 200, 0),
('FAMILY20', 0.20, '2024-01-01T00:00:00', '2025-12-31T23:59:59', 150, 0)
```

### Notes:
- Use `usage_limit = NULL` for "unlimited" usage
- Set reasonable start/end dates (current year)
- Initialize `times_used = 0` for all codes
- Add this seeding logic to `init_db()` function after table creation
- Only seed if PromoCode table is empty (check COUNT(*) = 0)

## 2) Add Promo Code Field to Menu.HTML

### Implementation:
- Add input field for promo code in the order form
- Should be optional (not required)
- Place after customer_name field
- Use text input with placeholder "Enter promo code (optional)"
- Add validation to check if promo code exists and is valid

## 3) Add Promo Code Text to Confirmation.HTML

### Implementation:
- Add promo code display below the date field
- Format: "PROMO_CODE (X% off)" 
- Example: "WELCOME10 (10% off)"
- Only show if promo code was used
- Use same styling as other order details

## 4) Add Discount Display to Confirmation.HTML

### Implementation:
- Add "Discount" line below the order total
- Show discount amount: "-$X.XX"
- Add "Discounted Total" line below discount
- Calculate: Total - Discount = Discounted Total
- Only show discount section if promo code was applied