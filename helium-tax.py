import requests
import json
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

address = ''
year = '2021'
yearend = str(int(year)+1)
baseurl = f"https://api.helium.io/v1/hotspots/{address}/rewards?max_time={yearend}-01-01&min_time={year}-01-01"
baseoracle = "https://api.helium.io/v1/oracle/prices/"
rewards = requests.get(baseurl, verify=False)
datadump = rewards.json()
transactions = [['date', 'hnt', 'hnt price', 'USD earned', 'block']]
try:
	endcursor = datadump['cursor']
	currentcursor = datadump['cursor']
except KeyError:
	endcursor = "start"

while (True):
	data = datadump['data']
	for datum in data:
		activity = datum['type']
		time = datum['timestamp']
		block = str(datum['block'])
		#print(block)
		hnt = datum['amount']/100000000
		#print(hnt)
		oracle = requests.get(baseoracle+block, verify=False)
		oracle = oracle.json()
		oracleprice = oracle['data']['price']/100000000
		usd = hnt*oracleprice
		transactions.append([time, hnt, oracleprice, usd, block])
	try:
		currentcursor = datadump['cursor']
	except KeyError:
		break
	rewards = requests.get(f'https://api.helium.io/v1/hotspots/{address}/rewards?cursor={currentcursor}', verify=False)
	datadump = rewards.json()

with open("helium.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(transactions)
