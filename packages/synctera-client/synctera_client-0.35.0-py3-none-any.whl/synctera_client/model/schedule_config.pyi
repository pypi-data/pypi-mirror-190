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


class ScheduleConfig(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Payment schedule recurrence configuration
    """


    class MetaOapg:
        required = {
            "interval",
            "frequency",
            "start_date",
        }
        
        class properties:
            
            
            class frequency(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def DAILY(cls):
                    return cls("DAILY")
                
                @schemas.classproperty
                def WEEKLY(cls):
                    return cls("WEEKLY")
                
                @schemas.classproperty
                def MONTHLY(cls):
                    return cls("MONTHLY")
            
            
            class interval(
                schemas.IntSchema
            ):
                pass
            start_date = schemas.DateSchema
            
            
            class count(
                schemas.Int32Schema
            ):
                pass
            end_date = schemas.DateSchema
            __annotations__ = {
                "frequency": frequency,
                "interval": interval,
                "start_date": start_date,
                "count": count,
                "end_date": end_date,
            }
    
    interval: MetaOapg.properties.interval
    frequency: MetaOapg.properties.frequency
    start_date: MetaOapg.properties.start_date
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["frequency"]) -> MetaOapg.properties.frequency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["interval"]) -> MetaOapg.properties.interval: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["start_date"]) -> MetaOapg.properties.start_date: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["count"]) -> MetaOapg.properties.count: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["end_date"]) -> MetaOapg.properties.end_date: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["frequency", "interval", "start_date", "count", "end_date", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["frequency"]) -> MetaOapg.properties.frequency: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["interval"]) -> MetaOapg.properties.interval: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["start_date"]) -> MetaOapg.properties.start_date: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["count"]) -> typing.Union[MetaOapg.properties.count, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["end_date"]) -> typing.Union[MetaOapg.properties.end_date, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["frequency", "interval", "start_date", "count", "end_date", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        interval: typing.Union[MetaOapg.properties.interval, decimal.Decimal, int, ],
        frequency: typing.Union[MetaOapg.properties.frequency, str, ],
        start_date: typing.Union[MetaOapg.properties.start_date, str, date, ],
        count: typing.Union[MetaOapg.properties.count, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        end_date: typing.Union[MetaOapg.properties.end_date, str, date, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ScheduleConfig':
        return super().__new__(
            cls,
            *_args,
            interval=interval,
            frequency=frequency,
            start_date=start_date,
            count=count,
            end_date=end_date,
            _configuration=_configuration,
            **kwargs,
        )
