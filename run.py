from uzbase import create_app
from seed import seed_database

app = create_app()

if __name__ == '__main__':
    # Auto-seed on startup if needed
    seed_database()
    app.run(debug=True, port=5000)
