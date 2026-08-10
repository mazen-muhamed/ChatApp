import os
from sqlalchemy import create_engine,text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()

## TO connect with DB
DB_HOST = os.getenv("DB_HOST","localhost")
DB_PORT = os.getenv("DB_PORT","3306")
DB_USER = os.getenv("DB_USER", "root")
DB_NAME = os.getenv("DB_NAME","chatapp")
DB_PASSWORD = os.getenv("DB_PASSWORD","")


## it should be like that :  mysql+pymysql://root@localhost:3306/chatapp
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"\
# To check if the db connected
print("Connecting to:", DATABASE_URL)

# Configure engine & Session

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
CREATE_SQL_TABLES = """

CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(30) NOT NULL UNIQUE, 
        phone_number VARCHAR(15) NOT NULL,
        hashed_password VARCHAR(200) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );
    
    CREATE TABLE IF NOT EXISTS rooms (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(30) UNIQUE,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS Message (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT,
        room_id INT NOT NULL,
        sender_type ENUM('user','bot') DEFAULT 'user' NOT NULL,
        message TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL ON UPDATE CASCADE,
        FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    CREATE TABLE IF NOT EXISTS room_participants (
        user_id INT NOT NULL,
        room_id INT NOT NULL,
        joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        left_at DATETIME,
        PRIMARY KEY (user_id, room_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    
"""      

def create_tables():
    with engine.connect() as conn:
        for st in CREATE_SQL_TABLES.strip().split(';'):
            stmt = st.strip()
            if stmt:
                conn.execute(text(stmt))
        conn.commit()
    print("All tables created (or already exist).")

# Test