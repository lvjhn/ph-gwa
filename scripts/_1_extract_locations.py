from utils.wikipedia_scraper import WikipediaScraper 
from core.wiki_articles.article import Article
from core.wiki_articles.locations_extractor import LocationsExtractor

# --- parameters --- #  
BASIS_ARTICLES = [ "Regions", "Provinces", "Municities" ]

# --- load basis article ---  # 
def extract_regions():
    regions_ba = Article("basis/Regions")
    regions = LocationsExtractor.extract_regions(regions_ba)
    print(regions)

def extract_provinces():
    provinces_ba = Article("basis/Provinces") 
    provinces = LocationsExtractor.extract_provinces(provinces_ba) 
    print(provinces) 

def extract_municities(): 
    municities_ba = Article("basis/Municities")
    municities = LocationsExtractor.extract_municities(municities_ba) 
    print(municities)

# extract_regions()
# extract_provinces()
extract_municities()
