import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

class DataScraper():
    
    BASE_URL = "https://www.data.gov.uk/dataset/e7d4c1cf-45a0-4070-878f-24ad9641f655/domestic-electricity-and-gas-estimates-by-postcode-in-great-britain"
    
    def __init__(self):
        self.electricity_elements = []
        self.csv_elements = []
        self.df = None
        
    def get_electricity_links(self):
        """
            Allows to get all the elements of the table that contains electricity, with their corresponding
            links
        """
        res = requests.get(self.BASE_URL)
        soup = BeautifulSoup(res.content, features="html.parser")
        cell_elements = soup.find_all("td", {"class": "govuk-table__cell"})
        electricity_elements = []
        for cell in cell_elements:
            [s.extract() for s in cell('span')] # Extract the span elements to remove extra text
            text_content = ' '.join(cell.strings).replace("\n", "").strip()
            if "electricity" in text_content:
                link = cell.find("a")["href"]
                electricity_elements.append({"text": text_content, "link": link})
        
        self.electricity_elements = electricity_elements
        return 
    
    def get_electricity_csv(self):
        """
            Allows to get, from the links obtained with get_electricity_links(), the .csv files with
            the data
        """
        
        csv_elements = []
        for el in self.electricity_elements:
            text = el["text"]
            link = el["link"]
            year = text.split(" ")[0].strip() # The years is shown always before the word electricity

            # I'll skip the year 2013, because there is no information for 2014
            if year == "2013":
                continue

            # If the link is already to the csv file
            if "uploads" in link:
                csv_elements.append({
                    "text": text,
                    "link": link,
                    "year": year
                })
                continue


            else: # bring the page of statistics and get the .csv link
                res = requests.get(link)
                soup = BeautifulSoup(res.content, features="html.parser")

                sections = soup.find("section", {"id": "documents"}).find_all("section")
                # Select the section that contains the words "level all"
                all_level_section = [sections[idx] for idx, section in enumerate(sections) if
                                    "level all" in ' '.join(section.strings)][0]

                # The csv link is in the last element of the a tags
                csv_elements.append({
                    "text": text,
                    "link": all_level_section.find_all("a")[-1]["href"],
                    "year": year
                })
                
        self.csv_elements = csv_elements
        
        return 
    
    def get_df(self):
        """
            Returns a Pandas DataFrame that contains all the elements of the CSV, with their corresponding
            year
        """
        
        output_list = []
        for el in self.csv_elements:
            year = el["year"]
            link = el["link"]
            print(f"Reading the year {year}, link: {link}")
            df_tmp = pd.read_csv(link)
            df_tmp["Year"] = year
            output_list.append(df_tmp)
        print("DONE!")    
        
        df_electricity = pd.concat(output_list, ignore_index = True)
        
        self.df = df_electricity
        
        return 

    def save_df(self, path):
      print(f"Saving .CSV file in {path}")
      self.df.to_csv(path, index=False)