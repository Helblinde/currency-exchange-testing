from selenium.webdriver.support.ui import WebDriverWait
from elements import InputElement, CurrencyElement
from locators import ConverterPageLocators


class BasePage(object):
    """Base page class to be subclassed by all other page classes"""

    def __init__(self, driver):
        self.driver = driver


class ConverterPage(BasePage):
    """Page class for currency converter page, extends BasePage class"""

    # adding InputElement object to the ConverterPage
    input_element = InputElement(ConverterPageLocators.INPUT_FIELD)

    # adding two currency_lists to the ConverterPage:
    # one for initial currency and one for desirable currency
    initial_currency_element = CurrencyElement(ConverterPageLocators.FROM_CURRENCY_FIELD,
                                               ConverterPageLocators.FROM_CURRENCY_LIST_ELEMENT,
                                               ConverterPageLocators.CONVERTER_FROM_SELECT)
    desirable_currency_element = CurrencyElement(ConverterPageLocators.TO_CURRENCY_FIELD,
                                               ConverterPageLocators.TO_CURRENCY_LIST_ELEMENT,
                                               ConverterPageLocators.CONVERTER_TO_SELECT)

    def is_title_matches(self):
        """Verifies that we are on the converter's page"""
        return "Калькулятор иностранных валют" in self.driver.title

    def click_submit_button(self):
        """Triggers the exchange"""
        element = self.driver.find_element(*ConverterPageLocators.SUBMIT_BUTTON)
        element.click()
        WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element
                                            (*ConverterPageLocators.RESULT_VALUE).text != '')

    def choose_cash_to_cash_exchange(self):
        """Choosing cash-to-cash exchange type
        by clicking corresponding checkboxes
        """
        self.driver.find_element(*ConverterPageLocators.FROM_TYPE_CASH).click()
        self.driver.find_element(*ConverterPageLocators.TO_TYPE_CASH).click()

    def get_current_exchange_rates(self):
        """Grabbing current buy and sell exchange rates
        and return them as tuple
        """
        buy_exchange_rate = self.driver.find_element(*ConverterPageLocators.
                                                     BUY_EXCHANGE_RATE).text.replace(',', '.')
        sell_exchange_rate = self.driver.find_element(*ConverterPageLocators.
                                                      SELL_EXCHANGE_RATE).text.replace(',', '.')
        return (buy_exchange_rate, sell_exchange_rate)

    def get_final_currency(self):
        """Return final currency that we get after exchange"""
        return self.driver.find_element(*ConverterPageLocators.RESULT_CURRENCY).text

    def get_final_result(self):
        """Return formatted money amount after suggested exchange"""
        return self.driver.find_element(*ConverterPageLocators.RESULT_VALUE).\
            text.replace(' ', '').replace(',', '.')
