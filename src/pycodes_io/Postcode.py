import io

import requests


class PostcodeObj:
    def __init__(self, postcode, function, base_url):
        #  Default URL
        self.base_url = base_url
        self.extension = f"/{function}/"
        self.postcode = str(postcode)
        tmp_data = self.get_data()
        code_data: dict = self.validate_data(tmp_data)
        self.termination_status = code_data["TERMINATED"] if "TERMINATED" in code_data else "INUSE"
        self.country = code_data["country"] if "country" in code_data else "NA"
        self.region = code_data["region"] if "region" in code_data else "NA"
        self.parish = code_data["parish"] if "parish" in code_data else "NA"
        self.quality_rating = code_data["quality"] if "quality" in code_data else "NA"
        self.constituency = {x: y for x, y in code_data.items() if "parliamentary" in x}
        self.admin = {x: y for x, y in code_data.items() if "admin" in x}
        self.admin_district = code_data["admin_district"] if "admin_district" in code_data else "NA"
        self.admin_ward = code_data["admin_ward"] if "admin_ward" in code_data else "NA"
        self.lsoa = code_data["lsoa"] if "lsoa" in code_data else "NA"
        self.lsoa21 = code_data["lsoa21"] if "lsoa21" in code_data else "NA"
        self.icb = code_data["icb"] if "icb" in code_data else "NA"
        self.bua = code_data["bua"] if "bua" in code_data else "NA"
        self.inoutcode = (
            {
                "outcode": code_data["outcode"],
                "incode": (code_data["incode"] if "incode" in code_data else "NA"),
            }
            if "outcode" in code_data
            else {"outcode": "TERMINATED", "incode": "TERMINATED"}
        )
        self.lat_long = (
            {
                "latitude": code_data["latitude"],
                "longitude": code_data["longitude"],
            }
            if "latitude" in code_data
            else {"latitude": "NA", "longitude": "NA"}
        )
        self.east_north = (
            {
                "eastings": code_data["eastings"],
                "northings": code_data["northings"],
            }
            if "eastings" in code_data
            else {"eastings": "NA", "northings": "NA"}
        )
        self.raw_codes = code_data["codes"] if "codes" in code_data else "NA"
        self.collection = self.__iter__()

    def __iter__(self):
        yield from self.__dict__.items()

    def __str__(self):
        txt = io.StringIO()
        txt.write(f"{self.__class__.__name__}:\n")
        [txt.write(f"- {a}: {b} \n") for a, b in self.collection if a not in ["block", "collection", "contents"]]
        txt.write(")")
        return txt.getvalue()

    def validate_data(self, data) -> dict[str, str]:
        if "error" in data and data["error"] == "Postcode not found":
            return {"TERMINATED": "TERMINATED"}
        if "result" in data:
            return data["result"]

    def get_data(self):
        return requests.get(f"http://{self.base_url}{self.extension}{self.postcode}").json()["result"]


data = {
    "nhs_ha": "East of England",
    "european_electoral_region": "Eastern",
    "primary_care_trust": "West Essex",
    "lsoa": "Uttlesford 002C",
    "msoa": "Uttlesford 002",
    "date_of_introduction": "199507",
    "ced": "Saffron Walden",
    "ccg": "NHS Hertfordshire and West Essex",
    "nuts": "Uttlesford",
    "pfa": "Essex",
}
