import json
import requests
from os import path
from gsheet import open_sheet
from datetime import datetime

class C(object):
    HEADERS = {
        'x-rapidapi-host': "realtor.p.rapidapi.com",
        'x-rapidapi-key': ""
        }

    AOI = [
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
        },
        {
          "area_type": "city",
          "_id": "city:or_portland",
          "_score": 18.105978,
          "city": "Portland",
          "state_code": "OR",
          "country": "USA",
          "centroid": {
            "lon": -122.649971,
            "lat": 45.5369506
          },
          "geo_id": "b41cbc0e-3d4e-5c89-8f4a-475a92007ec5"
        }
    ]


def get_city(city='portland'):
    url = 'https://realtor.p.rapidapi.com/locations/auto-complete'

    querystring = {'input': city}

    headers = {
        'x-rapidapi-host': 'realtor.p.rapidapi.com',
        'x-rapidapi-key': ''
        }

    response = requests.get(url, headers=C.HEADERS, params=querystring)

    return response.json()


def get_sale_listings(city_details, property_id_list, limit=200, offset=0):
    url = 'https://realtor.p.rapidapi.com/properties/v2/list-for-sale'
    parameters = {
                   "beds_min":"1",
                   "sort":"newest",
                   "radius":"10",
                   "price_max":"450001",
                   "is_pending":"false",
                   #"features":"garage_1_or_more",
                   "limit":str(limit),
                   "offset":str(offset),
                   "prop_type": "single_family"
                 }
    city_details.update(parameters)

    querystring = city_details

    response = requests.get(url, headers=C.HEADERS, params=querystring)
    properties = response.json()['properties']

    new_properties = []
    for property in properties:
        if property['property_id'] in property_id_list:
            return new_properties
        else:
            new_properties.append(property)

    if properties:
        return new_properties + get_sale_listings(city_details, property_id_list, offset=offset+limit)

    return []

def find_new_listings():
    new_properties = []
    new_aoi_properties = []
    for aoi in C.AOI:
        properties = []
        if path.exists('%s.json' % aoi['city']):
            fin = open('%s.json' % aoi['city'], 'r')
            properties = json.load(fin)
            fin.close()

        property_id_list = [p['property_id'] for p in properties]
        new_aoi_properties = get_sale_listings(aoi, property_id_list)
        properties += new_aoi_properties
        print(aoi['city'], len(new_aoi_properties))
        new_properties += new_aoi_properties

        fout = open('%s.json' % aoi['city'], 'w')
        fout.write(json.dumps(properties, indent=2))
        fout.truncate()
        fout.close()
    return new_properties


def update_sheet(new_listings, sheet_id, range='robot_found'):
    sheet = open_sheet()
    row_num = _find_empty_row(sheet, sheet_id, range)

    rows = []
    property_ids = []
    for new_listing in new_listings:
        if new_listing['property_id'] not in property_ids:
            property_ids.append(new_listing['property_id'])
            row = [datetime.now().strftime('%Y-%m-%d %H:%M'), 'placy mcplace face']
            row.append(new_listing['property_id'])
            row.append(new_listing['listing_id'])
            row.append(new_listing['price'])
            row.append(new_listing['address']['line'])
            row.append(' '.join([str(ft) for ft in new_listing['building_size'].values()]) if 'building_size' in new_listing else '?')
            row.append('%s,%s' % (new_listing['address']['lat'], new_listing['address']['lon']))
            row.append(new_listing['address']['neighborhood_name'] if 'neighborhood_name' in new_listing['address'] else '?')
            row.append(', '.join([nl['name'] for nl in new_listing['agents']]))
            row.append(new_listing['office']['name'] if 'name' in new_listing['office'] else '?')

            rows.append(row)

    body = {'values': rows}
    result = sheet.values().update(spreadsheetId=sheet_id, valueInputOption='RAW', range='robot_found!A%s'%row_num, body=body).execute()

def _find_empty_row(sheet, sheet_id, range):
    result = sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
    return len(result.get('values', [])) + 1

listings = find_new_listings()
update_sheet(listings, '')
