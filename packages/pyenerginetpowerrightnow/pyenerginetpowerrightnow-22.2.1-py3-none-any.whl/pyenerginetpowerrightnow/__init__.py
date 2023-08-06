
from urllib.request import urlopen
import json

def getCurrentData():
    url = buildUrl()
    data = fetchData(url)
    return mapData(data)

def buildUrl():
	return "https://prod-wwwenerginetdk-kort-app.azurewebsites.net/api/EDS?cacheName=PowerRightNow&dataset=powersystemrightnow&sort=Minutes1UTC%20desc_limit=1"

def fetchData(url):
    # download csv
    with urlopen(url) as response:
        result = dict()
        body = response.read()
        decoded_content = body.decode('utf-8')
        return json.loads(decoded_content)

def mapData(content):

    # this is what one sample looks like
    # {
    # "Minutes1UTC": "2023-02-07T13:33:00", "Minutes1DK": "2023-02-07T14:33:00",
    # "CO2Emission": 119.480003, "ProductionGe100MW": 1373.01001,
    # "ProductionLt100MW": 706.599976, "SolarPower": 424.899994,
    # "OffshoreWindPower": 826.75, "OnshoreWindPower": 1115.609985,
    # "Exchange_Sum": 58.669998, "Exchange_DK1_DE": -2301.310059,
    # "Exchange_DK1_NL": 461.390015, "Exchange_DK1_NO": 1109.280029,
    # "Exchange_DK1_SE": 715.0, "Exchange_DK1_DK2": -339.700012,
    # "Exchange_DK2_DE": 56.77, "Exchange_DK2_SE": 9.08,
    # "Exchange_Bornholm_SE": 8.46
    # }

    data = content['records'][0]
    data['total_power_usage_DK'] = data['ProductionGe100MW'] + data['ProductionLt100MW'] + data['SolarPower'] + data['OffshoreWindPower'] + data['OnshoreWindPower'] + data['Exchange_Sum']
    data['renewable_ratio'] = (data['SolarPower'] + data['OffshoreWindPower'] + data['OnshoreWindPower']) / data['total_power_usage_DK']
    return data
