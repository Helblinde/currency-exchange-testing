import pytest
from selenium import webdriver


@pytest.fixture()
def driver(request):
    """Pytest fixture that creates and returns
    Firefox selenium driver and also sets implicit
    wait value and opens converters page.
    Also uses finalizer that will call driver.quit() method
    """
    print("Creating Firefox driver")
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get("http://www.sberbank.ru/ru/quotes/converter")
    def driver_teardown():
        driver.quit()
    request.addfinalizer(driver_teardown)
    return driver
