from app.db.mongo import user_collection
from app.core.security import hash_password, verify_password, is_password_reused
from app.exceptions.custom_exceptions import UserAlreadyExists, InvalidPasswordFormat
from app.core.validators import is_valid_password, is_email_or_phone
from datetime import datetime, date
import logging
from app.core.security import create_reset_token, verify_reset_token
from app.db.mysql import SessionLocal
from app.db.models import UserSQL




def convert_date_to_datetime(d: date) -> datetime:
    return datetime.combine(d, datetime.min.time())

async def register_user(data: dict):
    username = data["username"]

    existing = await user_collection.find_one({"username": username})
    if existing:
        raise UserAlreadyExists()

    if not is_email_or_phone(username):
        raise ValueError("Invalid username format. Must be a valid email or 10-digit phone number.")

    if not is_valid_password(data["password"]):
        raise InvalidPasswordFormat("Password must be 8-20 characters and contain uppercase, lowercase, number, and special character.")

    
    data["dob"] = convert_date_to_datetime(data["dob"])
    data["doj"] = convert_date_to_datetime(data["doj"])

    hashed_pwd = hash_password(data["password"])
    data.update({
        "password": hashed_pwd,
        "created_at": datetime.utcnow(),
        "password_last_changed": datetime.utcnow().isoformat(),
        "previous_passwords": [hashed_pwd]
    })
    # Saving the data to mongo  
    await user_collection.insert_one(data)
    logging.info(f"[Mongo] Registered: {username}")

    # Saving the data to MySQL
    db = SessionLocal()
    try:
        user_sql = UserSQL(
            username=username,
            first_name=data["first_name"],
            last_name=data["last_name"],
            dob=data["dob"],
            doj=data["doj"],
            address=data["address"],
            comment=data.get("comment", ""),
            is_active=data["is_active"],
            created_at=data["created_at"]
        )
        db.add(user_sql)
        db.commit()
        logging.info(f"[MySQL] Registered: {username}")
    except Exception as e:
        db.rollback()
        logging.error(f"MySQL save failed: {str(e)}")
        raise
    finally:
        db.close()

    return {"message": "User registered in both MongoDB and MySQL successfully"}


async def validate_login(username: str, password: str):
    user = await user_collection.find_one({"username": username})
    if not user:
        logging.warning(f"Login failed: User not found - {username}")
        return None

    if not verify_password(password, user["password"]):
        logging.warning(f"Login failed: Incorrect password - {username}")
        return None

    return user


async def update_password(username: str, old_pwd: str, new_pwd: str):
    user = await user_collection.find_one({"username": username})
    
    if not user:
        logging.warning(f"Password change failed: User not found - {username}")
        raise ValueError("User not found")

    if not verify_password(old_pwd, user["password"]):
        logging.warning(f"Password change failed: Incorrect old password - {username}")
        raise ValueError("Invalid old password")

    if not is_valid_password(new_pwd):
        raise InvalidPasswordFormat("New password does not meet complexity requirements")

    if is_password_reused(new_pwd, user.get("previous_passwords", [])):
        raise ValueError("This password has already been used")

    # Updating the MongoDB with new password
    new_hashed = hash_password(new_pwd)

    await user_collection.update_one(
        {"username": username},
        {
            "$set": {
                "password": new_hashed,
                "password_last_changed": datetime.utcnow().isoformat()
            },
            "$push": {
                "previous_passwords": new_hashed
            }
        }
    )

    logging.info(f"MongoDB password updated for: {username}")

    # Updating new password in MySQL database
    db = SessionLocal()
    try:
        db_user = db.query(UserSQL).filter_by(username=username).first()
        if db_user:
            db_user.created_at = datetime.utcnow()
            db.commit()
            logging.info(f"MySQL password timestamp updated for: {username}")
    except Exception as e:
        db.rollback()
        logging.error(f"MySQL update error: {str(e)}")
    finally:
        db.close()

    return {"message": "Password changed successfully"}

async def handle_forgot_password(username: str):
    user = await user_collection.find_one({"username": username})
    if not user:
        raise ValueError("User not found")

    # when we click execute in swagger we get thislink for reset the password with valid JWT token
    token = create_reset_token(username)
    logging.info(f"[FORGOT-PASSWORD] Token generated for {username}: {token}")
    return {"reset_link": f"http://yourdomain.com/reset-password?token={token}"}

async def handle_reset_password(token: str, new_password: str):
    username = verify_reset_token(token)
    if not username:
        raise ValueError("Invalid or expired token")

    user = await user_collection.find_one({"username": username})
    if not user:
        raise ValueError("User not found")

    if not is_valid_password(new_password):
        raise ValueError("Password does not meet complexity rules")

    if is_password_reused(new_password, user.get("previous_passwords", [])):
        raise ValueError("Password was previously used")

    hashed_pwd = hash_password(new_password)

    # Updating in MongoDB with reseted password 
    await user_collection.update_one(
        {"username": username},
        {
            "$set": {
                "password": hashed_pwd,
                "password_last_changed": datetime.utcnow().isoformat()
            },
            "$push": {
                "previous_passwords": hashed_pwd
            }
        }
    )

    # Updating in mysql databse with reseted password
    db = SessionLocal()
    try:
        db_user = db.query(UserSQL).filter_by(username=username).first()
        if db_user:
            db_user.created_at = datetime.utcnow()
            db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"MySQL error: {e}")
    finally:
        db.close()

    return {"message": "Password reset successful"}

async def update_email_or_phone(username: str, new_username: str):
    if not is_email_or_phone(new_username):
        raise ValueError("New username must be a valid email or phone")

    # Checking Mongo databse for multiple or duplicates
    existing = await user_collection.find_one({"username": new_username})
    if existing:
        raise ValueError("Username already exists")

    # Updating Mongo database
    await user_collection.update_one(
        {"username": username},
        {"$set": {"username": new_username}}
    )
    logging.info(f"MongoDB: Username updated from {username} to {new_username}")

    # Updating mysql database
    db = SessionLocal()
    try:
        user_sql = db.query(UserSQL).filter_by(username=username).first()
        if user_sql:
            user_sql.username = new_username
            db.commit()
            logging.info(f"MySQL: Username updated from {username} to {new_username}")
    except Exception as e:
        db.rollback()
        logging.error(f"MySQL update failed: {str(e)}")
        raise
    finally:
        db.close()

    return {"message": f"Username changed to {new_username} successfully"}

async def logout_user(username: str):
    logging.info(f"User logged out: {username}")
    return {"message": "Logout successful"}


async def logout_user(username: str):
    user = await user_collection.find_one({"username": username})
    if user:
        logging.warning(f"Logout Sucessful - {username}")

    else:
        logging.warning(f"Login failed: User not found - {username}")
        return None

    return user
