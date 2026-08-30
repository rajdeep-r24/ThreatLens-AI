import logging
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, init_database
from app.models.user import User, RoleEnum
from app.core.security import hash_password

logger = logging.getLogger(__name__)

# Default demo users to seed for instant testing & development
SEED_USERS = [
    {
        "email": "admin@threatlens.ai",
        "username": "admin",
        "full_name": "Platform Administrator",
        "password": "AdminPassword123!",
        "role": RoleEnum.ADMINISTRATOR,
    },
    {
        "email": "analyst@threatlens.ai",
        "username": "analyst_sarah",
        "full_name": "Sarah Connor (Security Analyst)",
        "password": "AnalystPassword123!",
        "role": RoleEnum.SECURITY_ANALYST,
    },
    {
        "email": "soc@threatlens.ai",
        "username": "soc_alex",
        "full_name": "Alex Mercer (SOC Analyst)",
        "password": "SocPassword123!",
        "role": RoleEnum.SOC_TEAM,
    },
    {
        "email": "researcher@threatlens.ai",
        "username": "researcher_elena",
        "full_name": "Dr. Elena Rostova (Malware Researcher)",
        "password": "ResearcherPassword123!",
        "role": RoleEnum.RESEARCHER,
    },
]


def seed_default_users(db: Session) -> None:
    """Seed default accounts for each role if they don't already exist."""
    for user_data in SEED_USERS:
        existing_user = db.query(User).filter(
            (User.email == user_data["email"]) | (User.username == user_data["username"])
        ).first()

        if not existing_user:
            user = User(
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                hashed_password=hash_password(user_data["password"]),
                role=user_data["role"],
                is_active=True,
            )
            db.add(user)
            logger.info(f"Seeded user: {user.username} ({user.role.value})")
    
    db.commit()


def setup_initial_data() -> None:
    """Initialize DB schema and seed initial test accounts."""
    init_database()
    db = SessionLocal()
    try:
        seed_default_users(db)
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_initial_data()
    print("Database initialized and seeded successfully.")
