# coding: utf-8

"""
    Synctera API

    <h2>Let's build something great.</h2><p>Welcome to the official reference documentation for Synctera APIs. Our APIs are the best way to automate your company's banking needs and are designed to be easy to understand and implement.</p><p>We're continuously growing this library and what you see here is just the start, but if you need something specific or have a question, <a class='text-blue-600' href='https://synctera.com/contact' target='_blank' rel='noreferrer'>contact us</a>.</p>   # noqa: E501

    The version of the OpenAPI document: 0.35.0
    Generated by: https://openapi-generator.tech
"""

from synctera_client.paths.cash_pickups.post import CreateCashPickup
from synctera_client.paths.cash_pickups_cash_pickup_id.get import GetCashPickup
from synctera_client.paths.cash_pickups.get import ListCashPickups
from synctera_client.paths.cash_pickups_cash_pickup_id.patch import PatchCashPickup


class CashPickupsAlphaApi(
    CreateCashPickup,
    GetCashPickup,
    ListCashPickups,
    PatchCashPickup,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
