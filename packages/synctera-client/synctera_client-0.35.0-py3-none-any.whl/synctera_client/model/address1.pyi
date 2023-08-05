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


class Address1(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "country_code",
            "city",
            "address_line_1",
            "state",
            "postal_code",
        }
        
        class properties:
            address_line_1 = schemas.StrSchema
            city = schemas.StrSchema
            country_code = schemas.StrSchema
            postal_code = schemas.StrSchema
            state = schemas.StrSchema
            address_line_2 = schemas.StrSchema
            __annotations__ = {
                "address_line_1": address_line_1,
                "city": city,
                "country_code": country_code,
                "postal_code": postal_code,
                "state": state,
                "address_line_2": address_line_2,
            }
    
    country_code: MetaOapg.properties.country_code
    city: MetaOapg.properties.city
    address_line_1: MetaOapg.properties.address_line_1
    state: MetaOapg.properties.state
    postal_code: MetaOapg.properties.postal_code
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["address_line_1"]) -> MetaOapg.properties.address_line_1: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["city"]) -> MetaOapg.properties.city: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["country_code"]) -> MetaOapg.properties.country_code: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["postal_code"]) -> MetaOapg.properties.postal_code: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["address_line_2"]) -> MetaOapg.properties.address_line_2: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["address_line_1", "city", "country_code", "postal_code", "state", "address_line_2", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["address_line_1"]) -> MetaOapg.properties.address_line_1: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["city"]) -> MetaOapg.properties.city: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["country_code"]) -> MetaOapg.properties.country_code: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["postal_code"]) -> MetaOapg.properties.postal_code: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["address_line_2"]) -> typing.Union[MetaOapg.properties.address_line_2, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["address_line_1", "city", "country_code", "postal_code", "state", "address_line_2", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        country_code: typing.Union[MetaOapg.properties.country_code, str, ],
        city: typing.Union[MetaOapg.properties.city, str, ],
        address_line_1: typing.Union[MetaOapg.properties.address_line_1, str, ],
        state: typing.Union[MetaOapg.properties.state, str, ],
        postal_code: typing.Union[MetaOapg.properties.postal_code, str, ],
        address_line_2: typing.Union[MetaOapg.properties.address_line_2, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Address1':
        return super().__new__(
            cls,
            *_args,
            country_code=country_code,
            city=city,
            address_line_1=address_line_1,
            state=state,
            postal_code=postal_code,
            address_line_2=address_line_2,
            _configuration=_configuration,
            **kwargs,
        )
