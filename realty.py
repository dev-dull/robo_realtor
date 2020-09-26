import json
import yaml
import requests
from os import path
from CONSTS import C
from gsheet import open_sheet
from datetime import datetime
from argparse import ArgumentParser

def get_city(city):
    url = '/'.join([C.BASE_URL, C.ENDPOINT_GET_CITY])

    querystring = {C.API_KEYWORD_INPUT: city}
    response = requests.get(url, headers=C.HEADERS, params=querystring)

    return yaml.dump([response.json()[C.API_RESPONSE_KEYWORD_AUTOCOMPLETE][0]], default_flow_style=False)


def get_sale_listings(city_details, property_id_list, limit=200, offset=0):
    url = '/'.join([C.BASE_URL, C.ENDPOINT_GET_SALE_LISTINGS])
    parameters = C.QUERY_PARAMETERS

    # we depend on these things being true, so hard-code them.
    parameters['sort'] = 'newest'
    parameters['limit'] = str(limit)
    parameters['offset'] = str(offset)

    city_details.update(parameters)

    response = requests.get(url, headers=C.HEADERS, params=city_details)
    properties = response.json()[C.API_RESPONSE_KEYWORD_PROPERTIES]

    new_properties = []
    for _property in properties:
        if _property[C.API_RESPONSE_KEYWORD_PROPERTY_ID] in property_id_list:
            return new_properties
        else:
            new_properties.append(_property)

    if properties:
        return new_properties + get_sale_listings(city_details, property_id_list, offset=offset+limit)

    return []


def find_new_listings():
    new_properties = []
    new_aoi_properties = []
    for aoi in C.AREA_OF_INTEREST:
        properties = []
        if path.exists('%s.json' % aoi[C.API_KEYWORD_CITY]):
            fin = open('%s.json' % aoi[C.API_KEYWORD_CITY], 'r')
            properties = json.load(fin)
            fin.close()

        property_id_list = [p[C.API_RESPONSE_KEYWORD_PROPERTY_ID] for p in properties]
        new_aoi_properties = get_sale_listings(aoi, property_id_list)
        properties += new_aoi_properties
        print(aoi['city'], len(new_aoi_properties))
        new_properties += new_aoi_properties

        fout = open('%s.json' % aoi[C.API_KEYWORD_CITY], 'w')
        fout.write(json.dumps(properties, indent=2))
        fout.truncate()
        fout.close()
    return new_properties


def update_sheet(new_listings, sheet_id, range):
    sheet = open_sheet()
    row_num = _find_empty_row(sheet, sheet_id, range)

    rows = []
    property_ids = []
    for new_listing in new_listings:
        if new_listing[C.API_RESPONSE_KEYWORD_PROPERTY_ID] not in property_ids:
            property_ids.append(new_listing[C.API_RESPONSE_KEYWORD_PROPERTY_ID])
            row = [datetime.now().strftime(C.SHEET_TIMESTAMP_FORMAT), 'placy mcplace face']
            row.append(new_listing.get(C.API_RESPONSE_KEYWORD_PROPERTY_ID, '?'))
            row.append(new_listing.get(C.API_RESPONSE_KEYWORD_LISTING_ID, '?'))
            row.append(new_listing.get(C.API_RESPONSE_KEYWORD_PRICE, '?'))
            row.append(new_listing.get(C.API_RESPONSE_KEYWORD_ADDRESS, {}).get(C.API_RESPONSE_KEYWORD_LINE, '?'))
            row.append(' '.join([str(ft) for ft in new_listing[C.API_RESPONSE_KEYWORD_BUILDING_SIZE].values()]) if C.API_RESPONSE_KEYWORD_BUILDING_SIZE in new_listing else '?')
            row.append('%s,%s' % (new_listing[C.API_RESPONSE_KEYWORD_ADDRESS][C.API_RESPONSE_KEYWORD_LATITUDE], new_listing[C.API_RESPONSE_KEYWORD_ADDRESS][C.API_RESPONSE_KEYWORD_LONGITUDE]))
            row.append(new_listing[C.API_RESPONSE_KEYWORD_ADDRESS].get(C.API_RESPONSE_KEYWORD_NEIGHBORHOOD_NAME, '?'))
            row.append(', '.join([nl[C.API_RESPONSE_KEYWORD_NAME] for nl in new_listing.get(C.API_RESPONSE_KEYWORD_AGENTS, [])]))
            row.append(new_listing.get(C.API_RESPONSE_KEYWORD_OFFICE, {}).get(C.API_RESPONSE_KEYWORD_NAME, '?'))

            rows.append(row)

    if row_num == 1:
        rows = [['Date found', 'Name this location', 'Property ID', 'Listing ID', 'Price', 'Address', 'Building size', 'lat,lon', 'Neighborhood name', 'Agents', 'Realtor office']] + rows
    body = {'values': rows}
    result = sheet.values().update(spreadsheetId=sheet_id, valueInputOption='RAW', range='%s!A%s' % (C.SHEET_NAME, row_num), body=body).execute()


def _find_empty_row(sheet, sheet_id, range):
    result = sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
    return len(result.get('values', [])) + 1


def main():
    parser = ArgumentParser(description='Find new real estate listings for the locations defined in config.yaml')
    parser.add_argument('-c', '--get-city-details', dest='city', default=None,
                        help='Prints out the AREA_OF_INTEREST text needed in config.yaml')
    parser.add_argument('-i', '--init', dest='make_cache', action='store_true', default=False,
                        help='Builds an initial city cache of all listings that are available now.')
    args = parser.parse_args()

    if args.make_cache and args.city:
        print('Sorry, please use --get-city-details, update config.yaml, and then use --init')
    elif args.make_cache:
        find_new_listings()
    elif args.city:
        print('Add the following to the AREA_OF_INTEREST section of config.yaml:')
        print(get_city(args.city))
    else:
        listings = find_new_listings()
        update_sheet(listings, C.DOCUMENT_ID, C.SHEET_NAME)


if __name__ == '__main__':
    main()