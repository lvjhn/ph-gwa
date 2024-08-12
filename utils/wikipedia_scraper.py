from core.helpers.verbose_logging import VerboseLogging 

import requests

class WikipediaScraper(VerboseLogging): 
    
    def __init__(
        self,
        base_url = "https://en.wikipedia.org",
        prefix   = "/wiki",
        *args,
        **kwargs
    ): 
        VerboseLogging.__init__(self, *args, **kwargs) 

        self.base_url        = base_url 
        self.prefix          = prefix  

    def get_download_url(self, key): 
        return self.base_url + self.prefix + "/" + key

    def save_to_file(self, data, file): 
        open(file, "w").write(data)

    def download(
        self, 
        key, 
        output_folder = "./data/temp/",
        output_filename = None
    ):
        # fetch wikipedia article
        url = self.get_download_url(key)
        req  = requests.get(url) 
        data = req.text 

        if self.verbose:
            print(f"{self.indent}--- Downloading `{key}` ({url}) ---")

        # save to file
        if output_filename is None:
            output_filename = key

        full_output_path = \
            output_folder + "/" + output_filename + ".html"

        self.save_to_file(data, full_output_path)

        