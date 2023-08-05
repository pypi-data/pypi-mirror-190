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


class Wire(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "creation_time",
            "transaction_id",
            "amount",
            "last_updated_time",
            "originating_account_id",
            "receiving_account_id",
            "sender_reference_id",
            "currency",
            "id",
            "customer_id",
            "status",
        }
        
        class properties:
            amount = schemas.IntSchema
            creation_time = schemas.DateTimeSchema
            currency = schemas.StrSchema
            customer_id = schemas.UUIDSchema
            id = schemas.UUIDSchema
            last_updated_time = schemas.DateTimeSchema
            originating_account_id = schemas.UUIDSchema
            receiving_account_id = schemas.UUIDSchema
            sender_reference_id = schemas.StrSchema
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "PENDING": "PENDING",
                        "COMPLETED": "COMPLETED",
                        "CANCELED": "CANCELED",
                        "DECLINED": "DECLINED",
                    }
                
                @schemas.classproperty
                def PENDING(cls):
                    return cls("PENDING")
                
                @schemas.classproperty
                def COMPLETED(cls):
                    return cls("COMPLETED")
                
                @schemas.classproperty
                def CANCELED(cls):
                    return cls("CANCELED")
                
                @schemas.classproperty
                def DECLINED(cls):
                    return cls("DECLINED")
            transaction_id = schemas.UUIDSchema
            bank_message = schemas.StrSchema
            recipient_message = schemas.StrSchema
            __annotations__ = {
                "amount": amount,
                "creation_time": creation_time,
                "currency": currency,
                "customer_id": customer_id,
                "id": id,
                "last_updated_time": last_updated_time,
                "originating_account_id": originating_account_id,
                "receiving_account_id": receiving_account_id,
                "sender_reference_id": sender_reference_id,
                "status": status,
                "transaction_id": transaction_id,
                "bank_message": bank_message,
                "recipient_message": recipient_message,
            }
    
    creation_time: MetaOapg.properties.creation_time
    transaction_id: MetaOapg.properties.transaction_id
    amount: MetaOapg.properties.amount
    last_updated_time: MetaOapg.properties.last_updated_time
    originating_account_id: MetaOapg.properties.originating_account_id
    receiving_account_id: MetaOapg.properties.receiving_account_id
    sender_reference_id: MetaOapg.properties.sender_reference_id
    currency: MetaOapg.properties.currency
    id: MetaOapg.properties.id
    customer_id: MetaOapg.properties.customer_id
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["customer_id"]) -> MetaOapg.properties.customer_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["originating_account_id"]) -> MetaOapg.properties.originating_account_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["receiving_account_id"]) -> MetaOapg.properties.receiving_account_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["sender_reference_id"]) -> MetaOapg.properties.sender_reference_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transaction_id"]) -> MetaOapg.properties.transaction_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bank_message"]) -> MetaOapg.properties.bank_message: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["recipient_message"]) -> MetaOapg.properties.recipient_message: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["amount", "creation_time", "currency", "customer_id", "id", "last_updated_time", "originating_account_id", "receiving_account_id", "sender_reference_id", "status", "transaction_id", "bank_message", "recipient_message", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["customer_id"]) -> MetaOapg.properties.customer_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["originating_account_id"]) -> MetaOapg.properties.originating_account_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["receiving_account_id"]) -> MetaOapg.properties.receiving_account_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["sender_reference_id"]) -> MetaOapg.properties.sender_reference_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transaction_id"]) -> MetaOapg.properties.transaction_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bank_message"]) -> typing.Union[MetaOapg.properties.bank_message, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["recipient_message"]) -> typing.Union[MetaOapg.properties.recipient_message, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["amount", "creation_time", "currency", "customer_id", "id", "last_updated_time", "originating_account_id", "receiving_account_id", "sender_reference_id", "status", "transaction_id", "bank_message", "recipient_message", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, ],
        transaction_id: typing.Union[MetaOapg.properties.transaction_id, str, uuid.UUID, ],
        amount: typing.Union[MetaOapg.properties.amount, decimal.Decimal, int, ],
        last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, ],
        originating_account_id: typing.Union[MetaOapg.properties.originating_account_id, str, uuid.UUID, ],
        receiving_account_id: typing.Union[MetaOapg.properties.receiving_account_id, str, uuid.UUID, ],
        sender_reference_id: typing.Union[MetaOapg.properties.sender_reference_id, str, ],
        currency: typing.Union[MetaOapg.properties.currency, str, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        customer_id: typing.Union[MetaOapg.properties.customer_id, str, uuid.UUID, ],
        status: typing.Union[MetaOapg.properties.status, str, ],
        bank_message: typing.Union[MetaOapg.properties.bank_message, str, schemas.Unset] = schemas.unset,
        recipient_message: typing.Union[MetaOapg.properties.recipient_message, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Wire':
        return super().__new__(
            cls,
            *_args,
            creation_time=creation_time,
            transaction_id=transaction_id,
            amount=amount,
            last_updated_time=last_updated_time,
            originating_account_id=originating_account_id,
            receiving_account_id=receiving_account_id,
            sender_reference_id=sender_reference_id,
            currency=currency,
            id=id,
            customer_id=customer_id,
            status=status,
            bank_message=bank_message,
            recipient_message=recipient_message,
            _configuration=_configuration,
            **kwargs,
        )
