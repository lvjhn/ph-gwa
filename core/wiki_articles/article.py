from bs4 import BeautifulSoup

class Article: 
    def __init__(
        self,
        source = "Regions",
        folder = "./data/locations/articles/"
    ):  
        self.source  = source 
        self.folder  = folder 
        self.content = None 
        self.get_content()

    def get_path(self): 
        return self.folder + self.source + ".html"

    def get_content(self, reload_ = False):
        if self.content is not None and not reload_:
            return self.content 
        else: 
            path = self.get_path()
            self.content = open(path, "r").read()
            return self.content

    def load(self): 
        return BeautifulSoup(self.content, "html.parser")
    

