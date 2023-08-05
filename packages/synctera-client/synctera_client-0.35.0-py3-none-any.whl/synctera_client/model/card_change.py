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


class CardChange(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Card change details
    """


    class MetaOapg:
        required = {
            "updated_at",
            "channel",
            "updated_by",
            "change_type",
            "id",
            "state",
        }
        
        class properties:
        
            @staticmethod
            def change_type() -> typing.Type['ChangeType']:
                return ChangeType
        
            @staticmethod
            def channel() -> typing.Type['ChangeChannel']:
                return ChangeChannel
            id = schemas.UUIDSchema
        
            @staticmethod
            def state() -> typing.Type['CardChangeState']:
                return CardChangeState
            updated_at = schemas.DateTimeSchema
            updated_by = schemas.StrSchema
        
            @staticmethod
            def memo() -> typing.Type['CardStatusReasonMemo']:
                return CardStatusReasonMemo
        
            @staticmethod
            def reason() -> typing.Type['CardStatusReasonCode']:
                return CardStatusReasonCode
            __annotations__ = {
                "change_type": change_type,
                "channel": channel,
                "id": id,
                "state": state,
                "updated_at": updated_at,
                "updated_by": updated_by,
                "memo": memo,
                "reason": reason,
            }
    
    updated_at: MetaOapg.properties.updated_at
    channel: 'ChangeChannel'
    updated_by: MetaOapg.properties.updated_by
    change_type: 'ChangeType'
    id: MetaOapg.properties.id
    state: 'CardChangeState'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["change_type"]) -> 'ChangeType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["channel"]) -> 'ChangeChannel': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["state"]) -> 'CardChangeState': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated_by"]) -> MetaOapg.properties.updated_by: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["memo"]) -> 'CardStatusReasonMemo': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["reason"]) -> 'CardStatusReasonCode': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["change_type", "channel", "id", "state", "updated_at", "updated_by", "memo", "reason", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["change_type"]) -> 'ChangeType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["channel"]) -> 'ChangeChannel': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> 'CardChangeState': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated_at"]) -> MetaOapg.properties.updated_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated_by"]) -> MetaOapg.properties.updated_by: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["memo"]) -> typing.Union['CardStatusReasonMemo', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["reason"]) -> typing.Union['CardStatusReasonCode', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["change_type", "channel", "id", "state", "updated_at", "updated_by", "memo", "reason", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        updated_at: typing.Union[MetaOapg.properties.updated_at, str, datetime, ],
        channel: 'ChangeChannel',
        updated_by: typing.Union[MetaOapg.properties.updated_by, str, ],
        change_type: 'ChangeType',
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        state: 'CardChangeState',
        memo: typing.Union['CardStatusReasonMemo', schemas.Unset] = schemas.unset,
        reason: typing.Union['CardStatusReasonCode', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CardChange':
        return super().__new__(
            cls,
            *_args,
            updated_at=updated_at,
            channel=channel,
            updated_by=updated_by,
            change_type=change_type,
            id=id,
            state=state,
            memo=memo,
            reason=reason,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.card_change_state import CardChangeState
from synctera_client.model.card_status_reason_code import CardStatusReasonCode
from synctera_client.model.card_status_reason_memo import CardStatusReasonMemo
from synctera_client.model.change_channel import ChangeChannel
from synctera_client.model.change_type import ChangeType
