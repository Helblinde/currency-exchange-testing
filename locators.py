from selenium.webdriver.common.by import By


class ConverterPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    INPUT_FIELD = (By.XPATH, "//input[@placeholder='Сумма']")
    FROM_TYPE_CASH = (By.XPATH, "//p[text()='Наличные']")
    TO_TYPE_CASH = (By.XPATH, "//p[text()='Выдать наличные']")
    SUBMIT_BUTTON = (By.XPATH, "//aside[@class='rates-aside']//"
                               "button[text()='Показать']")
    RESULT_VALUE = (By.XPATH, "//div[@class='converter-result']/h4/span[1]")
    RESULT_CURRENCY = (By.XPATH, "//div[@class='converter-result']/h4/span[2]")
    BUY_EXCHANGE_RATE = (By.XPATH, "//div[@class='current-table']/table/tbody/"
                                   "tr/td[3]/span")
    SELL_EXCHANGE_RATE = (By.XPATH, "//div[@class='current-table']/table/tbody/"
                                    "tr/td[4]/span")
    FROM_CURRENCY_FIELD = (By.XPATH, "//aside[@class='rates-aside']/div[1]/div[1]/"
                                     "div[3]/div[2]")
    TO_CURRENCY_FIELD = (By.XPATH, "//aside[@class='rates-aside']/div[1]/div[1]/"
                                   "div[4]/div[2]")
    FROM_CURRENCY_LIST_ELEMENT = (By.XPATH, "//aside[@class='rates-aside']/div/div/"
                                            "div[3]/div[2]/div/div/span[%d]")
    TO_CURRENCY_LIST_ELEMENT = (By.XPATH, "//aside[@class='rates-aside']/div/div/"
                                          "div[4]/div[2]/div/div/span[%d]")
    CONVERTER_FROM_SELECT = (By.NAME, "converterFrom")
    CONVERTER_TO_SELECT = (By.NAME, "converterTo")

    # dictionary of all available currencies and their corresponding
    # index number in the list of currencies on the converter's page
    CURRENCIES = {'RUR': 1, 'CHF': 2, 'EUR': 3, 'GBP': 4, 'JPY': 5, 'USD': 6}
