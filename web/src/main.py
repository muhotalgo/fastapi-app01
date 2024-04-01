from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

app = FastAPI()

# mariadb 커넥션 초기화
host = "db"
user = "fauser"
password = "abc123!"
dbname = "fastapi"
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{dbname}", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# 모델 클래스 정의
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120), unique=True)

    def __repr__(self):
        return f"User({self.id}, {self.name}, {self.email})"

# 라우트 정의
@app.get("/")
def index():
    return {"message": "Hello from fastapi x Docker Compose"}


@app.get("/users")
def get_users():
    sess = Session()
    users = sess.query(User).all()
    sess.close()

    return [repr(user) for user in users]
