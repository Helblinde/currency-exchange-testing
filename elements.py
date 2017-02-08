from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from locators import ConverterPageLocators


class ConverterPageElement(object):
    """Base element class with __init__, __set__
    and __get__ methods for typical page elements
    """

    def __init__(self, locator):
        self.locator = locator

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(*self.locator))
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(*self.locator))
        element = driver.find_element(*self.locator)
        return element.get_attribute("value")


class InputElement(ConverterPageElement):
    """Class for the specific input field element"""

    def __set__(self, obj, value):
        """Overrides base class __set__ method because we need to
        clear this input field manually before entering the value
        since it is not automatically cleared after being clicked on
        """
        driver = obj.driver
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(*self.locator))
        # find input field, click and clear
        element = driver.find_element(*self.locator)
        element.click()
        element.clear()
        # if input field is still not cleared somehow, click and clear again
        if not WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element(*self.locator).get_attribute('value') == ''):
            element.click()
            element.clear()
        # input passed values
        element.send_keys(value)


class CurrencyElement(ConverterPageElement):
    """Class that is used for currency lists on the page"""

    def __init__(self, element_locator, list_locator, select_locator):
        """Constructor for initializing currency list element;
        first locator is the locator of displayed field;
        second locator is specific locator of an element in the list
        that depends on the currency we want to choose and will
        be formatted in the __set__ method based on the passed value;
        third locator is locator of <select> element for
        choosing the value.
        """
        super(CurrencyElement, self).__init__(element_locator)
        self.list_locator = list_locator
        self.select_locator = select_locator

    def __set__(self, obj, value):
        """Chooses proper currency value in the currency list"""
        driver = obj.driver
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(*self.locator))
        # click on the visible element to expand the list
        driver.find_element(*self.locator).click()
        # format list_locator value to find proper element of the list
        # that corresponds to the specific currency we need
        proper_currency_list_element = list(self.list_locator)
        proper_currency_list_element[1] = proper_currency_list_element[1] \
                                        % ConverterPageLocators.CURRENCIES[value]
        # select specific currency
        driver.find_element(*proper_currency_list_element).click()
        Select(driver.find_element(*self.select_locator)).select_by_visible_text(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified currency_list;
        overrides __get__ method of base class since we want
        to get '.text' field instead of '.get_attribute("value")'
        """
        driver = obj.driver
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(*self.locator))
        element = driver.find_element(*self.locator)
        return element.text
