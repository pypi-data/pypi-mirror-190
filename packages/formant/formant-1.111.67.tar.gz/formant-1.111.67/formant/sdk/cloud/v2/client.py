from .src.admin_api import AdminAPI
import os

ADMIN_API_URL = "https://api.formant.io/v1/admin"


class Client:
    def __init__(
        self,
        email: str = None,
        password: str = None,
        api_url: str = ADMIN_API_URL,
    ):
        self._email = os.getenv("FORMANT_EMAIL") if email is None else email
        self._password = os.getenv("FORMANT_PASSWORD") if password is None else password
        if self._email is None:
            raise ValueError(
                "email argument missing and FORMANT_EMAIL environment variable not set!"
            )
        if self._password is None:
            raise ValueError(
                "password argument missing and FORMANT_PASSWORD environment variable not set"  # noqa: E501
            )
        self.admin_api = AdminAPI(
            email=self._email, password=self._password, api_url=api_url
        )
