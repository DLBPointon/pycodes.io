import io
import requests

class DoogalObj:
    def __init__(self, postcode, function):
        #  Default URL
        self.base_url       = "www.doogal.co.uk"
        self.extension      = "/GetPostcode/"
        self.postcode       = str(postcode)
        self.code_data      = self.get_data()
        self.country        = (self.code_data["country"] if 'country' in self.code_data else "NA")
        self.region         = (self.code_data["region"] if 'region' in self.code_data else "NA")
        self.parish         = (self.code_data["parish"] if 'parish' in self.code_data else "NA")
        self.quality_rating = (self.code_data["quality"] if 'quality' in self.code_data else "NA")
        self.admin          = self.admin_codes()
        self.constituency   = { x: y for x, y in self.code_data.items() if "parliamentary" in x}
        self.inoutcode      = { "outcode": (self.code_data["outcode"] if 'outocode' in self.code_data else "NA"), "incode": (self.code_data["incode"] if 'incode' in self.code_data else "NA")}
        self.lat_long       = { "latitude" : self.code_data["latitude"], "longitude" : self.code_data["longitude"] }
        self.east_north     = { "eastings" : self.code_data["easting"], "northings": self.code_data["northing"]}
        self.raw_codes      = self.other_codes()
        self.collection     = self.__iter__()

    def __iter__(self):
        yield from self.__dict__.items()

    def __str__(self):
        txt = io.StringIO()
        txt.write(f"{self.__class__.__name__}:\n")
        [
            txt.write(f"- {a}: {b} \n")
            for a, b in self.collection
            if a not in ["block", "collection", "contents","code_data"]
        ]
        txt.write(")")
        return txt.getvalue()


    def admin_codes(self):
        admin_codes = {}
        for x, y in self.code_data.items():
            if x in ["district", "constituency", "ward"]:
                admin_codes[x] = y
        return admin_codes

    def other_codes(self):
        other_codes = {}
        for x, y in self.code_data.items():
            if x in ["lsoa", "wardCode"]:
                other_codes[x] = y
        return other_codes

    def get_data(self):
        print(f"http://{self.base_url}{self.extension}{self.postcode}?output=json")
        return requests.get(f"http://{self.base_url}{self.extension}{self.postcode}").json()


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
