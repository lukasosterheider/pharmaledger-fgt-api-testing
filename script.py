from time import sleep
import requests
from requests.auth import HTTPBasicAuth
import gtin
import random
import string
import json

# Variables
api = "https://api-mah-bayer-fgt.pharmaledger.pdmfc.com/"
user = "MAH251339219"
password = "This1sSuchAS3curePassw0rd"
basicAuth = HTTPBasicAuth(user, password)
headers = {"Content-Type": "application/json", "accept": "application/json"}

numberOfProducts = 3
numberOfBatches = 3 # per product
numberOfSerials = 300 # per batch
# numberOfShipments = 1 # per batch

products = []
batches = []
shipments = []

expiryDate = "2030-01-01"

shipmentReceiver = "PHA228233000"

# Create Products

for x in range(numberOfProducts):
    rand = random.randint(1000000000000,9999999999999)
    gtinNumber = int(gtin.GTIN(raw=rand))
    name = "Sample Product " + ''.join(random.choices(string.ascii_uppercase, k=8))
    description = ''.join(random.choices(string.ascii_lowercase, k=16))
    
    products.append(gtinNumber)
    
    payload = {'name':name, 'gtin':str(gtinNumber), 'description':description}
    response = requests.post(api + "traceability/product/create", auth=basicAuth, headers=headers , data = json.dumps(payload))

    print(response)
    # print(response.content)

print("Products: " + str(products))

# Create Batches

for x in products:
    for y in range(numberOfBatches):
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        serialNumbers = []
        for z in range(numberOfSerials):
            serial = random.randint(1000000000,9999999999)
            serialNumbers.append(serial)
        
        batches.append([x, rand])

        payload = {'gtin':str(x), 'batchNumber':rand, 'expiry':expiryDate, 'serialNumbers':serialNumbers}
        response = requests.post(api + "traceability/batch/create", auth=basicAuth, headers=headers , data = json.dumps(payload))

        print(response)
        # print(response.content)

print("Batches: " + str(batches))

# Create Shipments

for x in range(len(batches)):
    gtinNumber = batches[x][0]
    batchNumber = batches[x][1]

    shipmentId = rand = random.randint(10000000,99999999)

    shipments.append(shipmentId)

    payload = {'shipmentId':str(shipmentId), 'requesterId': shipmentReceiver, 'shipmentLines':[{'gtin':str(gtinNumber), 'batch':batchNumber,  'quantity':numberOfSerials}]}
    response = requests.post(api + "traceability/shipment/create", auth=basicAuth, headers=headers , data = json.dumps(payload))
    print(response)

print("Shipments: " + str(shipments))

# Wait for Shipment creation at Recipient

print("Sleeping now for 3 minutes...")
sleep(180)
print("Sleep completed - starting with updating the shipment status")

# Update Shipment Status

for x in shipments:
    payload1 = {'status':'pickup'}
    payload2 = {'status':'transit'}
    payload3 = {'status':'delivered'}

    sleep(1)

    response = requests.put(api + "traceability/shipment/update/" + str(x), auth=basicAuth, headers=headers , data = json.dumps(payload1))
    print(response)

    sleep(1)

    response = requests.put(api + "traceability/shipment/update/" + str(x), auth=basicAuth, headers=headers , data = json.dumps(payload2))
    print(response)

    sleep(1)

    response = requests.put(api + "traceability/shipment/update/" + str(x), auth=basicAuth, headers=headers , data = json.dumps(payload3))
    print(response)

print("Done!")