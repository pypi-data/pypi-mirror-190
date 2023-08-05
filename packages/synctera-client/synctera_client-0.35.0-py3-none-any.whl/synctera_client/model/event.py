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


class Event(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Webhook event object
    """


    class MetaOapg:
        
        class properties:
            event_resource = schemas.StrSchema
            event_resource_changed_fields = schemas.StrSchema
            event_time = schemas.DateTimeSchema
            id = schemas.UUIDSchema
            
            
            class metadata(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 1024
            
            
            class response_history(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['ResponseHistoryItem']:
                        return ResponseHistoryItem
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['ResponseHistoryItem'], typing.List['ResponseHistoryItem']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'response_history':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'ResponseHistoryItem':
                    return super().__getitem__(i)
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "RUNNING": "RUNNING",
                        "SUCCESS": "SUCCESS",
                        "RETRYING": "RETRYING",
                        "FAILED": "FAILED",
                    }
                
                @schemas.classproperty
                def RUNNING(cls):
                    return cls("RUNNING")
                
                @schemas.classproperty
                def SUCCESS(cls):
                    return cls("SUCCESS")
                
                @schemas.classproperty
                def RETRYING(cls):
                    return cls("RETRYING")
                
                @schemas.classproperty
                def FAILED(cls):
                    return cls("FAILED")
        
            @staticmethod
            def type() -> typing.Type['EventTypeExplicit']:
                return EventTypeExplicit
            
            
            class url(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 1024
            webhook_id = schemas.UUIDSchema
            __annotations__ = {
                "event_resource": event_resource,
                "event_resource_changed_fields": event_resource_changed_fields,
                "event_time": event_time,
                "id": id,
                "metadata": metadata,
                "response_history": response_history,
                "status": status,
                "type": type,
                "url": url,
                "webhook_id": webhook_id,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["event_resource"]) -> MetaOapg.properties.event_resource: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["event_resource_changed_fields"]) -> MetaOapg.properties.event_resource_changed_fields: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["event_time"]) -> MetaOapg.properties.event_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["response_history"]) -> MetaOapg.properties.response_history: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> 'EventTypeExplicit': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["webhook_id"]) -> MetaOapg.properties.webhook_id: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["event_resource", "event_resource_changed_fields", "event_time", "id", "metadata", "response_history", "status", "type", "url", "webhook_id", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["event_resource"]) -> typing.Union[MetaOapg.properties.event_resource, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["event_resource_changed_fields"]) -> typing.Union[MetaOapg.properties.event_resource_changed_fields, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["event_time"]) -> typing.Union[MetaOapg.properties.event_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["response_history"]) -> typing.Union[MetaOapg.properties.response_history, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> typing.Union['EventTypeExplicit', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["url"]) -> typing.Union[MetaOapg.properties.url, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["webhook_id"]) -> typing.Union[MetaOapg.properties.webhook_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["event_resource", "event_resource_changed_fields", "event_time", "id", "metadata", "response_history", "status", "type", "url", "webhook_id", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        event_resource: typing.Union[MetaOapg.properties.event_resource, str, schemas.Unset] = schemas.unset,
        event_resource_changed_fields: typing.Union[MetaOapg.properties.event_resource_changed_fields, str, schemas.Unset] = schemas.unset,
        event_time: typing.Union[MetaOapg.properties.event_time, str, datetime, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, str, schemas.Unset] = schemas.unset,
        response_history: typing.Union[MetaOapg.properties.response_history, list, tuple, schemas.Unset] = schemas.unset,
        status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
        type: typing.Union['EventTypeExplicit', schemas.Unset] = schemas.unset,
        url: typing.Union[MetaOapg.properties.url, str, schemas.Unset] = schemas.unset,
        webhook_id: typing.Union[MetaOapg.properties.webhook_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Event':
        return super().__new__(
            cls,
            *_args,
            event_resource=event_resource,
            event_resource_changed_fields=event_resource_changed_fields,
            event_time=event_time,
            id=id,
            metadata=metadata,
            response_history=response_history,
            status=status,
            type=type,
            url=url,
            webhook_id=webhook_id,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.event_type_explicit import EventTypeExplicit
from synctera_client.model.response_history_item import ResponseHistoryItem
