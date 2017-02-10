from selenium.webdriver.common.by import By


class ConverterPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    INPUT_FIELD = (By.XPATH, "//aside//input")
    FROM_TYPE_CASH = (By.XPATH, "//p[text()='Наличные']")
    TO_TYPE_CASH = (By.XPATH, "//p[text()='Выдать наличные']")
    SUBMIT_BUTTON = (By.XPATH, "//aside//button")
    RESULT_VALUE = (By.XPATH, "//h4/span[1]")
    RESULT_CURRENCY = (By.XPATH, "//h4/span[2]")
    BUY_EXCHANGE_RATE = (By.XPATH, "//td[3]/span")
    SELL_EXCHANGE_RATE = (By.XPATH, "//td[4]/span")
    FROM_CURRENCY_FIELD = (By.XPATH, "//select[@name='converterFrom']/parent::div")
    TO_CURRENCY_FIELD = (By.XPATH, "//select[@name='converterTo']/parent::div")
    FROM_CURRENCY_LIST_ELEMENT = (By.XPATH, "//select[@name='converterFrom']/"
                                            "following-sibling::div/*/span[%d]")
    TO_CURRENCY_LIST_ELEMENT = (By.XPATH, "//select[@name='converterTo']/"
                                          "following-sibling::div/*/span[%d]")
    CONVERTER_FROM_SELECT = (By.NAME, "converterFrom")
    CONVERTER_TO_SELECT = (By.NAME, "converterTo")

    # dictionary of all available currencies and their corresponding
    # index number in the list of currencies on the converter's page
    CURRENCIES = {'RUR': 1, 'CHF': 2, 'EUR': 3, 'GBP': 4, 'JPY': 5, 'USD': 6}
