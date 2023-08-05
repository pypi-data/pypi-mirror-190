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


class AccountTemplate(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "is_enabled",
            "template",
            "name",
        }
        
        class properties:
            is_enabled = schemas.BoolSchema
            name = schemas.StrSchema
        
            @staticmethod
            def template() -> typing.Type['TemplateFields']:
                return TemplateFields
        
            @staticmethod
            def application_type() -> typing.Type['ApplicationType']:
                return ApplicationType
            description = schemas.StrSchema
            id = schemas.UUIDSchema
            tenant = schemas.StrSchema
            __annotations__ = {
                "is_enabled": is_enabled,
                "name": name,
                "template": template,
                "application_type": application_type,
                "description": description,
                "id": id,
                "tenant": tenant,
            }
    
    is_enabled: MetaOapg.properties.is_enabled
    template: 'TemplateFields'
    name: MetaOapg.properties.name
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_enabled"]) -> MetaOapg.properties.is_enabled: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["template"]) -> 'TemplateFields': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["application_type"]) -> 'ApplicationType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tenant"]) -> MetaOapg.properties.tenant: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["is_enabled", "name", "template", "application_type", "description", "id", "tenant", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_enabled"]) -> MetaOapg.properties.is_enabled: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["template"]) -> 'TemplateFields': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["application_type"]) -> typing.Union['ApplicationType', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tenant"]) -> typing.Union[MetaOapg.properties.tenant, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["is_enabled", "name", "template", "application_type", "description", "id", "tenant", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        is_enabled: typing.Union[MetaOapg.properties.is_enabled, bool, ],
        template: 'TemplateFields',
        name: typing.Union[MetaOapg.properties.name, str, ],
        application_type: typing.Union['ApplicationType', schemas.Unset] = schemas.unset,
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        tenant: typing.Union[MetaOapg.properties.tenant, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'AccountTemplate':
        return super().__new__(
            cls,
            *_args,
            is_enabled=is_enabled,
            template=template,
            name=name,
            application_type=application_type,
            description=description,
            id=id,
            tenant=tenant,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.application_type import ApplicationType
from synctera_client.model.template_fields import TemplateFields
