from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import pytest

class TestGeckoDriver:

    """
    Test the firefox driver
    """
    # @pytest.mark.skip(reason="Driver works for now")
    def test_firefox_driver(self):
        with Firefox() as driver:
            driver.get("http://google.com/ncr")
            wait = WebDriverWait(driver, 10)
            driver.find_element(By.NAME, "q").send_keys("cheese" + Keys.RETURN)
            wait.until(presence_of_element_located((By.XPATH, '//*[@id="rcnt"]')))
            results = driver.find_elements(By.XPATH, "//a[@href]")

        assert results is not None