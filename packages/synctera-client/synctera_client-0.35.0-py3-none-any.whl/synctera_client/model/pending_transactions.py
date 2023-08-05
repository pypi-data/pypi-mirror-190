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


class PendingTransactions(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "result",
            "next_page_token",
        }
        
        class properties:
            
            
            class next_page_token(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'next_page_token':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class result(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['PendingTransaction']:
                        return PendingTransaction
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['PendingTransaction'], typing.List['PendingTransaction']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'result':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'PendingTransaction':
                    return super().__getitem__(i)
            __annotations__ = {
                "next_page_token": next_page_token,
                "result": result,
            }
    
    result: MetaOapg.properties.result
    next_page_token: MetaOapg.properties.next_page_token
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["next_page_token"]) -> MetaOapg.properties.next_page_token: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["result"]) -> MetaOapg.properties.result: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["next_page_token", "result", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["next_page_token"]) -> MetaOapg.properties.next_page_token: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["result"]) -> MetaOapg.properties.result: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["next_page_token", "result", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        result: typing.Union[MetaOapg.properties.result, list, tuple, ],
        next_page_token: typing.Union[MetaOapg.properties.next_page_token, None, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PendingTransactions':
        return super().__new__(
            cls,
            *_args,
            result=result,
            next_page_token=next_page_token,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.pending_transaction import PendingTransaction
