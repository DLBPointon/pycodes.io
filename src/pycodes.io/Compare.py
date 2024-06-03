import io
from Postcode import PostcodeObj
from Doogal import DoogalObj

class ComparisonObj:
    def __init__(self, postcodes: PostcodeObj, doogal: DoogalObj):
        # Not saved as self to ensure a cleaner collection
        self.postcodes_call = f'{postcodes.base_url}{postcodes.extension}{postcodes.postcode}'
        self.doogal_call = f'{doogal.base_url}{doogal.extension}{doogal.postcode}'
        self.comparison = self.get_comparison(postcodes, doogal)

    def __str__(self):
        txt = io.StringIO()

        for x, y in {0: "Postcodes.io", 1: "Doogal"}.items():
            txt.write(f"\n\nField\t{y}\n")

            for k, v in self.comparison.items():
                txt.write(f'{k}\t{v[x]}\n')

        return txt.getvalue()

    def get_comparison(self, postcodesio, doogal):
        data_dict = {}
        data_dict['API_call'] = [self.postcodes_call, self.doogal_call]
        data_dict['Country'] = [postcodesio.country, doogal.country]
        data_dict['Region'] = [postcodesio.region, doogal.region]
        data_dict['Admin'] = [postcodesio.admin, doogal.admin]
        data_dict['Constituency'] = [postcodesio.constituency, doogal.constituency]
        data_dict['Parish'] = [postcodesio.parish, doogal.parish]
        data_dict['Q Rating'] = [postcodesio.quality_rating, doogal.quality_rating]
        data_dict['Lat/Long'] = [postcodesio.lat_long, doogal.lat_long]
        data_dict['East/North'] = [postcodesio.east_north, doogal.east_north]
        data_dict['Raw_Codes'] = [postcodesio.raw_codes, doogal.raw_codes]
        return data_dict
