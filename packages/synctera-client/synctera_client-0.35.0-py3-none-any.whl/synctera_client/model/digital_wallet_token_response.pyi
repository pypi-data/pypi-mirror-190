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


class DigitalWalletTokenResponse(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            approved_time = schemas.DateTimeSchema
            card_id = schemas.UUIDSchema
            
            
            class device_id(
                schemas.StrSchema
            ):
                pass
            
            
            class device_type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def MOBILE_PHONE(cls):
                    return cls("MOBILE_PHONE")
                
                @schemas.classproperty
                def WATCH(cls):
                    return cls("WATCH")
                
                @schemas.classproperty
                def TABLET(cls):
                    return cls("TABLET")
                
                @schemas.classproperty
                def MOBILE_PHONE_OR_TABLET(cls):
                    return cls("MOBILE_PHONE_OR_TABLET")
                
                @schemas.classproperty
                def VEHICLE(cls):
                    return cls("VEHICLE")
                
                @schemas.classproperty
                def APPLIANCE(cls):
                    return cls("APPLIANCE")
                
                @schemas.classproperty
                def LAPTOP(cls):
                    return cls("LAPTOP")
                
                @schemas.classproperty
                def GAMING_DEVICE(cls):
                    return cls("GAMING_DEVICE")
                
                @schemas.classproperty
                def UNKNOWN(cls):
                    return cls("UNKNOWN")
            id = schemas.UUIDSchema
            last_modified_time = schemas.DateTimeSchema
            requested_time = schemas.DateTimeSchema
        
            @staticmethod
            def state() -> typing.Type['DigitalWalletTokenState']:
                return DigitalWalletTokenState
            
            
            class type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def APPLE_PAY(cls):
                    return cls("APPLE_PAY")
                
                @schemas.classproperty
                def ANDROID_PAY(cls):
                    return cls("ANDROID_PAY")
                
                @schemas.classproperty
                def SAMSUNG_PAY(cls):
                    return cls("SAMSUNG_PAY")
            __annotations__ = {
                "approved_time": approved_time,
                "card_id": card_id,
                "device_id": device_id,
                "device_type": device_type,
                "id": id,
                "last_modified_time": last_modified_time,
                "requested_time": requested_time,
                "state": state,
                "type": type,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["approved_time"]) -> MetaOapg.properties.approved_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_id"]) -> MetaOapg.properties.card_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["device_id"]) -> MetaOapg.properties.device_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["device_type"]) -> MetaOapg.properties.device_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_modified_time"]) -> MetaOapg.properties.last_modified_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["requested_time"]) -> MetaOapg.properties.requested_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["state"]) -> 'DigitalWalletTokenState': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["approved_time", "card_id", "device_id", "device_type", "id", "last_modified_time", "requested_time", "state", "type", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["approved_time"]) -> typing.Union[MetaOapg.properties.approved_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_id"]) -> typing.Union[MetaOapg.properties.card_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["device_id"]) -> typing.Union[MetaOapg.properties.device_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["device_type"]) -> typing.Union[MetaOapg.properties.device_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_modified_time"]) -> typing.Union[MetaOapg.properties.last_modified_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["requested_time"]) -> typing.Union[MetaOapg.properties.requested_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> typing.Union['DigitalWalletTokenState', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> typing.Union[MetaOapg.properties.type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["approved_time", "card_id", "device_id", "device_type", "id", "last_modified_time", "requested_time", "state", "type", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        approved_time: typing.Union[MetaOapg.properties.approved_time, str, datetime, schemas.Unset] = schemas.unset,
        card_id: typing.Union[MetaOapg.properties.card_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        device_id: typing.Union[MetaOapg.properties.device_id, str, schemas.Unset] = schemas.unset,
        device_type: typing.Union[MetaOapg.properties.device_type, str, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        last_modified_time: typing.Union[MetaOapg.properties.last_modified_time, str, datetime, schemas.Unset] = schemas.unset,
        requested_time: typing.Union[MetaOapg.properties.requested_time, str, datetime, schemas.Unset] = schemas.unset,
        state: typing.Union['DigitalWalletTokenState', schemas.Unset] = schemas.unset,
        type: typing.Union[MetaOapg.properties.type, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'DigitalWalletTokenResponse':
        return super().__new__(
            cls,
            *_args,
            approved_time=approved_time,
            card_id=card_id,
            device_id=device_id,
            device_type=device_type,
            id=id,
            last_modified_time=last_modified_time,
            requested_time=requested_time,
            state=state,
            type=type,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.digital_wallet_token_state import DigitalWalletTokenState
