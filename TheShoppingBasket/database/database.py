from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    'mariadb+mariadbconnector://admin:toor@mariadb:3306/shopping_basket_db'
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)

