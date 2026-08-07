
"""
CREATE DATABASE IF NOT EXISTS chat_app ; """



    """ 
     
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(30) NOT NULL UNIQUE, 
        phone_number VARCHAR(15) NOT NULL,
        hashed_password VARCHAR(200) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS rooms (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(30) UNIQUE,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
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
    """,
    """
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
