import io

import requests


class DoogalObj:
    def __init__(self, postcode, function):
        #  Default URL
        self.base_url = "www.doogal.co.uk"
        self.extension = "/GetPostcode/"
        self.postcode = str(postcode)
        code_data = self.get_data()  # JSON
        self.country = code_data["country"] if "country" in code_data else "NA"
        self.region = code_data["region"] if "region" in code_data else "NA"
        self.parish = code_data["parish"] if "parish" in code_data else "NA"
        self.quality_rating = code_data["quality"] if "quality" in code_data else "NA"
        self.admin = self.admin_codes(code_data)
        self.constituency = {x: y for x, y in code_data.items() if "parliamentary" in x}
        self.inoutcode = {
            "outcode": (code_data["outcode"] if "outocode" in code_data else "NA"),
            "incode": (code_data["incode"] if "incode" in code_data else "NA"),
        }
        self.lat_long = {"latitude": code_data["latitude"], "longitude": code_data["longitude"]}
        self.east_north = {"eastings": code_data["easting"], "northings": code_data["northing"]}
        self.raw_codes = self.other_codes(code_data)
        self.collection = self.__iter__()

    def __iter__(self):
        yield from self.__dict__.items()

    def __str__(self):
        txt = io.StringIO()
        txt.write(f"{self.__class__.__name__}:\n")
        [
            txt.write(f"- {a}: {b} \n")
            for a, b in self.collection
            if a not in ["block", "collection", "contents", "code_data"]
        ]
        txt.write(")")
        return txt.getvalue()

    def admin_codes(self, code_data):
        admin_codes = {}
        for x, y in code_data.items():
            if x in ["district", "constituency", "ward", "admin"]:
                admin_codes[x] = y
        return admin_codes

    def other_codes(self, code_data):
        other_codes = {}
        for x, y in code_data.items():
            if x in ["lsoa", "wardCode"]:
                other_codes[x] = y
        return other_codes

    def get_data(self):
        return requests.get(f"http://{self.base_url}{self.extension}{self.postcode}").json()[
            "result"
        ]
