## app.js Contains : 
- Login
- Register
- Logout
- WebSocket Connection
- Send MSG
- Receive MSG
- Render MSG
- Create Room
- Load Rooms
- Join Rooms

----------------------------------------------------------------------------------------

@main.py:
    Routes
    HTTP StatusCodes
    CRUD Operations

@database.py:
    DatabaseConnections
    Sessions
    Engine

@models.py:
    SQLAlchemy Models {ORM} => Room , Message

@schemas.py:
    Request Validation:
        Login/Register
        Room Create
        Message Create

@auth.py:
    hash_password()
    verify_password()
    create_access_token()
    verify_token()
    get_current_user()
    get_active_sessions()
    revoke_all_sessions()

@websockets.py:
    Connection Manager
    connect()
    disconnect()
    broadcast()

@ai.py:
    generate_reply
    find_best_answer : based on context of user
    fallback_response


