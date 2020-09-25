import yaml

class C(object):
    # Values are set in config.yaml
    AREA_OF_INTREST = [
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

    BASE_URL = 'https://realtor.p.rapidapi.com/'


    # Define that these things exist so IDEs don't complain
    # Values are set outside the class so users can't overwrite values via config.yaml
    HEADERS = {}
    ENDPOINT_GET_CITY = ''


# Inject user set values into Constants
fin = open('config.yaml', 'r')
yams = fin.read()
fin.close()
yamo = yaml.load(yams)
for k,v in yamo.items():
    setattr(C, k, v)

# Setting values that the user should not be able to override
ENDPOINT_GET_CITY = 'locations/auto-complete'
HEADERS = {
    'x-rapidapi-host': 'realtor.p.rapidapi.com',
    'x-rapidapi-key': ''
    }