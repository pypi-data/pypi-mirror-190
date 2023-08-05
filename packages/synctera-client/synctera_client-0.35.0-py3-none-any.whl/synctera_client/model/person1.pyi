# coding: utf-8

"""
    Synctera API

    <h2>Let's build something great.</h2><p>Welcome to the official reference documentation for Synctera APIs. Our APIs are the best way to automate your company's banking needs and are designed to be easy to understand and implement.</p><p>We're continuously growing this library and what you see here is just the start, but if you need something specific or have a question, <a class='text-blue-600' href='https://synctera.com/contact' target='_blank' rel='noreferrer'>contact us</a>.</p>   # noqa: E501

    The version of the OpenAPI document: 0.32.0.dev6
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


class Person1(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            creation_time = schemas.DateTimeSchema
            first_name = schemas.StrSchema
            id = schemas.UUIDSchema
            last_name = schemas.StrSchema
            last_updated_time = schemas.DateTimeSchema
            middle_name = schemas.StrSchema
            relationship_type = schemas.StrSchema
            __annotations__ = {
                "creation_time": creation_time,
                "first_name": first_name,
                "id": id,
                "last_name": last_name,
                "last_updated_time": last_updated_time,
                "middle_name": middle_name,
                "relationship_type": relationship_type,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["first_name"]) -> MetaOapg.properties.first_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_name"]) -> MetaOapg.properties.last_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["middle_name"]) -> MetaOapg.properties.middle_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["relationship_type"]) -> MetaOapg.properties.relationship_type: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["creation_time", "first_name", "id", "last_name", "last_updated_time", "middle_name", "relationship_type", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["first_name"]) -> typing.Union[MetaOapg.properties.first_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_name"]) -> typing.Union[MetaOapg.properties.last_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> typing.Union[MetaOapg.properties.last_updated_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["middle_name"]) -> typing.Union[MetaOapg.properties.middle_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["relationship_type"]) -> typing.Union[MetaOapg.properties.relationship_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["creation_time", "first_name", "id", "last_name", "last_updated_time", "middle_name", "relationship_type", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
        first_name: typing.Union[MetaOapg.properties.first_name, str, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        last_name: typing.Union[MetaOapg.properties.last_name, str, schemas.Unset] = schemas.unset,
        last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, schemas.Unset] = schemas.unset,
        middle_name: typing.Union[MetaOapg.properties.middle_name, str, schemas.Unset] = schemas.unset,
        relationship_type: typing.Union[MetaOapg.properties.relationship_type, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Person1':
        return super().__new__(
            cls,
            *_args,
            creation_time=creation_time,
            first_name=first_name,
            id=id,
            last_name=last_name,
            last_updated_time=last_updated_time,
            middle_name=middle_name,
            relationship_type=relationship_type,
            _configuration=_configuration,
            **kwargs,
        )
