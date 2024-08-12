import pandas as pd
import re 

class LocationsExtractor:
    def extract_regions(article): 
        html       = article.load()
        rows       = html.select("tbody > tr")
        rows       = rows[:-1]
        
        names      = [] 
        ids        = []
        links      = [] 
        
        for row in rows: 
            columns = row.select("td")
            element = columns[0]
            
            # get name
            name    = element.select("a")[0].get_text()
            name    = name.replace("\t", "")
            name    = name.replace("\n", " ")

            # get link
            link    = element.select("a")[0]["href"] 

            # get id
            id_     = element.select("span")[0].get_text()
            id_     = id_[1:-1]

            # add data
            names.append(name)
            ids.append(id_)
            links.append(link)

        return pd.DataFrame({
            "id"    : ids,
            "name"  : names, 
            "link"  : links
        })

    def extract_provinces(article): 
        html       = article.load()
        rows       = html.select("tbody > tr")
        rows       = rows[:-2]

        isos       = []
        names      = []
        links      = []
        regions    = []
        
        for row in rows: 
            td_cols = row.select("td")
            th_cols = row.select("th")

            name_el     = td_cols[0]
            iso_el      = th_cols[0]
            region_el   = td_cols[8]
            
            # get name
            name    = name_el.select("a")[0].get_text()
            name    = name.replace("\t", "")
            name    = name.replace("\n", " ")
            name    = re.sub("\[.*\]", "", name)

            # get link
            link    = name_el.select("a")[0]["href"] 
            
            # get iso
            iso     = iso_el.get_text()
            iso     = iso.replace("\n", "")
            iso     = iso.replace("\t", "")

            # get region
            region  = region_el.get_text() 
            region  = re.sub("\[.*\]", "", region)
            region  = region.replace("\n", "")

            # add data
            names.append(name)
            links.append(link)
            isos.append(iso)
            regions.append(region)

        return pd.DataFrame({
            "name" : names, 
            "link" : links, 
            "iso"  : isos,
            "region" : regions
        })

    def extract_municities(article): 
        html       = article.load()
        rows       = html.select("tbody > tr")
        rows       = rows[:-1]

        names       = []
        links       = []
        provinces   = [] 
        classes     = []
        
        for row in rows: 
            td_cols = row.select("td")
            th_cols = row.select("th")
            
            name_el     = th_cols[0]
            class_el    = td_cols[4]
            province_el = td_cols[5]
            
            # get name
            name    = name_el.select("a")[0].get_text()
            name    = name.replace("*", "") 
            name    = name.replace("\t", "") 
            name    = name.replace("\n", " ")

            # get link 
            link    = name_el.select("a")[0]["href"] 


            # get class  
            class_  = class_el.get_text() 
            class_  = class_.replace("\n", "") 
            class_  = class_.replace("\t", "")

            # get province
            province = province_el.get_text() 
            province = province.replace("\n", " ")
            province = province.replace("\t", "")
            province = province.strip()

            # add data
            names.append(name)
            links.append(link)
            classes.append(class_)
            provinces.append(province)
 

        return pd.DataFrame({
            "name" : names, 
            "link" : links, 
            "class" : classes,
            "province" : provinces
        })