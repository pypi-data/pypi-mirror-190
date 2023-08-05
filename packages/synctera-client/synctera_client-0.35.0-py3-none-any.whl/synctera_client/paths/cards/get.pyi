# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

from dataclasses import dataclass
import typing_extensions
import urllib3
from urllib3._collections import HTTPHeaderDict

from synctera_client import api_client, exceptions
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

from synctera_client.model.error import Error
from synctera_client.model.card_status import CardStatus
from synctera_client.model.card_brand import CardBrand
from synctera_client.model.card_list_response import CardListResponse
from synctera_client.model.form import Form

# Query params
TenantSchema = schemas.StrSchema
CustomerIdSchema = schemas.UUIDSchema


class AccountIdSchema(
    schemas.ListSchema
):


    class MetaOapg:
        items = schemas.UUIDSchema

    def __new__(
        cls,
        _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, uuid.UUID, ]], typing.List[typing.Union[MetaOapg.items, str, uuid.UUID, ]]],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'AccountIdSchema':
        return super().__new__(
            cls,
            _arg,
            _configuration=_configuration,
        )

    def __getitem__(self, i: int) -> MetaOapg.items:
        return super().__getitem__(i)
EmbossNameSchema = schemas.StrSchema


class LastFourSchema(
    schemas.StrSchema
):
    pass
ExpirationDateSchema = schemas.DateSchema


class CardTypeSchema(
    schemas.EnumBase,
    schemas.StrSchema
):
    
    @schemas.classproperty
    def DEBIT(cls):
        return cls("DEBIT")
CardBrandSchema = CardBrand
FormSchema = Form
CardProductIdSchema = schemas.UUIDSchema
CardStatusSchema = CardStatus
PostalCodeSchema = schemas.StrSchema


class LimitSchema(
    schemas.IntSchema
):
    pass
PageTokenSchema = schemas.StrSchema


