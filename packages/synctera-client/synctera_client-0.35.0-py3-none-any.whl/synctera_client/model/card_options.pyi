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


class CardOptions(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
        
            @staticmethod
            def billing_address() -> typing.Type['BillingAddress']:
                return BillingAddress
            card_present = schemas.BoolSchema
            
            
            class cvv(
                schemas.StrSchema
            ):
                pass
            
            
            class expiration(
                schemas.StrSchema
            ):
                pass
            __annotations__ = {
                "billing_address": billing_address,
                "card_present": card_present,
                "cvv": cvv,
                "expiration": expiration,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_address"]) -> 'BillingAddress': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_present"]) -> MetaOapg.properties.card_present: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["cvv"]) -> MetaOapg.properties.cvv: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expiration"]) -> MetaOapg.properties.expiration: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["billing_address", "card_present", "cvv", "expiration", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_address"]) -> typing.Union['BillingAddress', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_present"]) -> typing.Union[MetaOapg.properties.card_present, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["cvv"]) -> typing.Union[MetaOapg.properties.cvv, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expiration"]) -> typing.Union[MetaOapg.properties.expiration, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["billing_address", "card_present", "cvv", "expiration", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        billing_address: typing.Union['BillingAddress', schemas.Unset] = schemas.unset,
        card_present: typing.Union[MetaOapg.properties.card_present, bool, schemas.Unset] = schemas.unset,
        cvv: typing.Union[MetaOapg.properties.cvv, str, schemas.Unset] = schemas.unset,
        expiration: typing.Union[MetaOapg.properties.expiration, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CardOptions':
        return super().__new__(
            cls,
            *_args,
            billing_address=billing_address,
            card_present=card_present,
            cvv=cvv,
            expiration=expiration,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.billing_address import BillingAddress
