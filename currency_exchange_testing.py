import pytest
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# location of csv file for data-driven testing
FILE_WITH_PARAMS = 'params.csv'

# constants section with XPATH values for main page objects
INPUT_FIELD_XPATH = "//input[@placeholder='Сумма']"
FROM_TYPE_CASH_XPATH = "//p[text()='Наличные']"
TO_TYPE_CASH_XPATH = "//p[text()='Выдать наличные']"
SUBMIT_BUTTON_XPATH = "//aside[@class='rates-aside']//" \
                      "button[text()='Показать']"
RESULT_VALUE_XPATH = "//div[@class='converter-result']/h4/span[1]"
RESULT_CURRENCY_XPATH = "//div[@class='converter-result']/h4/span[2]"
BUY_EXCHANGE_RATE_XPATH = "//div[@class='current-table']/table/tbody/" \
                          "tr/td[3]/span"
SELL_EXCHANGE_RATE_XPATH = "//div[@class='current-table']/table/tbody/" \
                           "tr/td[4]/span"
FROM_CURRENCY_FIELD_XPATH = "//aside[@class='rates-aside']/div[1]/div[1]/" \
                            "div[3]/div[2]"
TO_CURRENCY_FIELD_XPATH = "//aside[@class='rates-aside']/div[1]/div[1]/" \
                          "div[4]/div[2]"
FROM_CURRENCY_LIST_ELEMENT_XPATH = "//aside[@class='rates-aside']/div/div/" \
                                   "div[3]/div[2]/div/div/span[%d]"
TO_CURRENCY_LIST_ELEMENT_XPATH = "//aside[@class='rates-aside']/div/div/" \
                                 "div[4]/div[2]/div/div/span[%d]"

# dictionary of all available currencies and their corresponding
# index number in the list of currencies on the converter's page
CURRENCIES = {'RUR': 1, 'CHF': 2, 'EUR': 3, 'GBP': 4, 'JPY': 5, 'USD': 6}


def importing_csv():
    """Auxiliary function:
    Opens 'params.csv' file in this module's dir,
    reads all lines and composes parameters tuple
    in specific pytest format including headers
    and values. Returns this tuple for further
    test function parameterizing
    """
    parameters_list = []
    parameters_header = ("from_currency", "to_currency", "value")
    with open(FILE_WITH_PARAMS, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            parameters_list.append(tuple(row))
    parameters = (parameters_header, parameters_list)
    return parameters


@pytest.fixture()
def driver(request):
    """Pytest fixture that creates and returns
    Firefox selenium driver and also sets implicit
    wait value. Also uses finalizer that will
    call driver.quit() method
    """
    print("Creating Firefox driver")
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    def driver_teardown():
        driver.quit()
    request.addfinalizer(driver_teardown)
    return driver


@pytest.mark.parametrize(*importing_csv())
def test_currency_exchange(from_currency, to_currency, value, driver):
    """Main test method, that is parametrized with
    different sets of values from csv file;
    Input values: 'from_currency' that is our cash currency,
    'to_currency' that is the currency we want to have,
    'value' that is our cash amount.
    Expected result: all elements are found on the page,
    cash value after suggested exchange matches the calculations
    made using exchange rates on the page.
    """

    # open converter's page and check the title
    driver.get("http://www.sberbank.ru/ru/quotes/converter")
    assert "Калькулятор иностранных валют" in driver.title

    # find input field for money amount, click on it and clear
    money_input_field = driver.find_element_by_xpath(INPUT_FIELD_XPATH)
    print("Default input field value:", money_input_field.get_attribute('value'))
    money_input_field.click()
    money_input_field.clear()

    # if input field is still not cleared somehow, click and clear again
    if not WebDriverWait(driver, 10).until(
            lambda s: s.find_element_by_xpath(INPUT_FIELD_XPATH).get_attribute('value') == ''):
        money_input_field.click()
        money_input_field.clear()

    # type our cash amount
    money_input_field.send_keys(value)
    print("Our input field value:", money_input_field.get_attribute('value'))

    # choosing cash-to-cash exchange type
    driver.find_element_by_xpath(FROM_TYPE_CASH_XPATH).click()
    driver.find_element_by_xpath(TO_TYPE_CASH_XPATH).click()

    # choosing initial currency
    driver.find_element_by_xpath(FROM_CURRENCY_FIELD_XPATH).click()
    driver.find_element_by_xpath(FROM_CURRENCY_LIST_ELEMENT_XPATH %
                                 CURRENCIES[from_currency]).click()
    Select(driver.find_element_by_name("converterFrom")).\
        select_by_visible_text(from_currency)

    # choosing desirable currency
    driver.find_element_by_xpath(TO_CURRENCY_FIELD_XPATH).click()
    driver.find_element_by_xpath(TO_CURRENCY_LIST_ELEMENT_XPATH %
                                 CURRENCIES[to_currency]).click()
    Select(driver.find_element_by_name("converterTo")).\
        select_by_visible_text(to_currency)

    # grabbing current buy and sell exchange rates
    buy_exchange_rate = driver.find_element_by_xpath(BUY_EXCHANGE_RATE_XPATH).\
        text.replace(',', '.')
    sell_exchange_rate = driver.find_element_by_xpath(SELL_EXCHANGE_RATE_XPATH).\
        text.replace(',', '.')
    print("Current exchange rates:", buy_exchange_rate, sell_exchange_rate)

    # click on submit button and wait until result is seen
    driver.find_element_by_xpath(SUBMIT_BUTTON_XPATH).click()
    WebDriverWait(driver, 10).until(lambda s: s.find_element_by_xpath
                                             (RESULT_VALUE_XPATH).text != '')

    # choosing type of exchange calculation (from RUR or to RUR)
    if to_currency == 'RUR':
        expected_result = round(float(value.replace(',', '.')) * float(buy_exchange_rate), 2)
    if from_currency == 'RUR':
        expected_result = round(float(value.replace(',', '.')) / float(sell_exchange_rate), 2)

    # check that result currency equals desirable currency
    result_currency = driver.find_element_by_xpath(RESULT_CURRENCY_XPATH).text
    print("Result currency:", result_currency)
    assert to_currency == result_currency

    # check that result value equals expected_result due to calculations
    actual_result = round((float(driver.find_element_by_xpath(RESULT_VALUE_XPATH).
                                 text.replace(' ', '').replace(',', '.'))), 2)
    print("Expected result:", expected_result)
    print("Actual result:", actual_result)
    assert expected_result == actual_result
