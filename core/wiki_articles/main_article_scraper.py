import pandas as pd
from utils.wikipedia_scraper import WikipediaScraper

OUTPUT_FOLDER = "./data/locations/articles/main/"

class MainArticleScraper:
    scraper = WikipediaScraper(verbose=True, indent="\t")

    def scrape_context(context, scraper = None):
        if scraper is None: 
            scraper = MainArticleScraper.scraper 

        table_file = f"./data/locations/tables/{context}.csv"
        regions = pd.read_csv(table_file) 
        links = regions["link"]
        
        i = 0 
        n = len(links)
        for link in links: 
            print(f"--- Processing {link} ({i + 1} / {n}) ---")
            article_name = link.split("/")[2] 
            scraper.download(
                article_name, 
                output_folder=OUTPUT_FOLDER, 
                output_filename=article_name
            )
            i += 1
