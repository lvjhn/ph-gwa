import pandas as pd 
import re

from .article import Article

REGIONS_TABLE     = "./data/locations/tables/regions.csv"
PROVINCES_TABLE   = "./data/locations/tables/provinces.csv"
MUNICITIES_TABLE  = "./data/locations/tables/municities.csv"

class DatasetExtractor: 
    def extract_for_regions():
        dataset = {
            "text"      : [], 
            "label"     : [],
            "context"   : [], 
            "source"    : []
        }

        reg_table  = pd.read_csv(REGIONS_TABLE)
        prov_table = pd.read_csv(PROVINCES_TABLE)
        muct_table = pd.read_csv(MUNICITIES_TABLE) 

        # get paragraphs from region articles
        print("=== PHASE A : GET PARAGRAPHS FROM REGION ARTICLES ===")
        i = 0 
        n = len(reg_table)
        for index, row in reg_table.iterrows():
            article_name = row["link"].split("/")[2]
            print(f"@ Processing {article_name} ({i + 1} / {n})")
            article = Article(f"main/{article_name}")
            name = row["name"]
            paragraphs = DatasetExtractor.extract_paragraphs(article)
            dataset["text"]     += paragraphs 
            dataset["label"]    += [row["name"]] * len(paragraphs) 
            dataset["context"]  += ["PLA"] * len(paragraphs)
            dataset["source"]   += [article_name] * len(paragraphs)

            print(f"\t> Fetched {len(paragraphs)} paragraphs.")
            i += 1

        # get paragraphs from province articles
        print("=== PHASE B : GET PARAGRAPHS FROM PROVINCE ARTICLES ===")
        i = 0 
        n = len(prov_table)
        for index, row in prov_table.iterrows():
            article_name = row["link"].split("/")[2]
            print(f"@ Processing {article_name} ({i + 1} / {n})")
            article = Article(f"main/{article_name}")
            name = row["name"]
            paragraphs = DatasetExtractor.extract_paragraphs(article)
            dataset["text"]     += paragraphs 

            dataset["label"]    += [row["region"]] * len(paragraphs) 
            dataset["context"]  += ["PLA"] * len(paragraphs)
            dataset["source"]   += [article_name] * len(paragraphs)

            print(f"\t> Fetched {len(paragraphs)} paragraphs.")
            i += 1

        # get paragraphs from municity articles
        print("=== PHASE B : GET PARAGRAPHS FROM MUNICITY ARTICLES ===")
        i = 0 
        n = len(muct_table)
        for index, row in muct_table.iterrows():
            article_name = row["link"].split("/")[2]
            print(f"@ Processing {article_name} ({i + 1} / {n})")
            article = Article(f"main/{article_name}")
            name = row["name"]
            province = row["province"]
            paragraphs = DatasetExtractor.extract_paragraphs(article)
            dataset["text"]     += paragraphs 
            dataset["label"]    += [row["region"]] * len(paragraphs) 
            dataset["context"]  += ["MLA"] * len(paragraphs)
            dataset["source"]   += [article_name] * len(paragraphs)
            print(f"\t> Fetched {len(paragraphs)} paragraphs.")
            i += 1

        # create dataframe 
        df = pd.DataFrame(dataset) 

        # drop rows with null values
        df = df.dropna()

        return df

    def extract_for_provinces():
        dataset = {
            "text"      : [], 
            "label"     : [],
            "context"   : [], 
            "source"    : []
        }

        prov_table = pd.read_csv(PROVINCES_TABLE)
        muct_table = pd.read_csv(MUNICITIES_TABLE) 

        # get paragraphs from province articles
        print("=== PHASE A : GET PARAGRAPHS FROM PROVINCE ARTICLES ===")
        i = 0 
        n = len(prov_table)
        for index, row in prov_table.iterrows():
            article_name = row["link"].split("/")[2]
            print(f"@ Processing {article_name} ({i + 1} / {n})")
            article = Article(f"main/{article_name}")
            name = row["name"]
            paragraphs = DatasetExtractor.extract_paragraphs(article)
            dataset["text"]     += paragraphs 
            dataset["label"]    += [name] * len(paragraphs) 
            dataset["context"]  += ["PLA"] * len(paragraphs)
            dataset["source"]   += [article_name] * len(paragraphs)

            print(f"\t> Fetched {len(paragraphs)} paragraphs.")
            i += 1

        # get paragraphs from municity articles
        print("=== PHASE B : GET PARAGRAPHS FROM MUNICITY ARTICLES ===")
        i = 0 
        n = len(muct_table)
        for index, row in muct_table.iterrows():
            article_name = row["link"].split("/")[2]
            print(f"@ Processing {article_name} ({i + 1} / {n})")
            article = Article(f"main/{article_name}")
            name = row["name"]
            province = row["province"]
            paragraphs = DatasetExtractor.extract_paragraphs(article)
            dataset["text"]     += paragraphs 
            dataset["label"]    += [province] * len(paragraphs) 
            dataset["context"]  += ["MLA"] * len(paragraphs)
            dataset["source"]   += [article_name] * len(paragraphs)
            print(f"\t> Fetched {len(paragraphs)} paragraphs.")
            i += 1

        # create dataframe 
        df = pd.DataFrame(dataset) 

        # drop rows with null values
        df = df.dropna()

        return df

    def extract_for_municities():
        dataset = {
            "text"      : [], 
            "label"     : [],
            "context"   : [], 
            "source"    : []
        }

        muct_table = pd.read_csv(MUNICITIES_TABLE) 

        # get paragraphs from municity articles
        print("=== PHASE A : GET PARAGRAPHS FROM MUNICITY ARTICLES ===")
        i = 0 
        n = len(muct_table)
        for index, row in muct_table.iterrows():
            article_name = row["link"].split("/")[2]
            print(f"@ Processing {article_name} ({i + 1} / {n})")
            article = Article(f"main/{article_name}")
            name = row["name"]
            province = row["province"]
            paragraphs = DatasetExtractor.extract_paragraphs(article)
            dataset["text"]     += paragraphs 
            dataset["label"]    += [row["province"] + " | " + row["name"]] * len(paragraphs) 
            dataset["context"]  += ["MLA"] * len(paragraphs)
            dataset["source"]   += [article_name] * len(paragraphs)
            print(f"\t> Fetched {len(paragraphs)} paragraphs.")
            i += 1

        # create dataframe 
        df = pd.DataFrame(dataset) 

        # drop rows with null values
        df = df.dropna()

        return df

    def extract_paragraphs(article):
        html = article.load() 
        paragraphs = \
            html.select(
                ".mw-content-ltr.mw-parser-output > "
                "p, div, table, ul, ol"
            )

        paragraphs_ = []
        start = False

        for paragraph in paragraphs: 
            if paragraph.has_attr("class") and "infobox in class":
                p = paragraph.get_text()
                p = DatasetExtractor.clean(p)
                paragraphs_.append(p) 

        return paragraphs_

    def clean(paragraph): 
        paragraph = re.sub("\[.*\]", "", paragraph) 
        paragraph = re.sub("\t", "", paragraph) 
        paragraph = paragraph.strip()
        return paragraph


