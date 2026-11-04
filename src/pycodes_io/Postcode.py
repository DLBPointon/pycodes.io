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
        self.termination_status = code_data.get("TERMINATED", "INUSE")
        self.country = code_data.get("country", "NA")
        self.region = code_data.get("region", "NA")
        self.parish = code_data.get("parish", "NA")
        self.quality_rating = code_data.get("quality", "NA")
        self.constituency = {x: y for x, y in code_data.items() if "parliamentary" in x}
        self.admin = {x: y for x, y in code_data.items() if "admin" in x}
        self.admin_district = code_data.get("admin_district", "NA")
        self.admin_ward = code_data.get("admin_ward", "NA")
        self.lsoa = code_data.get("lsoa", "NA")
        self.lsoa21 = code_data.get("lsoa21", "NA")
        self.icb = code_data.get("icb", "NA")
        self.bua = code_data.get("bua", "NA")
        self.inoutcode = {
            "outcode": code_data.get("outcode", "TERMINATED"),
            "incode": code_data.get("incode", "TERMINATED"),
        }
        self.lat_long = {
            "latitude": code_data.get("latitude", "NA"),
            "longitude": code_data.get("longitude", "NA"),
        }
        self.east_north = {
            "eastings": code_data.get("eastings", "NA"),
            "northings": code_data.get("northings", "NA"),
        }
        self.raw_codes = code_data.get("codes", "NA")
        self.collection = self.__iter__()

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

    def validate_data(self, data) -> dict[str, str]:
        if "error" in data and data["error"] == "Postcode not found":
            return {"TERMINATED": "TERMINATED"}
        elif "result" in data:
            return data["result"]
        else:
            return {"FAILED": "FAILED"}

    def get_data(self):
        return requests.get(
            f"http://{self.base_url}{self.extension}{self.postcode}"
        ).json()


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
