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


class TransactionLine(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "amount",
            "dc_sign",
            "account_id",
            "currency",
            "account_no",
            "uuid",
        }
        
        class properties:
            account_id = schemas.StrSchema
            account_no = schemas.StrSchema
            amount = schemas.IntSchema
            currency = schemas.StrSchema
        
            @staticmethod
            def dc_sign() -> typing.Type['DcSign']:
                return DcSign
            uuid = schemas.UUIDSchema
            __annotations__ = {
                "account_id": account_id,
                "account_no": account_no,
                "amount": amount,
                "currency": currency,
                "dc_sign": dc_sign,
                "uuid": uuid,
            }
    
    amount: MetaOapg.properties.amount
    dc_sign: 'DcSign'
    account_id: MetaOapg.properties.account_id
    currency: MetaOapg.properties.currency
    account_no: MetaOapg.properties.account_no
    uuid: MetaOapg.properties.uuid
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_id"]) -> MetaOapg.properties.account_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_no"]) -> MetaOapg.properties.account_no: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["dc_sign"]) -> 'DcSign': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["uuid"]) -> MetaOapg.properties.uuid: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["account_id", "account_no", "amount", "currency", "dc_sign", "uuid", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_id"]) -> MetaOapg.properties.account_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_no"]) -> MetaOapg.properties.account_no: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["dc_sign"]) -> 'DcSign': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["uuid"]) -> MetaOapg.properties.uuid: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account_id", "account_no", "amount", "currency", "dc_sign", "uuid", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        amount: typing.Union[MetaOapg.properties.amount, decimal.Decimal, int, ],
        dc_sign: 'DcSign',
        account_id: typing.Union[MetaOapg.properties.account_id, str, ],
        currency: typing.Union[MetaOapg.properties.currency, str, ],
        account_no: typing.Union[MetaOapg.properties.account_no, str, ],
        uuid: typing.Union[MetaOapg.properties.uuid, str, uuid.UUID, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TransactionLine':
        return super().__new__(
            cls,
            *_args,
            amount=amount,
            dc_sign=dc_sign,
            account_id=account_id,
            currency=currency,
            account_no=account_no,
            uuid=uuid,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.dc_sign import DcSign
