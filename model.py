from mysql import Base
from sqlalchemy import (Column,Integer,String)

#define model
class User (Base):

#define TABLE      
    __tablename__='user'

#define attributes
    id=Column (Integer,primary_key=True,index=True)
    username=Column(String(250),nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
  