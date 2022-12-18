from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime

from src.models import idp_users
from src.utils.auth_utils import create_password_hash
def create_super_admin(db: Session):

    try:
        hashed_password = create_password_hash("admin")
        check = idp_users(
            uuid = uuid4(),
            organization_id = "2",
            username = "syedfaisal",
            title = None,
            first_name = "syed",
            last_name = "faisal",
            email = "faisal@gmail.com",
            other_email = "syedfaisal2@gmail.com",
            gender = "male",
            nhs_number = "4",
            password_hash = hashed_password,
            reset_password_token = "nothing",
            reset_password_token_expiry = "nothing",
            profile_image = None,
            contact_no = "2222222222",
            address = "nothing",
            is_approved = True,
            is_rejected = False,
            is_on_hold = False,
            is_superuser = True,
            is_active = True,
            created_date = datetime.now(),
            updated_date = datetime.now(),
            last_login_date = datetime.now()
            )
        db.add(check)
        db.commit()
    except Exception as e:
        print(e)