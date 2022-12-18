import os
import random
import datetime
import pyotp
from starlette import status

from celery_worker import otp_sender
from helpers.customize_response import custom_response
from src.services.access_service import AccessService
from src.validators.access_validator import SuccessfulJsonResponseValidator
from utils.common import get_encrypted_text
from utils.utils import get_redis_client

redis_client = get_redis_client()


class AccessController():
    def __init__(self, db):
        self.db = db

    def send_otp_email(self, email, product_name,product_id):

        user_data = AccessService(self.db).get_user_apps_info_db(user_email=email)
        if user_data:
            OTP = ''.join([random.choice("123456789") for _ in range(6)])
            otp_hash = get_encrypted_text(OTP + ":" + str(product_id))
            redis_client.setex(name=email, value=otp_hash, time=15 * 60 + 5)
            date_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
            natural_datetime = date_time.strftime('%I:%M:%S %p %d %b, %Y')
            data = {
                "name": user_data.get("user").first_name,
                "recipient": email,
                "app": product_name,
                "otp": OTP,
                "expires": natural_datetime,
                "logo": 'logo url'
            }

            task = otp_sender.delay(user_data=data)
            # 2022-05-20 04:10:29.098
            return {'status_code': status.HTTP_200_OK, "expires": date_time, 'task_id': task.id}
        else:
            data = {
                "message": 'product not found for this user',
                "statuscode": status.HTTP_404_NOT_FOUND
            }
            validated_data = SuccessfulJsonResponseValidator(**data)
            return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)

        data = {
            "message": 'user not found with this email.',
            "statuscode": status.HTTP_404_NOT_FOUND
        }
        validated_data = SuccessfulJsonResponseValidator(**data)
        return custom_response(status_code=status.HTTP_404_NOT_FOUND, data=validated_data)
        # raise CustomException(status_code=status.HTTP_406_NOT_ACCEPTABLE, message='user already exists with this email')