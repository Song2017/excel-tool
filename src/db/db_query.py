import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker


def get_session(sql_str: str = ""):
    sql_str = sql_str or os.getenv('DB_CONN')
    engine = create_engine(sql_str, encoding='utf-8')
    session = scoped_session(sessionmaker(bind=engine))
    return session


def execute_query(p_text: str, p_filter: dict, session=None) -> list:
    # sql_query = text("SELECT * FROM users WHERE name = :name")
    # # 使用 session 执行原生的 SQL 语句
    # results = session.execute(sql_query, {'name': 'John Doe'})
    session = session or get_session()
    sql_query = text(p_text)
    c_results = session.execute(sql_query, p_filter)
    # 遍历查询结果
    result = [row for row in c_results]
    # 关闭结果集
    c_results.close()
    return result
