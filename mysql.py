from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


#CREATE DATABASE URL 
username='root'
password='Pao1234!'
host='localhost'
port=3306
db_name='co2'
#CREATE DATA BASE URL
DATABASE_URL=f"mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}"
#CREATE ENGINE
engine=create_engine (DATABASE_URL)
#CREATE SESSION MAKER
Local_session=sessionmaker(autocommit=False,bind=engine,autoflush=False)

 #DECLARE BASE CLASS
Base = declarative_base()

#PROVIDE SESSION 
def get_db():
 db=Local_session()
 try:
    yield db
 finally :    db.close()
 #JHBFJRHFJRKFREFKRFRK