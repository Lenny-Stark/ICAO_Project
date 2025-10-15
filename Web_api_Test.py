import requests

ICAO = input("Geben sie den gewünschten ICAO Code ein: ")
url = f"https://airportdb.io/api/v1/airport/{ICAO}?apiToken=9747fdf8c4dde53ccbcd81be10d42d8ad1ec61d2a24ff582f77b9c875a40230af9adf5585fa7cb0c785f7ec9b67a3227"
response = requests.get(url) #response ist info die https anfrage funktioniert hat
print(response)

data = response.json() #data ist die json von der url
print(f"Flughafen Name: {data['name']}")

#Zugriff auf einzelne frequenzen
for i in data["runways"]:
    rw_count=0
    if i:
        rw_count += 1
print(f"This airport has {rw_count} runways")