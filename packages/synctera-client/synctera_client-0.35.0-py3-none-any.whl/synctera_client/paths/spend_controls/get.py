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
from synctera_client.model.payment_type import PaymentType
from synctera_client.model.spend_control_response_list import SpendControlResponseList
from synctera_client.model.spend_control_direction import SpendControlDirection

from . import path

# Query params
AccountIdSchema = schemas.UUIDSchema
PaymentTypeSchema = PaymentType


class AmountLimitSchema(
    schemas.Int64Schema
):


    class MetaOapg:
        format = 'int64'
        exclusive_minimuminclusive_minimum = 0


class AmountLimitGteSchema(
    schemas.IntSchema
):


    class MetaOapg:
        exclusive_minimuminclusive_minimum = 0


class AmountLimitLteSchema(
    schemas.IntSchema
):


    class MetaOapg:
        exclusive_minimuminclusive_minimum = 0


class NumRelatedAccountsSchema(
    schemas.IntSchema
):


    class MetaOapg:
        inclusive_minimum = 0


class NumRelatedAccountsGteSchema(
    schemas.IntSchema
):


    class MetaOapg:
        inclusive_minimum = 0


class NumRelatedAccountsLteSchema(
    schemas.IntSchema
):


    class MetaOapg:
        inclusive_minimum = 0
IsActiveSchema = schemas.BoolSchema
NameSchema = schemas.StrSchema
DirectionSchema = SpendControlDirection
TenantSchema = schemas.StrSchema


class IdSchema(
    schemas.ListSchema
):


    class MetaOapg:
        items = schemas.UUIDSchema

    def __new__(
        cls,
        _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, uuid.UUID, ]], typing.List[typing.Union[MetaOapg.items, str, uuid.UUID, ]]],
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'IdSchema':
        return super().__new__(
            cls,
            _arg,
            _configuration=_configuration,
        )

    def __getitem__(self, i: int) -> MetaOapg.items:
        return super().__getitem__(i)


class SortBySchema(
    schemas.ListSchema
):


    class MetaOapg:
        
        
        class items(
            schemas.EnumBase,
            schemas.StrSchema
        ):
        
        
            class MetaOapg:
                enum_value_to_name = {
                    "name:asc": "NAMEASC",
                    "name:desc": "NAMEDESC",
                    "num_related_accounts:asc": "NUM_RELATED_ACCOUNTSASC",
                    "num_related_accounts:desc": "NUM_RELATED_ACCOUNTSDESC",
                    "amount_limit:asc": "AMOUNT_LIMITASC",
                    "amount_limit:desc": "AMOUNT_LIMITDESC",
                    "last_modified_time:asc": "LAST_MODIFIED_TIMEASC",
                    "last_modified_time:desc": "LAST_MODIFIED_TIMEDESC",
                    "is_active:asc": "IS_ACTIVEASC",
                    "is_active:desc": "IS_ACTIVEDESC",
                }
            
            @schemas.classproperty
            def NAMEASC(cls):
                return cls("name:asc")
            
            @schemas.classproperty
            def NAMEDESC(cls):
                return cls("name:desc")
            
            @schemas.classproperty
            def NUM_RELATED_ACCOUNTSASC(cls):
                return cls("num_related_accounts:asc")
            
            @schemas.classproperty
            def NUM_RELATED_ACCOUNTSDESC(cls):
                return cls("num_related_accounts:desc")
            
            @schemas.classproperty
            def AMOUNT_LIMITASC(cls):
                return cls("amount_limit:asc")
            
            @schemas.classproperty
            def AMOUNT_LIMITDESC(cls):
                return cls("amount_limit:desc")
            
            @schemas.classproperty
            def LAST_MODIFIED_TIMEASC(cls):
                return cls("last_modified_time:asc")
            
            @schemas.classproperty
            def LAST_MODIFIED_TIMEDESC(cls):
                return cls("last_modified_time:desc")
            
            @schemas.classproperty
            def IS_ACTIVEASC(cls):
                return cls("is_active:asc")
            
            @schemas.classproperty
            def IS_ACTIVEDESC(cls):
                return cls("is_active:desc")

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
        'account_id': typing.Union[AccountIdSchema, str, uuid.UUID, ],
        'payment_type': typing.Union[PaymentTypeSchema, ],
        'amount_limit': typing.Union[AmountLimitSchema, decimal.Decimal, int, ],
        'amount_limit_gte': typing.Union[AmountLimitGteSchema, decimal.Decimal, int, ],
        'amount_limit_lte': typing.Union[AmountLimitLteSchema, decimal.Decimal, int, ],
        'num_related_accounts': typing.Union[NumRelatedAccountsSchema, decimal.Decimal, int, ],
        'num_related_accounts_gte': typing.Union[NumRelatedAccountsGteSchema, decimal.Decimal, int, ],
        'num_related_accounts_lte': typing.Union[NumRelatedAccountsLteSchema, decimal.Decimal, int, ],
        'is_active': typing.Union[IsActiveSchema, bool, ],
        'name': typing.Union[NameSchema, str, ],
        'direction': typing.Union[DirectionSchema, ],
        'tenant': typing.Union[TenantSchema, str, ],
        'id': typing.Union[IdSchema, list, tuple, ],
        'sort_by': typing.Union[SortBySchema, list, tuple, ],
    },
    total=False
)


