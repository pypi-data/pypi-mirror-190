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


class TemplateFieldsGenericResponse(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "account_type",
            "bank_country",
            "currency",
        }
        
        class properties:
        
            @staticmethod
            def account_type() -> typing.Type['AccountType']:
                return AccountType
            
            
            class bank_country(
                schemas.StrSchema
            ):
                pass
            
            
            class currency(
                schemas.StrSchema
            ):
                pass
        
            @staticmethod
            def balance_ceiling() -> typing.Type['BalanceCeiling']:
                return BalanceCeiling
        
            @staticmethod
            def balance_floor() -> typing.Type['BalanceFloor']:
                return BalanceFloor
        
            @staticmethod
            def billing_period() -> typing.Type['BillingPeriod']:
                return BillingPeriod
            
            
            class chargeoff_period(
                schemas.IntSchema
            ):
                pass
            
            
            class delinquency_period(
                schemas.IntSchema
            ):
                pass
            
            
            class fee_product_ids(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.UUIDSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, uuid.UUID, ]], typing.List[typing.Union[MetaOapg.items, str, uuid.UUID, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'fee_product_ids':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            
            
            class grace_period(
                schemas.IntSchema
            ):
                pass
            interest_product_id = schemas.UUIDSchema
            is_ach_enabled = schemas.BoolSchema
            is_card_enabled = schemas.BoolSchema
            is_p2p_enabled = schemas.BoolSchema
            is_wire_enabled = schemas.BoolSchema
        
            @staticmethod
            def minimum_payment() -> typing.Type['MinimumPayment']:
                return MinimumPayment
            
            
            class overdraft_limit(
                schemas.Int64Schema
            ):
                pass
        
            @staticmethod
            def spend_control_ids() -> typing.Type['SpendControlIds']:
                return SpendControlIds
        
            @staticmethod
            def spending_limits() -> typing.Type['SpendingLimits']:
                return SpendingLimits
            __annotations__ = {
                "account_type": account_type,
                "bank_country": bank_country,
                "currency": currency,
                "balance_ceiling": balance_ceiling,
                "balance_floor": balance_floor,
                "billing_period": billing_period,
                "chargeoff_period": chargeoff_period,
                "delinquency_period": delinquency_period,
                "fee_product_ids": fee_product_ids,
                "grace_period": grace_period,
                "interest_product_id": interest_product_id,
                "is_ach_enabled": is_ach_enabled,
                "is_card_enabled": is_card_enabled,
                "is_p2p_enabled": is_p2p_enabled,
                "is_wire_enabled": is_wire_enabled,
                "minimum_payment": minimum_payment,
                "overdraft_limit": overdraft_limit,
                "spend_control_ids": spend_control_ids,
                "spending_limits": spending_limits,
            }
    
    account_type: 'AccountType'
    bank_country: MetaOapg.properties.bank_country
    currency: MetaOapg.properties.currency
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_type"]) -> 'AccountType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bank_country"]) -> MetaOapg.properties.bank_country: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["balance_ceiling"]) -> 'BalanceCeiling': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["balance_floor"]) -> 'BalanceFloor': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["billing_period"]) -> 'BillingPeriod': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["chargeoff_period"]) -> MetaOapg.properties.chargeoff_period: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["delinquency_period"]) -> MetaOapg.properties.delinquency_period: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["fee_product_ids"]) -> MetaOapg.properties.fee_product_ids: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["grace_period"]) -> MetaOapg.properties.grace_period: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["interest_product_id"]) -> MetaOapg.properties.interest_product_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_ach_enabled"]) -> MetaOapg.properties.is_ach_enabled: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_card_enabled"]) -> MetaOapg.properties.is_card_enabled: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_p2p_enabled"]) -> MetaOapg.properties.is_p2p_enabled: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_wire_enabled"]) -> MetaOapg.properties.is_wire_enabled: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["minimum_payment"]) -> 'MinimumPayment': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["overdraft_limit"]) -> MetaOapg.properties.overdraft_limit: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["spend_control_ids"]) -> 'SpendControlIds': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["spending_limits"]) -> 'SpendingLimits': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["account_type", "bank_country", "currency", "balance_ceiling", "balance_floor", "billing_period", "chargeoff_period", "delinquency_period", "fee_product_ids", "grace_period", "interest_product_id", "is_ach_enabled", "is_card_enabled", "is_p2p_enabled", "is_wire_enabled", "minimum_payment", "overdraft_limit", "spend_control_ids", "spending_limits", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_type"]) -> 'AccountType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bank_country"]) -> MetaOapg.properties.bank_country: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["balance_ceiling"]) -> typing.Union['BalanceCeiling', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["balance_floor"]) -> typing.Union['BalanceFloor', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["billing_period"]) -> typing.Union['BillingPeriod', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["chargeoff_period"]) -> typing.Union[MetaOapg.properties.chargeoff_period, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["delinquency_period"]) -> typing.Union[MetaOapg.properties.delinquency_period, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["fee_product_ids"]) -> typing.Union[MetaOapg.properties.fee_product_ids, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["grace_period"]) -> typing.Union[MetaOapg.properties.grace_period, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["interest_product_id"]) -> typing.Union[MetaOapg.properties.interest_product_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_ach_enabled"]) -> typing.Union[MetaOapg.properties.is_ach_enabled, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_card_enabled"]) -> typing.Union[MetaOapg.properties.is_card_enabled, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_p2p_enabled"]) -> typing.Union[MetaOapg.properties.is_p2p_enabled, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_wire_enabled"]) -> typing.Union[MetaOapg.properties.is_wire_enabled, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["minimum_payment"]) -> typing.Union['MinimumPayment', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["overdraft_limit"]) -> typing.Union[MetaOapg.properties.overdraft_limit, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["spend_control_ids"]) -> typing.Union['SpendControlIds', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["spending_limits"]) -> typing.Union['SpendingLimits', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account_type", "bank_country", "currency", "balance_ceiling", "balance_floor", "billing_period", "chargeoff_period", "delinquency_period", "fee_product_ids", "grace_period", "interest_product_id", "is_ach_enabled", "is_card_enabled", "is_p2p_enabled", "is_wire_enabled", "minimum_payment", "overdraft_limit", "spend_control_ids", "spending_limits", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        account_type: 'AccountType',
        bank_country: typing.Union[MetaOapg.properties.bank_country, str, ],
        currency: typing.Union[MetaOapg.properties.currency, str, ],
        balance_ceiling: typing.Union['BalanceCeiling', schemas.Unset] = schemas.unset,
        balance_floor: typing.Union['BalanceFloor', schemas.Unset] = schemas.unset,
        billing_period: typing.Union['BillingPeriod', schemas.Unset] = schemas.unset,
        chargeoff_period: typing.Union[MetaOapg.properties.chargeoff_period, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        delinquency_period: typing.Union[MetaOapg.properties.delinquency_period, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        fee_product_ids: typing.Union[MetaOapg.properties.fee_product_ids, list, tuple, schemas.Unset] = schemas.unset,
        grace_period: typing.Union[MetaOapg.properties.grace_period, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        interest_product_id: typing.Union[MetaOapg.properties.interest_product_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        is_ach_enabled: typing.Union[MetaOapg.properties.is_ach_enabled, bool, schemas.Unset] = schemas.unset,
        is_card_enabled: typing.Union[MetaOapg.properties.is_card_enabled, bool, schemas.Unset] = schemas.unset,
        is_p2p_enabled: typing.Union[MetaOapg.properties.is_p2p_enabled, bool, schemas.Unset] = schemas.unset,
        is_wire_enabled: typing.Union[MetaOapg.properties.is_wire_enabled, bool, schemas.Unset] = schemas.unset,
        minimum_payment: typing.Union['MinimumPayment', schemas.Unset] = schemas.unset,
        overdraft_limit: typing.Union[MetaOapg.properties.overdraft_limit, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        spend_control_ids: typing.Union['SpendControlIds', schemas.Unset] = schemas.unset,
        spending_limits: typing.Union['SpendingLimits', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TemplateFieldsGenericResponse':
        return super().__new__(
            cls,
            *_args,
            account_type=account_type,
            bank_country=bank_country,
            currency=currency,
            balance_ceiling=balance_ceiling,
            balance_floor=balance_floor,
            billing_period=billing_period,
            chargeoff_period=chargeoff_period,
            delinquency_period=delinquency_period,
            fee_product_ids=fee_product_ids,
            grace_period=grace_period,
            interest_product_id=interest_product_id,
            is_ach_enabled=is_ach_enabled,
            is_card_enabled=is_card_enabled,
            is_p2p_enabled=is_p2p_enabled,
            is_wire_enabled=is_wire_enabled,
            minimum_payment=minimum_payment,
            overdraft_limit=overdraft_limit,
            spend_control_ids=spend_control_ids,
            spending_limits=spending_limits,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.account_type import AccountType
from synctera_client.model.balance_ceiling import BalanceCeiling
from synctera_client.model.balance_floor import BalanceFloor
from synctera_client.model.billing_period import BillingPeriod
from synctera_client.model.minimum_payment import MinimumPayment
from synctera_client.model.spend_control_ids import SpendControlIds
from synctera_client.model.spending_limits import SpendingLimits
