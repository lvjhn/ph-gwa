from core.wiki_articles.dataset_extractor import DatasetExtractor

# --- Extracting Regional-Level Dataset --- #
print("===== Extracting Regional-level Dataset =====")
dataset_df = DatasetExtractor.extract_for_regions()
dataset_df.to_csv("./data/datasets/wla/regional.csv")
print()

# --- Extracting Provincial-Level Dataset --- #
print("===== Extracting Provincial-level Dataset =====")
dataset_df = DatasetExtractor.extract_for_provinces()
dataset_df.to_csv("./data/datasets/wla/provincial.csv")
print()

# --- Extracting Municity-Level Dataset --- #
print("===== Extracting Municity-level Dataset =====")
dataset_df = DatasetExtractor.extract_for_municities()
dataset_df.to_csv("./data/datasets/wla/municity.csv")
print()