from models.scraper import DataScraper

scraper = DataScraper()

scraper.get_electricity_links()
scraper.get_electricity_csv()
scraper.get_df()
scraper.save_df("data/all_levels.csv")