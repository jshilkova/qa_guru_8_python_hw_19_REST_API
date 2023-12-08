import json
import logging

import allure
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have

API_BASE_URL = 'https://demowebshop.tricentis.com'
WEB_BASE_URL = 'https://demowebshop.tricentis.com'


def demowebshop_api_post(url, **kwargs):
    with step("API POST Request"):
        result = requests.post(url=API_BASE_URL + url, **kwargs)

        allure.attach(body=result.request.url, name="Request url",
                      attachment_type=AttachmentType.TEXT)
        allure.attach(body=json.dumps(result.request.body, indent=4, ensure_ascii=True), name="Request body",
                      attachment_type=AttachmentType.JSON, extension="json")

        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

        logging.info("Request: " + result.request.url)
        if result.request.body:
            logging.info("INFO Request body: " + result.request.body)
        logging.info("Request headers: " + str(result.request.headers))
        logging.info("Response code " + str(result.status_code))
        logging.info("Response: " + result.text)
    return result


def test_add_to_cart_from_catalog_with_api(browser_setup):
    response = demowebshop_api_post('/addproducttocart/catalog/22/1/1')
    cookie = response.cookies.get("Nop.customer")

    with step("Set cookie from API"):
        browser.open('/')

        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    with step("Open cart"):
        browser.open('/cart')

    with step("Check one item presents"):
        browser.all('.cart-item-row').should(have.size(1))
        (browser.all('.cart-item-row').element_by(have.text('Health Book'))
         .element('[name^="itemquantity"]').should(have.value("1")))


def test_add_4_items_to_cart_with_api():
    browser.config.base_url = 'https://demowebshop.tricentis.com'
    response = demowebshop_api_post('/addproducttocart/details/45/1', data={"addtocart_45.EnteredQuantity": 4})
    cookie = response.cookies.get("Nop.customer")

    with step("Set cookie from API"):
        browser.open('/')
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    with step("Open cart"):
        browser.open('/cart')

    with step("Check four items present"):
        browser.all('.cart-item-row').should(have.size(1))
        (browser.all('.cart-item-row').element_by(have.text('Fiction'))
         .element('[name^="itemquantity"]').should(have.value("4")))


def test_add_different_items_to_cart_with_api():
    browser.config.base_url = 'https://demowebshop.tricentis.com'
    response = demowebshop_api_post('/addproducttocart/details/28/1',
                                    data={"product_attribute_28_7_10": 25,
                                          "product_attribute_28_1_11": 31,
                                          "addtocart_28.EnteredQuantity": 4})
    cookie = response.cookies.get("Nop.customer")
    demowebshop_api_post('/addproducttocart/details/45/1',
                         data={"addtocart_45.EnteredQuantity": 1},
                         cookies={"Nop.customer": cookie})

    with step("Set cookie from API"):
        browser.open('/')
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    with step("Open cart"):
        browser.open('/cart')

    with step("Check two items present"):
        browser.all('.cart-item-row').should(have.size(2))
        (browser.all('.cart-item-row').element_by(have.text('Fiction'))
         .element('[name^="itemquantity"]').should(have.value("1")))
        (browser.all('.cart-item-row').element_by(have.text('Blue and green Sneaker'))
         .element('[name^="itemquantity"]').should(have.value("4")))
    with step("Check total"):
        browser.element('.order-total').should(have.exact_text("68.00"))
