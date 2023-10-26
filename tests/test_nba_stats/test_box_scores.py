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

class TestBoxScores:

    """
    Tests on box scores
    """

    box_scores_webbie = "https://www.nba.com/game/lal-vs-den-0022300061/box-score"

    @pytest.mark.skip("Test passed")
    def test_get_box_scores_table(self):
        """
        Try finding the box scores table 
        """
        with Firefox() as driver:
            driver.get(self.box_scores_webbie)
            result = driver.find_elements(By.CLASS_NAME, "GameBoxscore_gbTableSection__zTOUg")

            print(result[0].get_attribute('innerHTML'))
            assert len(result) == 2



    def test_format_box_scores_table(self):

        with open("./tests/test_nba_stats/sample_html_files/box_scores.html", "r") as file:
            box_scores = file.read()


        soup = BeautifulSoup(box_scores, features="html.parser")
        team_header = soup.find('h2').text.strip()
        table_data = []
        table_head = soup.find('thead').find('tr')
        table_body = soup.find('tbody')

        rows: list = table_body.find_all('tr')
        columns: list = table_head.find_all('th')
        table_columns = [column.text for column in columns] + ['TEAMHEADER']

        # Append table columns
        table_data.append(table_columns)

        # Append table rows
        for row in rows:
            row_data = row.find_all('td')
            row_data_entries = [re.sub(r'\s+', " ", element.text.strip().replace('\n', '')) 
                                for element in row_data] + [team_header]
            

            table_data.append(row_data_entries)

        
        # Create pandas dataframe 
        stats_df = DataFrame(table_data[1:], columns=table_data[0])

        # Check the number of rows 
        print(f"Number of records: {stats_df.shape[0]}")
        print(stats_df)

        print(table_data)
        assert stats_df.shape[0] == 12
        assert 1==0