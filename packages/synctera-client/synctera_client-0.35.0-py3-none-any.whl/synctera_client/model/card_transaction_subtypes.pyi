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


class CardTransactionSubtypes(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    The set of valid CARD transaction subtypes
    """
    
    @schemas.classproperty
    def ATM_WITHDRAWAL(cls):
        return cls("ATM_WITHDRAWAL")
    
    @schemas.classproperty
    def ATM_WITHDRAWAL_REVERSAL(cls):
        return cls("ATM_WITHDRAWAL_REVERSAL")
    
    @schemas.classproperty
    def BALANCE_INQUIRY(cls):
        return cls("BALANCE_INQUIRY")
    
    @schemas.classproperty
    def CARD_TRANSACTION(cls):
        return cls("CARD_TRANSACTION")
    
    @schemas.classproperty
    def CARD_TRANSACTION_REVERSAL(cls):
        return cls("CARD_TRANSACTION_REVERSAL")
    
    @schemas.classproperty
    def CREDIT(cls):
        return cls("CREDIT")
    
    @schemas.classproperty
    def CREDIT_REVERSAL(cls):
        return cls("CREDIT_REVERSAL")
    
    @schemas.classproperty
    def DIRECTPOST(cls):
        return cls("DIRECTPOST")
    
    @schemas.classproperty
    def DIRECTPOST_REVERSAL(cls):
        return cls("DIRECTPOST_REVERSAL")
    
    @schemas.classproperty
    def POS_CASHBACK(cls):
        return cls("POS_CASHBACK")
    
    @schemas.classproperty
    def POS_CASHBACK_REVERSAL(cls):
        return cls("POS_CASHBACK_REVERSAL")
    
    @schemas.classproperty
    def POS_PURCHASE(cls):
        return cls("POS_PURCHASE")
    
    @schemas.classproperty
    def POS_PURCHASE_REFUND(cls):
        return cls("POS_PURCHASE_REFUND")
    
    @schemas.classproperty
    def POS_PURCHASE_REFUND_REVERSAL(cls):
        return cls("POS_PURCHASE_REFUND_REVERSAL")
    
    @schemas.classproperty
    def POS_PURCHASE_REVERSAL(cls):
        return cls("POS_PURCHASE_REVERSAL")
    
    @schemas.classproperty
    def POS_REFUND(cls):
        return cls("POS_REFUND")
    
    @schemas.classproperty
    def POS_REFUND_REVERSAL(cls):
        return cls("POS_REFUND_REVERSAL")
    
    @schemas.classproperty
    def PROVISIONAL_CREDIT(cls):
        return cls("PROVISIONAL_CREDIT")
    
    @schemas.classproperty
    def PROVISIONAL_CREDIT_REVERSAL(cls):
        return cls("PROVISIONAL_CREDIT_REVERSAL")
