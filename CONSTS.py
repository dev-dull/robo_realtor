import yaml


class C(object):
    # User can override values in config.yaml
    DOCUMENT_ID = ''
    SHEET_NAME = 'Sheet1'
    SHEET_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M'
    AREA_OF_INTEREST = [
        {
          "area_type": "city",
          "_id": "city:or_milwaukie",
          "_score": 36035.258,
          "city": "Milwaukie",
          "state_code": "OR",
          "country": "USA",
          "centroid": {
            "lon": -122.6232989,
            "lat": 45.4448485
          },
          "geo_id": "6d1bea9c-f367-5f98-ad22-bc85bfc3d22f"
        }
    ]

    REALTOR_RAPIDAPI_KEY = 'NOT CONFIGURED in config.yaml'

    BASE_URL = 'https://realtor.p.rapidapi.com'

    # Define that these things exist so IDEs don't complain
    # Values are set outside the class so users can't overwrite values via config.yaml
    HEADER_KEYWORD_RAPIDAPI_HOST = ''
    HEADER_KEYWORD_RAPIDAPI_KEY = ''
    HEADERS = {}

    ENDPOINT_GET_CITY = ''
    ENDPOINT_GET_SALE_LISTINGS = ''

    API_KEYWORD_INPUT = ''
    API_KEYWORD_CITY = ''

    API_RESPONSE_KEYWORD_AUTOCOMPLETE = ''
    API_RESPONSE_KEYWORD_PROPERTIES = ''
    API_RESPONSE_KEYWORD_PROPERTY_ID = ''
    API_RESPONSE_KEYWORD_LISTING_ID = ''
    API_RESPONSE_KEYWORD_PRICE = ''
    API_RESPONSE_KEYWORD_ADDRESS = ''
    API_RESPONSE_KEYWORD_LINE = ''
    API_RESPONSE_KEYWORD_BUILDING_SIZE = ''
    API_RESPONSE_KEYWORD_LATITUDE = ''
    API_RESPONSE_KEYWORD_LONGITUDE = ''
    API_RESPONSE_KEYWORD_NEIGHBORHOOD_NAME = ''
    API_RESPONSE_KEYWORD_NAME = ''
    API_RESPONSE_KEYWORD_AGENTS = ''
    API_RESPONSE_KEYWORD_OFFICE = ''


# Inject user set values into the class C
fin = open('config.yaml', 'r')
yams = fin.read()
fin.close()
yamo = yaml.load(yams, Loader=yaml.SafeLoader)
for k,v in yamo.items():
    setattr(C, k, v)

# Setting values that the user should not be able to override
C.ENDPOINT_GET_CITY = 'locations/auto-complete'
C.ENDPOINT_GET_SALE_LISTINGS = 'properties/v2/list-for-sale'

C.HEADER_KEYWORD_RAPIDAPI_HOST = 'x-rapidapi-host'
C.HEADER_KEYWORD_RAPIDAPI_KEY = 'x-rapidapi-key'
C.HEADERS = {
    C.HEADER_KEYWORD_RAPIDAPI_HOST: 'realtor.p.rapidapi.com',
    C.HEADER_KEYWORD_RAPIDAPI_KEY: C.REALTOR_RAPIDAPI_KEY
    }

C.API_KEYWORD_INPUT = 'input'
C.API_KEYWORD_CITY = 'city'

C.API_RESPONSE_KEYWORD_AUTOCOMPLETE = 'autocomplete'
C.API_RESPONSE_KEYWORD_PROPERTIES = 'properties'
C.API_RESPONSE_KEYWORD_PROPERTY_ID = 'property_id'
C.API_RESPONSE_KEYWORD_LISTING_ID = 'listing_id'
C.API_RESPONSE_KEYWORD_PRICE = 'price'
C.API_RESPONSE_KEYWORD_ADDRESS = 'address'
C.API_RESPONSE_KEYWORD_LINE = 'line'
C.API_RESPONSE_KEYWORD_BUILDING_SIZE = 'building_size'
C.API_RESPONSE_KEYWORD_LATITUDE = 'lat'
C.API_RESPONSE_KEYWORD_LONGITUDE = 'lon'
C.API_RESPONSE_KEYWORD_NEIGHBORHOOD_NAME = 'neighborhood_name'
C.API_RESPONSE_KEYWORD_NAME = 'name'
C.API_RESPONSE_KEYWORD_AGENTS = 'agents'
C.API_RESPONSE_KEYWORD_OFFICE = 'office'