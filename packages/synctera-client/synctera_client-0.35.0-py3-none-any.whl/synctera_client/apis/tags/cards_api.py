# coding: utf-8

"""
    Synctera API

    <h2>Let's build something great.</h2><p>Welcome to the official reference documentation for Synctera APIs. Our APIs are the best way to automate your company's banking needs and are designed to be easy to understand and implement.</p><p>We're continuously growing this library and what you see here is just the start, but if you need something specific or have a question, <a class='text-blue-600' href='https://synctera.com/contact' target='_blank' rel='noreferrer'>contact us</a>.</p>   # noqa: E501

    The version of the OpenAPI document: 0.35.0
    Generated by: https://openapi-generator.tech
"""

from synctera_client.paths.cards_activate.post import ActivateCard
from synctera_client.paths.cards_images.post import CreateCardImage
from synctera_client.paths.cards_gateways.post import CreateGateway
from synctera_client.paths.cards_card_id.get import GetCard
from synctera_client.paths.cards_card_id_barcodes.get import GetCardBarcode
from synctera_client.paths.cards_images_card_image_id_data.get import GetCardImageData
from synctera_client.paths.cards_images_card_image_id.get import GetCardImageDetails
from synctera_client.paths.cards_card_widget_url.get import GetCardWidgetUrl
from synctera_client.paths.cards_card_id_client_token.post import GetClientAccessToken
from synctera_client.paths.cards_single_use_token.post import GetClientSingleUseToken
from synctera_client.paths.cards_gateways_gateway_id.get import GetGateway
from synctera_client.paths.cards.post import IssueCard
from synctera_client.paths.cards_images.get import ListCardImageDetails
from synctera_client.paths.cards_products.get import ListCardProducts
from synctera_client.paths.cards.get import ListCards
from synctera_client.paths.cards_card_id_changes.get import ListChanges
from synctera_client.paths.cards_gateways.get import ListGateways
from synctera_client.paths.cards_card_id.patch import UpdateCard
from synctera_client.paths.cards_images_card_image_id.patch import UpdateCardImageDetails
from synctera_client.paths.cards_gateways_gateway_id.patch import UpdateGateway
from synctera_client.paths.cards_images_card_image_id_data.post import UploadCardImageData


class CardsApi(
    ActivateCard,
    CreateCardImage,
    CreateGateway,
    GetCard,
    GetCardBarcode,
    GetCardImageData,
    GetCardImageDetails,
    GetCardWidgetUrl,
    GetClientAccessToken,
    GetClientSingleUseToken,
    GetGateway,
    IssueCard,
    ListCardImageDetails,
    ListCardProducts,
    ListCards,
    ListChanges,
    ListGateways,
    UpdateCard,
    UpdateCardImageDetails,
    UpdateGateway,
    UploadCardImageData,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
