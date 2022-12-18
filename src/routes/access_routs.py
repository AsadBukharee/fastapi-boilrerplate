from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from core.db.session import get_db
from . import oauth2_scheme
from ..controllers.access_controller import AccessController
from ..validators.access_validator import OtpEmailValidator, SuccessfulJsonResponseValidator

router = APIRouter(tags=["Account Access"])


@router.post("/send-otp", summary="Send OTP via email",
             responses={200: {"model": SuccessfulJsonResponseValidator}}, status_code=200)
async def send_otp(email_validator: OtpEmailValidator, db: Session = Depends(
    get_db)):  # ,authorize: AuthJWT = Depends(), token: str = Depends(oauth2_scheme)):
    """
        This api returns the emails and apps list to grant access using emails.
        after receiving email, verify whether its register.
    """
    response = AccessController(db).send_otp_email(email=email_validator.email,
                                                   product_name=email_validator.product_name,
                                                   product_id=email_validator.product_id)
    return response
