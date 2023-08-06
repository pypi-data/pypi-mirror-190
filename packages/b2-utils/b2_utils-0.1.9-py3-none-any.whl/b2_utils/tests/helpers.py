import validate_docbr as _validate_docbr
from constance import config
from model_bakery import baker as _baker
from rest_framework.test import APIClient
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from b2_utils import models as _models

__all__ = [
    "sample_city",
    "sample_address",
    "sample_phone",
    "sample_cpf",
    "sample_cnpj",
    "configure_api_client",
]


def configure_api_client(
    client: APIClient, set_header_version=True, access_token=None, user=None
):
    headers = {}
    if set_header_version:
        version = config.ALLOWED_VERSIONS.split(" ")[0]
        headers["HTTP_ACCEPT"] = f"application/json; version={version}"

    if access_token is not None:
        headers["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"

    if user is not None:
        access = str(TokenObtainPairSerializer.get_token(user).access_token)
        headers["HTTP_AUTHORIZATION"] = f"Bearer {access}"

    client.credentials(
        **headers,
    )

    return client


def sample_city(**kwargs):
    """Create and return a sample City"""

    return _baker.make(_models.City, **kwargs)


def sample_address(**kwargs):
    """Create and return a sample Address"""

    kwargs["city"] = kwargs.get("city", sample_city)
    return _baker.make(_models.Address, **kwargs)


def sample_phone(**kwargs):
    """Create and return a sample Phone"""

    return _baker.make(_models.Phone, **kwargs)


def sample_cpf():
    """Return a sample CPF"""

    return _validate_docbr.CPF().generate()


def sample_cnpj():
    """Return a sample CNPJ"""

    return _validate_docbr.CNPJ().generate()
