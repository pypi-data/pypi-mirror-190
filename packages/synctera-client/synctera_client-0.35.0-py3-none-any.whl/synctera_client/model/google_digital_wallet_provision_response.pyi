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


class GoogleDigitalWalletProvisionResponse(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            card_id = schemas.UUIDSchema
            created_time = schemas.DateTimeSchema
            last_modified_time = schemas.DateTimeSchema
        
            @staticmethod
            def push_tokenize_request_data() -> typing.Type['PushTokenizeRequestData']:
                return PushTokenizeRequestData
            __annotations__ = {
                "card_id": card_id,
                "created_time": created_time,
                "last_modified_time": last_modified_time,
                "push_tokenize_request_data": push_tokenize_request_data,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_id"]) -> MetaOapg.properties.card_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created_time"]) -> MetaOapg.properties.created_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_modified_time"]) -> MetaOapg.properties.last_modified_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["push_tokenize_request_data"]) -> 'PushTokenizeRequestData': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["card_id", "created_time", "last_modified_time", "push_tokenize_request_data", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_id"]) -> typing.Union[MetaOapg.properties.card_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created_time"]) -> typing.Union[MetaOapg.properties.created_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_modified_time"]) -> typing.Union[MetaOapg.properties.last_modified_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["push_tokenize_request_data"]) -> typing.Union['PushTokenizeRequestData', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["card_id", "created_time", "last_modified_time", "push_tokenize_request_data", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        card_id: typing.Union[MetaOapg.properties.card_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        created_time: typing.Union[MetaOapg.properties.created_time, str, datetime, schemas.Unset] = schemas.unset,
        last_modified_time: typing.Union[MetaOapg.properties.last_modified_time, str, datetime, schemas.Unset] = schemas.unset,
        push_tokenize_request_data: typing.Union['PushTokenizeRequestData', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'GoogleDigitalWalletProvisionResponse':
        return super().__new__(
            cls,
            *_args,
            card_id=card_id,
            created_time=created_time,
            last_modified_time=last_modified_time,
            push_tokenize_request_data=push_tokenize_request_data,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.push_tokenize_request_data import PushTokenizeRequestData
