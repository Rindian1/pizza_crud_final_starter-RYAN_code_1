# CRUD Pizza Ordering App

A beginner-friendly Flask CRUD demo where diners browse a pizza menu, place orders, and receive an instant confirmation. The project uses SQLite for persistence and ships with sample menu items so you can run it immediately.

## Features

- **Menu browsing** – pulls pizzas from an SQLite table and renders them with pricing and images.
- **Order creation** – simple HTML form posts to the `/order` route and records the request.
- **Confirmation view** – displays the order summary, quantities, and total charge using server-side data.
- **Autoseeded database** – on first run, `data/pizzas.db` is created with example pizzas.

## Tech Stack

- Python 3.11+ (tested with CPython)
- Flask 3.0
- SQLite (via Python's built-in `sqlite3` module)
- Jinja2 templates + vanilla CSS

## Getting Started

### 1. Clone & install dependencies

```bash
git clone <your-fork-url> pizza-crud
cd pizza-crud
python -m venv .venv
.venv\Scripts\activate  # PowerShell
pip install -r requirements.txt
```

> On macOS/Linux, replace the activation command with `source .venv/bin/activate`.

### 2. Initialize the database (automatic)

Running the app triggers `init_db()` which creates `data/pizzas.db`, the `Pizza` and `Order` tables, and seeds sample pizzas. No manual SQL is required.

### 3. Run the development server

```bash
flask --app app --debug run
```

Visit http://127.0.0.1:5000 to open the menu.

## Project Structure

```
├── app.py              # Flask routes, DB helpers, seed logic
├── requirements.txt    # Python dependencies
├── templates/          # Jinja templates (menu + confirmation)
├── static/             # CSS, logos, pizza images
└── data/               # SQLite database (created on first run)
```

## Application Flow

1. **`GET /`** renders `menu.html` with pizzas loaded from the `Pizza` table.
2. **`POST /order`** validates form data, inserts a row in the `Order` table, then redirects to confirmation.
3. **`GET /confirmation?order_id=...`** looks up the saved order, calculates totals, and renders `confirmation.html`.

## Environment Variables (optional)

- `FLASK_ENV=development` – enables the debugger and auto reload.
- `FLASK_RUN_PORT=8000` – serve on a different port.


## Troubleshooting

| Issue | Fix |
| ----- | --- |
| `sqlite3.OperationalError: no such table: Pizza` | Delete `data/pizzas.db` and restart the app so `init_db()` can recreate it. |
| `ModuleNotFoundError: Flask` | Activate the virtual environment and reinstall `pip install -r requirements.txt`. |

## Contributing

1. Fork the repo & create a feature branch.
2. Make changes (keep commits focused).
3. Run the app locally to verify.
4. Open a pull request describing your change and testing steps.

## License

This starter is distributed under the MIT License. See `LICENSE` (add one if needed) for details.
