# coding: utf-8

"""
    Synctera API

    <h2>Let's build something great.</h2><p>Welcome to the official reference documentation for Synctera APIs. Our APIs are the best way to automate your company's banking needs and are designed to be easy to understand and implement.</p><p>We're continuously growing this library and what you see here is just the start, but if you need something specific or have a question, <a class='text-blue-600' href='https://synctera.com/contact' target='_blank' rel='noreferrer'>contact us</a>.</p>   # noqa: E501

    The version of the OpenAPI document: 0.35.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from synctera_client import schemas  # noqa: F401


class SingleUseTokenResponse(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "expires",
        }
        
        class properties:
            expires = schemas.DateTimeSchema
            customer_account_mapping_id = schemas.StrSchema
            token = schemas.StrSchema
            __annotations__ = {
                "expires": expires,
                "customer_account_mapping_id": customer_account_mapping_id,
                "token": token,
            }
    
    expires: MetaOapg.properties.expires
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expires"]) -> MetaOapg.properties.expires: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["customer_account_mapping_id"]) -> MetaOapg.properties.customer_account_mapping_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["token"]) -> MetaOapg.properties.token: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["expires", "customer_account_mapping_id", "token", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expires"]) -> MetaOapg.properties.expires: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["customer_account_mapping_id"]) -> typing.Union[MetaOapg.properties.customer_account_mapping_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["token"]) -> typing.Union[MetaOapg.properties.token, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["expires", "customer_account_mapping_id", "token", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        expires: typing.Union[MetaOapg.properties.expires, str, datetime, ],
        customer_account_mapping_id: typing.Union[MetaOapg.properties.customer_account_mapping_id, str, schemas.Unset] = schemas.unset,
        token: typing.Union[MetaOapg.properties.token, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'SingleUseTokenResponse':
        return super().__new__(
            cls,
            *_args,
            expires=expires,
            customer_account_mapping_id=customer_account_mapping_id,
            token=token,
            _configuration=_configuration,
            **kwargs,
        )
