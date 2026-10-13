from db import get_connection, migrate_sqlite_to_postgres

conn=get_connection()
migrate_sqlite_to_postgres(conn)
print("Migration complete")