class SortBySchema(
    schemas.ListSchema
):


    class MetaOapg:
        
        
        class items(
            schemas.EnumBase,
            schemas.StrSchema
        ):
            
            @schemas.classproperty
            def ACCOUNT_IDASC(cls):
                return cls("account_id:asc")
            
            @schemas.classproperty
            def ACCOUNT_IDDESC(cls):
                return cls("account_id:desc")
            
            @schemas.classproperty
            def CUSTOMER_IDASC(cls):
                return cls("customer_id:asc")
            
            @schemas.classproperty
            def CUSTOMER_IDDESC(cls):
                return cls("customer_id:desc")
            
            @schemas.classproperty
            def CARD_PRODUCT_IDASC(cls):
                return cls("card_product_id:asc")
            
            @schemas.classproperty
            def CARD_PRODUCT_IDDESC(cls):
                return cls("card_product_id:desc")
            
            @schemas.classproperty
            def LAST_FOURASC(cls):
                return cls("last_four:asc")
            
            @schemas.classproperty
            def LAST_FOURDESC(cls):
                return cls("last_four:desc")
            
            @schemas.classproperty
            def CARD_TYPEASC(cls):
                return cls("card_type:asc")
            
            @schemas.classproperty
            def CARD_TYPEDESC(cls):
                return cls("card_type:desc")
            
            @schemas.classproperty
            def CARD_BRANDASC(cls):
                return cls("card_brand:asc")
            
            @schemas.classproperty
            def CARD_BRANDDESC(cls):
                return cls("card_brand:desc")
            
            @schemas.classproperty
            def EXPIRATION_DATEASC(cls):
                return cls("expiration_date:asc")
            
            @schemas.classproperty
            def EXPIRATION_DATEDESC(cls):
                return cls("expiration_date:desc")
            
            @schemas.classproperty
            def FORMASC(cls):
                return cls("form:asc")
            
            @schemas.classproperty
            def FORMDESC(cls):
                return cls("form:desc")
            
            @schemas.classproperty
            def CARD_STATUSASC(cls):
                return cls("card_status:asc")
            
            @schemas.classproperty
            def CARD_STATUSDESC(cls):
                return cls("card_status:desc")

    def __new__(
        cls,
        _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'SortBySchema':
        return super().__new__(
            cls,
            _arg,
            _configuration=_configuration,
        )

    def __getitem__(self, i: int) -> MetaOapg.items:
        return super().__getitem__(i)
RequestRequiredQueryParams = typing_extensions.TypedDict(
    'RequestRequiredQueryParams',
    {
    }
)
RequestOptionalQueryParams = typing_extensions.TypedDict(
    'RequestOptionalQueryParams',
    {
        'tenant': typing.Union[TenantSchema, str, ],
        'customer_id': typing.Union[CustomerIdSchema, str, uuid.UUID, ],
        'account_id': typing.Union[AccountIdSchema, list, tuple, ],
        'emboss_name': typing.Union[EmbossNameSchema, str, ],
        'last_four': typing.Union[LastFourSchema, str, ],
        'expiration_date': typing.Union[ExpirationDateSchema, str, date, ],
        'card_type': typing.Union[CardTypeSchema, str, ],
        'card_brand': typing.Union[CardBrandSchema, ],
        'form': typing.Union[FormSchema, ],
        'card_product_id': typing.Union[CardProductIdSchema, str, uuid.UUID, ],
        'card_status': typing.Union[CardStatusSchema, ],
        'postal_code': typing.Union[PostalCodeSchema, str, ],
        'limit': typing.Union[LimitSchema, decimal.Decimal, int, ],
        'page_token': typing.Union[PageTokenSchema, str, ],
        'sort_by': typing.Union[SortBySchema, list, tuple, ],
    },
    total=False
)


class RequestQueryParams(RequestRequiredQueryParams, RequestOptionalQueryParams):
    pass


request_query_tenant = api_client.QueryParameter(
    name="tenant",
    style=api_client.ParameterStyle.FORM,
    schema=TenantSchema,
    explode=True,
)
request_query_customer_id = api_client.QueryParameter(
    name="customer_id",
    style=api_client.ParameterStyle.FORM,
    schema=CustomerIdSchema,
    explode=True,
)
request_query_account_id = api_client.QueryParameter(
    name="account_id",
    style=api_client.ParameterStyle.FORM,
    schema=AccountIdSchema,
)
request_query_emboss_name = api_client.QueryParameter(
    name="emboss_name",
    style=api_client.ParameterStyle.FORM,
    schema=EmbossNameSchema,
    explode=True,
)
request_query_last_four = api_client.QueryParameter(
    name="last_four",
    style=api_client.ParameterStyle.FORM,
    schema=LastFourSchema,
    explode=True,
)
request_query_expiration_date = api_client.QueryParameter(
    name="expiration_date",
    style=api_client.ParameterStyle.FORM,
    schema=ExpirationDateSchema,
    explode=True,
)
request_query_card_type = api_client.QueryParameter(
    name="card_type",
    style=api_client.ParameterStyle.FORM,
    schema=CardTypeSchema,
    explode=True,
)
request_query_card_brand = api_client.QueryParameter(
    name="card_brand",
    style=api_client.ParameterStyle.FORM,
    schema=CardBrandSchema,
    explode=True,
)
request_query_form = api_client.QueryParameter(
    name="form",
    style=api_client.ParameterStyle.FORM,
    schema=FormSchema,
    explode=True,
)
request_query_card_product_id = api_client.QueryParameter(
    name="card_product_id",
    style=api_client.ParameterStyle.FORM,
    schema=CardProductIdSchema,
    explode=True,
)
request_query_card_status = api_client.QueryParameter(
    name="card_status",
    style=api_client.ParameterStyle.FORM,
    schema=CardStatusSchema,
    explode=True,
)
request_query_postal_code = api_client.QueryParameter(
    name="postal_code",
    style=api_client.ParameterStyle.FORM,
    schema=PostalCodeSchema,
    explode=True,
)
request_query_limit = api_client.QueryParameter(
    name="limit",
    style=api_client.ParameterStyle.FORM,
    schema=LimitSchema,
    explode=True,
)
request_query_page_token = api_client.QueryParameter(
    name="page_token",
    style=api_client.ParameterStyle.FORM,
    schema=PageTokenSchema,
    explode=True,
)
request_query_sort_by = api_client.QueryParameter(
    name="sort_by",
    style=api_client.ParameterStyle.FORM,
    schema=SortBySchema,
)
SchemaFor201ResponseBodyApplicationJson = CardListResponse


@dataclass
class ApiResponseFor201(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor201ResponseBodyApplicationJson,
    ]
    headers: schemas.Unset = schemas.unset


_response_for_201 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor201,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor201ResponseBodyApplicationJson),
    },
)
SchemaFor400ResponseBodyApplicationProblemjson = Error


@dataclass
class ApiResponseFor400(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor400ResponseBodyApplicationProblemjson,
    ]
    headers: schemas.Unset = schemas.unset


_response_for_400 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor400,
    content={
        'application/problem+json': api_client.MediaType(
            schema=SchemaFor400ResponseBodyApplicationProblemjson),
    },
)
SchemaFor401ResponseBodyApplicationProblemjson = Error


@dataclass
class ApiResponseFor401(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor401ResponseBodyApplicationProblemjson,
    ]
    headers: schemas.Unset = schemas.unset


_response_for_401 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor401,
    content={
        'application/problem+json': api_client.MediaType(
            schema=SchemaFor401ResponseBodyApplicationProblemjson),
    },
)
SchemaFor403ResponseBodyApplicationProblemjson = Error


