from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from pandas import DataFrame
import logging
import re

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s", 
    datefmt="%Y-%m-%d %I:%M:%S %p", 
    level=logging.DEBUG
)

class NBA:

    """
    The NBA Stats Class
    
    :param nba_website: str 
        The stats website 
    """

    @staticmethod
    def __parse_table_data(table_str: str) -> DataFrame:
        """
        Parse table html string
        
        :params table_str: str 
            Table HTML String
        
        :raises BaseException 

        :returns table_data: DataFrame 
            Table data
        """
        soup = BeautifulSoup(table_str, features="html.parser")
        table_data = []
        table_head = soup.find('thead').find('tr')
        table_body = soup.find('tbody')

        if any([table_body is None, table_head is None]):
            raise Exception("Invalid table signature")
    
        rows: list = table_body.find_all('tr')
        columns: list = table_head.find_all('th')

        if any([len(rows) == 0 or len(columns) == 0]):
            raise Exception("0 rows or columns were found")
        
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

        return stats_df

    @staticmethod
    def get_stats(url: str) -> DataFrame:
        """
        Get NBA Statistics 
        
        :returns DataFrame 
            A dataframe containing NBA Stats
        """
        try:

            with Firefox() as driver:

                # Navigate to NBA Site
                logging.debug(f"Navigating to {url}")
                driver.get(url)
                driver.execute_script("window.scrollTo(0, 300)")
                
                # Select button xpath
                select_btn_xpath = "//div[@class='Crom_cromSettings__ak6Hd']/div[1]//select"

                # Wait for a max of 10 seconds for the element to appear
                wait = WebDriverWait(driver, 10)
                wait.until(presence_of_element_located((By.XPATH, select_btn_xpath)))

                # Select button
                select = Select(driver.find_element(By.XPATH, select_btn_xpath))
                select.select_by_index(0) # select all
                
                # Get table data
                logging.debug("Finding table element")
                table_data_html = driver.find_element(By.CLASS_NAME, "Crom_table__p1iZz")

                # Create dataframe from html string
                logging.debug("Parsing table data")
                stats_df = NBA.__parse_table_data(table_data_html.get_attribute('innerHTML'))
                
        except TimeoutException as err:
            logging.error(f"A timeout exception occurred: {err}")
            return DataFrame()

        except BaseException as err:
            logging.error("An error occurred while fetching stats")
            return DataFrame()

        else:
            logging.info("Successfully parsed table data")
            return stats_df



    

    

    
