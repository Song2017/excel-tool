import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

sql_str = os.getenv('DB_CONN')
print(sql_str)
engine = create_engine(sql_str, encoding='utf-8')
session = scoped_session(sessionmaker(bind=engine))


def main():
    # session.execute(
    #     " INSERT INTO test(name, school, score) VALUES ('name2', 'cb', 22);")
    # session.commit()
    flights = session.execute(
        "SELECT * FROM test").fetchall()
    for flight in flights:
        print(
            f"{flight.name} to {flight.school}, {flight.score} minutes."
        )


def run_codegen():
    """
        pip install sqlacodegen
    """
    args = f'sqlacodegen --outfile ./test_model.py {sql_str} '
    args += '--tables coupon_redeemed,factorderitem'
    os.system(args)


if __name__ == "__main__":
    run_codegen()
