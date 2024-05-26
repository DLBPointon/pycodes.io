import io
import requests

class PostcodeObj:
    def __init__(self, postcode, function):
        #  Default URL
        self.base_url       = "192.168.1.227:8070"
        self.extension      = f"/{function}/"
        self.postcode       = str(postcode)
        code_data           = self.get_data()
        self.country        = (code_data["country"] if 'country' in code_data else "NA")
        self.region         = (code_data["region"] if 'region' in code_data else "NA")
        self.parish         = (code_data["parish"] if 'parish' in code_data else "NA")
        self.quality_rating = (code_data["quality"] if 'quality' in code_data else "NA")
        self.constituency   = { x: y for x, y in code_data.items() if "parliamentary" in x}
        self.admin          = { x: y for x, y in code_data.items() if "admin" in x}
        self.inoutcode      = { "outcode": code_data["outcode"], "incode": (code_data["incode"] if 'incode' in code_data else "NA")}
        self.lat_long       = { "latitude" : code_data["latitude"], "longitude" : code_data["longitude"] }
        self.east_north     = { "eastings" : code_data["eastings"], "northings": code_data["northings"]}
        self.raw_codes      = (code_data["codes"] if 'codes' in code_data else "NA")
        self.collection     = self.__iter__()

    def __iter__(self):
        yield from self.__dict__.items()

    def __str__(self):
        txt = io.StringIO()
        txt.write(f"{self.__class__.__name__}:\n")
        [
            txt.write(f"- {a}: {b} \n")
            for a, b in self.collection
            if a not in ["block", "collection", "contents"]
        ]
        txt.write(")")
        return txt.getvalue()

    def get_data(self):
        print(f"http://{self.base_url}{self.extension}{self.postcode}")
        return requests.get(f"http://{self.base_url}{self.extension}{self.postcode}").json()["result"]


data = {
    'nhs_ha': 'East of England',
    'european_electoral_region': 'Eastern',
    'primary_care_trust': 'West Essex',
    'lsoa': 'Uttlesford 002C',
    'msoa': 'Uttlesford 002',
    'date_of_introduction': '199507',
    'ced': 'Saffron Walden',
    'ccg': 'NHS Hertfordshire and West Essex',
    'nuts': 'Uttlesford',
    'pfa': 'Essex'}
