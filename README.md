# Robo Realtor
## About
Finds new real estate listings in your area and dumps them into a Google spreadsheet.

## Requirements:
- `pip3 install requests --user`
- `pip3 install google-api-python-client --user`
- `pip3 install google-auth-oauthlib --user`

## Usage
### Get your area details:
```shell script
user@linux robo_realtor$ python3 realty.py -c "milwaukie, or"
Add the following to the AREA_OF_INTEREST section of config.yaml:
- _id: city:or_milwaukie
  _score: 36035.273
  area_type: city
  centroid:
    lat: 45.4448485
    lon: -122.6232989
  city: Milwaukie
  country: USA
  geo_id: 6d1bea9c-f367-5f98-ad22-bc85bfc3d22f
  slug_id: Milwaukie_OR
  state_code: OR
```
### Modify `config.yaml`
Copy and paste the above output into `config.yaml` under the `AREA_OF_INTEREST` section. Note that you can add multiple areas, just make sure each one has the leading dash (`- `)
```
AREA_OF_INTEREST:
- _id: city:or_milwaukie
  _score: 36035.273
  area_type: city
  centroid:
    lat: 45.4448485
    lon: -122.6232989
  city: Milwaukie
  country: USA
  geo_id: 6d1bea9c-f367-5f98-ad22-bc85bfc3d22f
  slug_id: Milwaukie_OR
  state_code: OR
```

