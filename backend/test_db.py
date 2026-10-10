from sqlalchemy import text
from app.db.session import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("SUCCESS: PostgreSQL connection is working.")
        print("Query result:", result.scalar())
except Exception as error:
    print("FAILED: PostgreSQL connection test.")
    print(type(error).__name__)
    print(str(error))
finally:
    engine.dispose()
