from database.database import engine
from database.tables import Base
from time import sleep


sleep(5)
Base.metadata.create_all(engine)