class RequestQueryParams(RequestRequiredQueryParams, RequestOptionalQueryParams):
    pass


request_query_account_id = api_client.QueryParameter(
    name="account_id",
    style=api_client.ParameterStyle.FORM,
    schema=AccountIdSchema,
    explode=True,
)
request_query_payment_type = api_client.QueryParameter(
    name="payment_type",
    style=api_client.ParameterStyle.FORM,
    schema=PaymentTypeSchema,
    explode=True,
)
request_query_amount_limit = api_client.QueryParameter(
    name="amount_limit",
    style=api_client.ParameterStyle.FORM,
    schema=AmountLimitSchema,
    explode=True,
)
request_query_amount_limit_gte = api_client.QueryParameter(
    name="amount_limit_gte",
    style=api_client.ParameterStyle.FORM,
    schema=AmountLimitGteSchema,
    explode=True,
)
request_query_amount_limit_lte = api_client.QueryParameter(
    name="amount_limit_lte",
    style=api_client.ParameterStyle.FORM,
    schema=AmountLimitLteSchema,
    explode=True,
)
request_query_num_related_accounts = api_client.QueryParameter(
    name="num_related_accounts",
    style=api_client.ParameterStyle.FORM,
    schema=NumRelatedAccountsSchema,
    explode=True,
)
request_query_num_related_accounts_gte = api_client.QueryParameter(
    name="num_related_accounts_gte",
    style=api_client.ParameterStyle.FORM,
    schema=NumRelatedAccountsGteSchema,
    explode=True,
)
request_query_num_related_accounts_lte = api_client.QueryParameter(
    name="num_related_accounts_lte",
    style=api_client.ParameterStyle.FORM,
    schema=NumRelatedAccountsLteSchema,
    explode=True,
)
request_query_is_active = api_client.QueryParameter(
    name="is_active",
    style=api_client.ParameterStyle.FORM,
    schema=IsActiveSchema,
    explode=True,
)
request_query_name = api_client.QueryParameter(
    name="name",
    style=api_client.ParameterStyle.FORM,
    schema=NameSchema,
    explode=True,
)
request_query_direction = api_client.QueryParameter(
    name="direction",
    style=api_client.ParameterStyle.FORM,
    schema=DirectionSchema,
    explode=True,
)
request_query_tenant = api_client.QueryParameter(
    name="tenant",
    style=api_client.ParameterStyle.FORM,
    schema=TenantSchema,
    explode=True,
)
request_query_id = api_client.QueryParameter(
    name="id",
    style=api_client.ParameterStyle.FORM,
    schema=IdSchema,
)
request_query_sort_by = api_client.QueryParameter(
    name="sort_by",
    style=api_client.ParameterStyle.FORM,
    schema=SortBySchema,
)
_auth = [
    'bearerAuth',
]
SchemaFor200ResponseBodyApplicationJson = SpendControlResponseList


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[
        SchemaFor200ResponseBodyApplicationJson,
    ]
    headers: schemas.Unset = schemas.unset


_response_for_200 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor200,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor200ResponseBodyApplicationJson),
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
_status_code_to_response = {
    '200': _response_for_200,
    '400': _response_for_400,
    '401': _response_for_401,
    '403': _response_for_403,
    '422': _response_for_422,
    '500': _response_for_500,
}
_all_accept_content_types = (
    'application/json',
    'application/problem+json',
)


class BaseApi(api_client.Api):
    @typing.overload
    def _list_spend_controls_oapg(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[
        ApiResponseFor200,
    ]: ...

    @typing.overload
    def _list_spend_controls_oapg(
        self,
        skip_deserialization: typing_extensions.Literal[True],
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> api_client.ApiResponseWithoutDeserialization: ...

    @typing.overload
    def _list_spend_controls_oapg(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = ...,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]: ...

    def _list_spend_controls_oapg(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = False,
    ):
        """
        List Spend Controls
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        self._verify_typed_dict_inputs_oapg(RequestQueryParams, query_params)
        used_path = path.value

        prefix_separator_iterator = None
        for parameter in (
            request_query_account_id,
            request_query_payment_type,
            request_query_amount_limit,
            request_query_amount_limit_gte,
            request_query_amount_limit_lte,
            request_query_num_related_accounts,
            request_query_num_related_accounts_gte,
            request_query_num_related_accounts_lte,
            request_query_is_active,
            request_query_name,
            request_query_direction,
            request_query_tenant,
            request_query_id,
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


class ListSpendControls(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    @typing.overload
    def list_spend_controls(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: typing_extensions.Literal[False] = ...,
    ) -> typing.Union[
        ApiResponseFor200,
    ]: ...

    @typing.overload
    def list_spend_controls(
        self,
        skip_deserialization: typing_extensions.Literal[True],
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> api_client.ApiResponseWithoutDeserialization: ...

    @typing.overload
    def list_spend_controls(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = ...,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]: ...

    def list_spend_controls(
        self,
        query_params: RequestQueryParams = frozendict.frozendict(),
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = False,
    ):
        return self._list_spend_controls_oapg(
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
        ApiResponseFor200,
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
        ApiResponseFor200,
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
        return self._list_spend_controls_oapg(
            query_params=query_params,
            accept_content_types=accept_content_types,
            stream=stream,
            timeout=timeout,
            skip_deserialization=skip_deserialization
        )


