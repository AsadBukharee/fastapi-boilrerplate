import base64
import logging
import re
import traceback
import shortuuid as shortuuid
from fastapi import status
from cryptography.fernet import Fernet
from core.project_settings import settings
from helpers.custom_exceptions import CustomException


def get_encrypted_text(text):
    try:
        # convert integer etc to string firsts
        txt = str(text)
        # get the key from settings
        cipher_suite = Fernet(settings().FERNET_SECRET_KEY.encode())  # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return str(encrypted_text)
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def get_decrypted_text(text):
    try:
        # base64 decode
        if text:
            txt = base64.urlsafe_b64decode(text)
            cipher_suite = Fernet(settings().FERNET_SECRET_KEY.encode())
            decoded_text = cipher_suite.decrypt(txt).decode("ascii")
            return decoded_text
        else:
            return None

    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def image_writer(data_image):
    message = ""
    image_data = data_image["file"]
    image_name = str(data_image["name"]).split('.')[0]
    content_type = data_image["type"]

    if content_type in ["image/png", "image/jpg", "image/jpeg", "image/webp"]:
        message += " accepted "
    else:
        message += " Invalid image typ"
        raise CustomException(
            message="There was an error,Invalid image type only png, jpg, jpeg,webp allowed - error occured in user utils",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    resource_name = shortuuid.ShortUUID().random(length=8) + "_" + image_name + f".{content_type.split('/')[-1]}"
    resource_name = resource_name.replace(" ", "_")
    with open(f"./public/profile_image/{resource_name}", 'wb') as f:
        try:
            f.write(image_data)
            return resource_name
        except Exception as e:
            raise CustomException(message="There was an error,Error in writing image - error occured in user utils",
                                  status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def format_data_for_update_user_image(image) -> dict:
    """
        Format Data For Update User Controller
    """

    try:
        data_image = {}
        data_image['file'] = image.file.read()
        data_image['name'] = image.filename
        data_image['type'] = image.content_type
        return data_image

    except Exception as e:

        raise CustomException(message=f"There was an error uploading the file(s),{e} - error occured in user utils",
                              status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def remove_int_from_urls(url):
    try:
        pattern = re.compile(r'/[0-9]+')
        n_url = pattern.sub('', url)
        return n_url
    except:
        return ""
