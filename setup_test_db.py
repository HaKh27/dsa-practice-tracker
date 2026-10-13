from db import get_connection, create_table

test_conn= get_connection(db_name="dsa_tracker_test")
create_table(test_conn)
print("Test database table created ")