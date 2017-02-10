import pytest
from importing_csv import importing_csv
from driver_fixture import driver
from pages import ConverterPage
from precise_result import precise_result


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
    All print statements are seen if running with '-s' flag
    """

    # create converter page object
    converter_page = ConverterPage(driver)

    # check the title
    assert converter_page.is_title_matches(), "Title is wrong!"

    # print currently set value
    print("Default value:", converter_page.input_element)

    # set our value and print it
    converter_page.input_element = value
    print("Our value:", converter_page.input_element)

    # choosing cash-to-cash exchange type
    converter_page.choose_cash_to_cash_exchange()

    # set initial and desirable currencies
    converter_page.initial_currency_element = from_currency
    converter_page.desirable_currency_element = to_currency

    # grabbing current buy and sell exchange rates
    buy_exchange_rate, sell_exchange_rate = converter_page.get_current_exchange_rates()
    print("Current exchange rates:", buy_exchange_rate, sell_exchange_rate)

    # click on submit button and wait until result is seen
    converter_page.click_submit_button()

    # choosing type of exchange calculation (from RUR or to RUR)
    # and calculate expected money amount
    if to_currency == 'RUR':
        expected_result = precise_result(str(float(value.replace(',', '.'))
                                             * float(buy_exchange_rate)))
    if from_currency == 'RUR':
        expected_result = precise_result(str(float(value.replace(',', '.'))
                                             / float(sell_exchange_rate)))

    # check that result currency equals desirable currency
    final_currency = converter_page.get_final_currency()
    print("Result currency:", final_currency)
    assert to_currency == final_currency, "Wrong currency received!"

    # check that received result equals expected_result due to calculations
    final_result = converter_page.get_final_result()
    print("Expected result:", expected_result)
    print("Actual result:", final_result)
    assert expected_result == final_result, "Wrong money amount received!"
