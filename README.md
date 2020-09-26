# Robo Realtor
## About
Finds new real estate listings in your area and dumps them into a Google spreadsheet.

## Requirements:
### Install required python3 packages
- `pip3 install requests --user`
- `pip3 install google-api-python-client --user`
- `pip3 install google-auth-oauthlib --user`

### Get your RapidAPI key:
- Go to https://rapidapi.com/ and either create an account or sign in.
- Go to https://rapidapi.com/apidojo/api/realtor and get a Realtor API key (`X-RapidAPI-Key`)
- Copy and paste the API key into `config.yaml` as the value for `REALTOR_RAPIDAPI_KEY`
```
REALTOR_RAPIDAPI_KEY: thisIsToatallyAValidKey038ecp1ddc37jsndd2769111111
```

### Create an empty Google sheet
- Go to https://docs.google.com/spreadsheets/u/0/
- Create a new "Blank" spreadsheet document
- Name your sheet something other than, "Untitled spreadsheet" so it gets saved.
- From the URL bar, copy the value after `/d/` and before `/edit` (e.g. `ValidhWzoTTksvIZnQqZ-Legit-NotFakevTtpoVJfHA`)
- Paste the ID into `config.yaml` as the value for `DOCUMENT_ID`
```
DOCUMENT_ID: ValidhWzoTTksvIZnQqZ-Legit-NotFakevTtpoVJfHA
```

NOTE: If you renamed 'Sheet1' (a 'worksheet' in Excel terminology) in the spreadsheet to something else, be sure to update the `SHEET_NAME` value to match.

### Enable Google Sheets API
- Go to https://developers.google.com/sheets/api/quickstart/python
- Click the "Enable the Google Sheets API" button
    - Name your project whatever you like (e.g. 'robo realtor') or leave it as 'Quickstart' and click 'NEXT'
    - Keep your 'OAuth' client type as 'Desktop app' and click 'CREATE'
    - Click, 'DOWNLOAD CLIENT CONFIGURATION'
- Move `credentials.json` to the same directory as the rest of the robo_realtor files (where `gsheet.py` is) 

NOTE: We already did the other steps listed in the Quickstart guide; you can skip their steps 2 through 4
NOTE: The sample code they show you on this page should look very much like what is in `gsheet.py` if you want to be paranoid about security.

## Usage
### First run only - Get your area details:
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

### First run only - Modify `config.yaml`
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

### First run only - Initialize the dataset
Run the below command
```
user@linux$ python3 realty.py --init
```
This is the initial dataset of listings it will assume you have already seen. Although you can skip this step, I don't recommend it unless you want a HUGE google doc.

### Run Robo Realtor
Run the below command which will launch your browser to authenticate you with Google so your spreadsheet can be updated. This is an objectively terrible design, but it is what Google forces you to do.
```
user@linux$ python3 realty.py
Milwaukie 0
```
NOTE: When authenticating with Google, make sure the app name (set in the 'Enable Google Sheets API' step) matches what you entered. I mention this out of security paranoia.

The output shows you the name of a city (e.g. 'Milwaukie') followed by the number of new listings found since the previous run. Here that number is zero because we *just* initialized our dataset (e.g. the `--init`)
