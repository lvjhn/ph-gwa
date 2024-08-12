from utils.wikipedia_scraper import WikipediaScraper 
from core.wiki_articles.article import Article
from core.wiki_articles.locations_extractor import LocationsExtractor

# --- parameters --- #  
BASIS_ARTICLES = [ "Regions", "Provinces", "Municities" ]

regions = None
provinces = None 
municities = None

prov_to_reg = None

# --- load basis article ---  # 
def extract_regions():
    global regions_ba
    regions_ba = Article("basis/Regions")
    regions = LocationsExtractor.extract_regions(regions_ba)
    regions.rename(columns={ "Unnamed: 0" : "index" })

def extract_provinces():
    global prov_to_reg, provinces_ba
    provinces_ba = Article("basis/Provinces") 
    provinces = LocationsExtractor.extract_provinces(provinces_ba) 
    provinces.rename(columns={ "Unnamed: 0" : "index" })

    # map provinces to regions 
    prov_to_reg = provinces[["name", "region"]]
    prov_to_reg = prov_to_reg.set_index("name")  

def extract_municities(): 
    global municities_ba
    municities_ba = Article("basis/Municities")
    municities = LocationsExtractor.extract_municities(municities_ba) 
    municities["region"] = \
        municities["province"].apply(lambda x: prov_to_reg.loc[x, "region"])
    municities.to_csv("./data/locations/tables/municities.csv")

extract_regions()
extract_provinces()
extract_municities()