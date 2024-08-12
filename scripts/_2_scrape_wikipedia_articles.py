from core.wiki_articles.main_article_scraper import MainArticleScraper

print("# === SCRAPING REGIONS === #")
MainArticleScraper.scrape_context("regions") 
print()

print("# === SCRAPING PROVINCES === #")
MainArticleScraper.scrape_context("provinces") 
print()

print("# === SCRAPING MUNICITIES === #")
MainArticleScraper.scrape_context("municities") 
print()