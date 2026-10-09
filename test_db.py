import pytest

from db import get_connection, insert_problems,create_table, get_all_problems,delete_problem_sql,update_field_sql, find_by_name_sql

def test_insert_problems():
    conn=get_connection(":memory:")
    create_table(conn)
    insert_problems(conn, "Test", "Testing", "Easy", "2026-10-08")
    result= get_all_problems(conn)
    assert result[0][1]=="Test"
    assert result[0][2]=="Testing"
    assert result[0][3]=="Easy"

def test_delete_problems():
    conn= get_connection(":memory:")
    create_table(conn)
    insert_problems(conn, "Test", "Testing", "Easy", "2026-10-08")
    result=get_all_problems(conn)
    delete_problem_sql(conn, result[0][0])
    result2= get_all_problems(conn)
    assert result2==[]

def test_update_field():
    conn= get_connection(":memory:")
    create_table(conn)
    insert_problems(conn, "Test", "Testing", "Easy", "2026-10-08")
    result=get_all_problems(conn)
    with pytest.raises(ValueError):
        update_field_sql(conn, result[0][0], "column", "x")

def test_partial_name_match():
    conn=get_connection(":memory:")
    create_table(conn)
    insert_problems(conn, "Test", "Testing", "Easy", "2026-10-08")
    result=get_all_problems(conn)
    found= find_by_name_sql(conn, "Te")
    assert found[0][1]=="Test"
