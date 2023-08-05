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


class CustomerVerificationResult(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Verification result
    """


    class MetaOapg:
        required = {
            "result",
            "verification_time",
            "verification_type",
        }
        
        class properties:
            
            
            class result(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def ACCEPTED(cls):
                    return cls("ACCEPTED")
                
                @schemas.classproperty
                def REJECTED(cls):
                    return cls("REJECTED")
                
                @schemas.classproperty
                def REVIEW(cls):
                    return cls("REVIEW")
                
                @schemas.classproperty
                def PROVIDER_FAILURE(cls):
                    return cls("PROVIDER_FAILURE")
                
                @schemas.classproperty
                def PROVISIONAL(cls):
                    return cls("PROVISIONAL")
            verification_time = schemas.DateTimeSchema
        
            @staticmethod
            def verification_type() -> typing.Type['VerificationType']:
                return VerificationType
            id = schemas.UUIDSchema
            
            
            class issues(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.StrSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'issues':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
        
            @staticmethod
            def raw_response() -> typing.Type['RawResponse']:
                return RawResponse
        
            @staticmethod
            def vendor_info() -> typing.Type['VerificationVendorInfo']:
                return VerificationVendorInfo
            __annotations__ = {
                "result": result,
                "verification_time": verification_time,
                "verification_type": verification_type,
                "id": id,
                "issues": issues,
                "raw_response": raw_response,
                "vendor_info": vendor_info,
            }
    
    result: MetaOapg.properties.result
    verification_time: MetaOapg.properties.verification_time
    verification_type: 'VerificationType'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["result"]) -> MetaOapg.properties.result: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["verification_time"]) -> MetaOapg.properties.verification_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["verification_type"]) -> 'VerificationType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["issues"]) -> MetaOapg.properties.issues: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["raw_response"]) -> 'RawResponse': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["vendor_info"]) -> 'VerificationVendorInfo': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["result", "verification_time", "verification_type", "id", "issues", "raw_response", "vendor_info", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["result"]) -> MetaOapg.properties.result: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["verification_time"]) -> MetaOapg.properties.verification_time: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["verification_type"]) -> 'VerificationType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["issues"]) -> typing.Union[MetaOapg.properties.issues, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["raw_response"]) -> typing.Union['RawResponse', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["vendor_info"]) -> typing.Union['VerificationVendorInfo', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["result", "verification_time", "verification_type", "id", "issues", "raw_response", "vendor_info", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        result: typing.Union[MetaOapg.properties.result, str, ],
        verification_time: typing.Union[MetaOapg.properties.verification_time, str, datetime, ],
        verification_type: 'VerificationType',
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        issues: typing.Union[MetaOapg.properties.issues, list, tuple, schemas.Unset] = schemas.unset,
        raw_response: typing.Union['RawResponse', schemas.Unset] = schemas.unset,
        vendor_info: typing.Union['VerificationVendorInfo', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CustomerVerificationResult':
        return super().__new__(
            cls,
            *_args,
            result=result,
            verification_time=verification_time,
            verification_type=verification_type,
            id=id,
            issues=issues,
            raw_response=raw_response,
            vendor_info=vendor_info,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.raw_response import RawResponse
from synctera_client.model.verification_type import VerificationType
from synctera_client.model.verification_vendor_info import VerificationVendorInfo
