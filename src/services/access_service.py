from sqlalchemy import and_, or_
from fastapi import status, HTTPException

from helpers.custom_exceptions import CustomException
from src.models.idp_users_model import idp_users


class AccessService():

    def __init__(self, db):
        self.db = db

    def get_user_apps_info_db(self, user_email) -> dict:
        users_info_object = self.db.query(idp_users).filter(idp_users.email==user_email).all()

        if users_info_object:
            products = dict({"products":[]})
            products.update({"user": users_info_object[0][0]})
            for user, apps in users_info_object:
                products["products"].append(
                        dict({
                        "email": user.email,
                        "product_name": apps.display_name,
                        "logo": apps.logo_url,
                        "product_id": apps.id
                     })
                )
            return products
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message='No data found for this user')