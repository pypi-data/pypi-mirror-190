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


class PatchPersonBusinessRelationship(
    schemas.ComposedBase,
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Denotes the relationship between specified person and business.
    """


    class MetaOapg:
        
        
        class all_of_0(
            schemas.AnyTypeSchema,
        ):
        
        
            class MetaOapg:
                required = {
                    "relationship_type",
                }
                
                class properties:
                
                    @staticmethod
                    def additional_data() -> typing.Type['AdditionalData']:
                        return AdditionalData
                    creation_time = schemas.DateTimeSchema
                    from_person_id = schemas.UUIDSchema
                    id = schemas.UUIDSchema
                    last_updated_time = schemas.DateTimeSchema
                    metadata = schemas.DictSchema
                    
                    
                    class relationship_type(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                    
                    
                        class MetaOapg:
                            format = 'enum'
                            enum_value_to_name = {
                                "BENEFICIAL_OWNER_OF": "BENEFICIAL_OWNER_OF",
                                "MANAGING_PERSON_OF": "MANAGING_PERSON_OF",
                                "OWNER_OF": "OWNER_OF",
                            }
                        
                        @schemas.classproperty
                        def BENEFICIAL_OWNER_OF(cls):
                            return cls("BENEFICIAL_OWNER_OF")
                        
                        @schemas.classproperty
                        def MANAGING_PERSON_OF(cls):
                            return cls("MANAGING_PERSON_OF")
                        
                        @schemas.classproperty
                        def OWNER_OF(cls):
                            return cls("OWNER_OF")
                    to_business_id = schemas.UUIDSchema
                    __annotations__ = {
                        "additional_data": additional_data,
                        "creation_time": creation_time,
                        "from_person_id": from_person_id,
                        "id": id,
                        "last_updated_time": last_updated_time,
                        "metadata": metadata,
                        "relationship_type": relationship_type,
                        "to_business_id": to_business_id,
                    }
        
            
            relationship_type: MetaOapg.properties.relationship_type
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["additional_data"]) -> 'AdditionalData': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["from_person_id"]) -> MetaOapg.properties.from_person_id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["relationship_type"]) -> MetaOapg.properties.relationship_type: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["to_business_id"]) -> MetaOapg.properties.to_business_id: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["additional_data", "creation_time", "from_person_id", "id", "last_updated_time", "metadata", "relationship_type", "to_business_id", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["additional_data"]) -> typing.Union['AdditionalData', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["from_person_id"]) -> typing.Union[MetaOapg.properties.from_person_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> typing.Union[MetaOapg.properties.last_updated_time, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["relationship_type"]) -> MetaOapg.properties.relationship_type: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["to_business_id"]) -> typing.Union[MetaOapg.properties.to_business_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["additional_data", "creation_time", "from_person_id", "id", "last_updated_time", "metadata", "relationship_type", "to_business_id", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                relationship_type: typing.Union[MetaOapg.properties.relationship_type, str, ],
                additional_data: typing.Union['AdditionalData', schemas.Unset] = schemas.unset,
                creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
                from_person_id: typing.Union[MetaOapg.properties.from_person_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, schemas.Unset] = schemas.unset,
                metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                to_business_id: typing.Union[MetaOapg.properties.to_business_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'all_of_0':
                return super().__new__(
                    cls,
                    *_args,
                    relationship_type=relationship_type,
                    additional_data=additional_data,
                    creation_time=creation_time,
                    from_person_id=from_person_id,
                    id=id,
                    last_updated_time=last_updated_time,
                    metadata=metadata,
                    to_business_id=to_business_id,
                    _configuration=_configuration,
                    **kwargs,
                )
        
        @classmethod
        @functools.lru_cache()
        def all_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                cls.all_of_0,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PatchPersonBusinessRelationship':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.additional_data import AdditionalData
