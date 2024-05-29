import io
from Postcode import PostcodeObj
from Doogal import DoogalObj

class ComparisonObj:
    def __init__(self, postcode: PostcodeObj, doogal: DoogalObj):
        # Not saved as self to ensure a cleaner collection
        postcodes = postcode
        doogal = doogal
        self.postcodes_call = ""
        self.doogal_call = ""
        self.comparison = self.get_comparison(postcodes, doogal)
        self.collection = self.__iter__()

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

    def get_comparison(self, postcodesio, doogal):
        pass