@dataclass
class ApiResponseFor403(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor403ResponseBodyApplicationProblemjson,
    ]
    headers: schemas.Unset = schemas.unset


_response_for_403 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor403,
    content={
        'application/problem+json': api_client.MediaType(
            schema=SchemaFor403ResponseBodyApplicationProblemjson),
    },
)
SchemaFor422ResponseBodyApplicationProblemjson = Error


@dataclass
class ApiResponseFor422(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor422ResponseBodyApplicationProblemjson,
    ]
    headers: schemas.Unset = schemas.unset


_response_for_422 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor422,
    content={
        'application/problem+json': api_client.MediaType(
            schema=SchemaFor422ResponseBodyApplicationProblemjson),
    },
)
SchemaFor500ResponseBodyApplicationProblemjson = Error


@dataclass
class ApiResponseFor500(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor500ResponseBodyApplicationProblemjson,
    ]
    headers: schemas.Unset = schemas.unset


_response_for_500 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor500,
    content={
        'application/problem+json': api_client.MediaType(
            schema=SchemaFor500ResponseBodyApplicationProblemjson),
    },
)
_all_accept_content_types = (
    'application/json',
    'application/problem+json',
)


class BaseApi(api_client.Api):
    @typing.overload
    def _list_cards_oapg(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[
        ApiResponseFor201,
    ]: ...

    @typing.overload
    def _list_cards_oapg(
        self,
        skip_deserialization: typing_extensions.Literal[True],
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> api_client.ApiResponseWithoutDeserialization: ...

    @typing.overload
    def _list_cards_oapg(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = ...,
    ) -> typing.Union[
        ApiResponseFor201,
        api_client.ApiResponseWithoutDeserialization,
    ]: ...

    def _list_cards_oapg(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = False,
    ):
        """
        List Cards
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        self._verify_typed_dict_inputs_oapg(RequestQueryParams, query_params)
        used_path = path.value

        prefix_separator_iterator = None
        for parameter in (
            request_query_tenant,
            request_query_customer_id,
            request_query_account_id,
            request_query_emboss_name,
            request_query_last_four,
            request_query_expiration_date,
            request_query_card_type,
            request_query_card_brand,
            request_query_form,
            request_query_card_product_id,
            request_query_card_status,
            request_query_postal_code,
            request_query_limit,
            request_query_page_token,
            request_query_sort_by,
        ):
            parameter_data = query_params.get(parameter.name, schemas.unset)
            if parameter_data is schemas.unset:
                continue
            if prefix_separator_iterator is None:
                prefix_separator_iterator = parameter.get_prefix_separator_iterator()
            serialized_data = parameter.serialize(parameter_data, prefix_separator_iterator)
            for serialized_value in serialized_data.values():
                used_path += serialized_value

        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)

        response = self.api_client.call_api(
            resource_path=used_path,
            method='get'.upper(),
            headers=_headers,
            auth_settings=_auth,
            stream=stream,
            timeout=timeout,
        )

        if skip_deserialization:
            api_response = api_client.ApiResponseWithoutDeserialization(response=response)
        else:
            response_for_status = _status_code_to_response.get(str(response.status))
            if response_for_status:
                api_response = response_for_status.deserialize(response, self.api_client.configuration)
            else:
                api_response = api_client.ApiResponseWithoutDeserialization(response=response)

        if not 200 <= response.status <= 299:
            raise exceptions.ApiException(
                status=response.status,
                reason=response.reason,
                api_response=api_response
            )

        return api_response


class ListCards(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    @typing.overload
    def list_cards(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[
        ApiResponseFor201,
    ]: ...

    @typing.overload
    def list_cards(
        self,
        skip_deserialization: typing_extensions.Literal[True],
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> api_client.ApiResponseWithoutDeserialization: ...

    @typing.overload
    def list_cards(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = ...,
    ) -> typing.Union[
        ApiResponseFor201,
        api_client.ApiResponseWithoutDeserialization,
    ]: ...

    def list_cards(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = False,
    ):
        return self._list_cards_oapg(
            query_params=query_params,
            accept_content_types=accept_content_types,
            stream=stream,
            timeout=timeout,
            skip_deserialization=skip_deserialization
        )


class ApiForget(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    @typing.overload
    def get(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[
        ApiResponseFor201,
    ]: ...

    @typing.overload
    def get(
        self,
        skip_deserialization: typing_extensions.Literal[True],
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> api_client.ApiResponseWithoutDeserialization: ...

    @typing.overload
    def get(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = ...,
    ) -> typing.Union[
        ApiResponseFor201,
        api_client.ApiResponseWithoutDeserialization,
    ]: ...

    def get(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = False,
    ):
        return self._list_cards_oapg(
            query_params=query_params,
            accept_content_types=accept_content_types,
            stream=stream,
            timeout=timeout,
            skip_deserialization=skip_deserialization
        )


