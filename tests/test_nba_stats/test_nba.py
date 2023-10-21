from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from pandas import DataFrame
from os import getenv
import pytest
import re


class TestNBA:

    """
    Tests on the NBA Website
    """
    nba_website = getenv("NBA_WEBSITE")

    @pytest.mark.skip("Reduce requests to nba site and use sample html file")
    def test_get_nba_table_stats(self):
        """
        Get the HTML of the NBA Website
        """
        with Firefox() as driver:
            driver.get(self.nba_website)
            result = driver.find_element(By.CLASS_NAME, "Crom_table__p1iZz")

            # print(result.get_attribute('innerHTML'))
            assert result is not None

    # @pytest.mark.skip("Table parsing complete")
    def test_parse_nba_stats_table(self):
        """
        Parse the NBA Stats table 
        """
        with open("./tests/test_nba_stats/sample_html_files/"
                  "sample_nba_stats_table.html", "r") as file:
            sample_nba_stats_table = file.read()

        soup = BeautifulSoup(sample_nba_stats_table, features="html.parser")
        table_data = []
        table_head = soup.find('thead').find('tr')
        table_body = soup.find('tbody')

        rows: list = table_body.find_all('tr')
        columns: list = table_head.find_all('th')
        table_columns = [re.sub(r'\s+', " ", column.text.strip().replace('\n', ' ').replace('\xa0', ' ')) 
                         for column in columns if column.attrs.get('hidden') is None]

        # Append table columns
        table_columns[0] = 'Rank'
        table_data.append(table_columns)

        # Append table data
        for row in rows:
            row_data = row.find_all('td')
            row_data_entries = [element.text.strip() for element in row_data]
            table_data.append(row_data_entries)

        # Create pandas dataframe 
        stats_df = DataFrame(table_data[1:], columns=table_data[0])

        assert soup is not None

        # Make sure table columns match table rows
        assert len(table_data[0]) == len(table_data[1])

        # Check the number of rows 
        print(f"Number of records: {len(table_data[1:])}")
        print(stats_df.head())
        assert len(table_data[1:]) >= 570


    @pytest.mark.skip("Selection complete")
    def test_all_records(self):
        """
        Get all records
        """

        with Firefox() as driver:

            # Navigate to NBA Site
            driver.get(self.nba_website)
            driver.execute_script("window.scrollTo(0, 300)")

            select_btn_xpath = "//div[@class='Crom_cromSettings__ak6Hd']/div[1]//select"
            wait = WebDriverWait(driver, 10)
            wait.until(presence_of_element_located((By.XPATH, select_btn_xpath)))
            select = Select(driver.find_element(By.XPATH, select_btn_xpath))
            select.select_by_index(0)
            
            table_data_html = driver.find_element(By.CLASS_NAME, "Crom_table__p1iZz")

            print(table_data_html.get_attribute('innerHTML'))
            assert table_data_html is not None
