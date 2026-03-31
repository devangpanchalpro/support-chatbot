import models, database, auth
from sqlalchemy.orm import Session

def initialize():
    print("\n--- Initializing Database for AarogyaOne ---")
    models.Base.metadata.create_all(bind=database.engine)
    db = next(database.get_db())

    # Create Default Admin User
    user = db.query(models.User).filter(models.User.username == "admin").first()
    if not user:
        print("Creating default user: admin / admin123")
        hashed = auth.get_password_hash("admin123")
        new_user = models.User(username="admin", hashed_password=hashed)
        db.add(new_user)
        db.commit()
        print("✅ User 'admin' created successfully!")
    else:
        print("⚠️ User 'admin' already exists.")

    print("\n--- Summary ---")
    print("API Key : aarogya_one_admin_api_key_xyz123 (X-API-KEY header)")
    print("User    : admin / admin123")
    print("-------------------------------------------\n")

if __name__ == "__main__":
    initialize()
