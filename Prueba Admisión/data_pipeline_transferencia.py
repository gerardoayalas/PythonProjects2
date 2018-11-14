import requests
import simplejson as json
import pandas as pd
import csv

# Get Data
response = requests.get("https://api.datos.observatoriologistico.cl/api/v2/datastreams/TEST-12708/data.json/?auth_key=0638a1e7e481ffed0849fd47588de259dfc122b5")#&limit=20")
jsonData = response.content
jsonData = json.loads(jsonData)
rows = jsonData["result"]["fRows"]
cols = jsonData["result"]["fCols"]
jsonData = jsonData['result']["fArray"]

# Transform json to Data Frame
data = [list(x.values())[0] for x in jsonData]
data = [0 if x == "" else x for x in data]
data = [data[x*cols:x*cols+cols] for x in range(rows)]
dataResp = data
data = pd.DataFrame(data[1:])

# Aggregate Data Frame
dataAgg = data.groupby([2,5,0,6,7]).sum()

# Create json
jsonResult = '{ "result": {"fLength": '+str(6*len(dataAgg.index.values))+', "fType": "ARRAY", "fTimestamp": null, "fArray": ['
jsonResult += '{"fType": "TEXT", "fStr": "AÑO", "fHeader": True}, {"fType": "TEXT", "fStr": "REGIÓN", "fHeader": True}, {"fType": "TEXT", "fStr": "PUERTO", "fHeader": True}, {"fType": "TEXT", "fStr": "LATITUD", "fHeader": True}, {"fType": "TEXT", "fStr": "LONGITUD", "fHeader": True}, {"fType": "TEXT", "fStr": "TONELADAS", "fHeader": True}'
c = 0
for x in dataAgg.index.values:
    jsonResult += ', {"fStr": "'+x[0]+'", "fType": "TEXT"}'
    jsonResult += ', {"fStr": "'+str(x[1])+'", "fType": "TEXT"}'
    jsonResult += ', {"fStr": "'+x[2]+'", "fType": "TEXT"}'
    jsonResult += ', {"fNum": '+str(x[3])+', "fType": "NUMBER", "fFormat": {"fPattern": "#,###.##", "fLocale": "en-US"}, "fDisplayFormat": {"fPattern": "#,###.##", "fLocale": "es", "fLang": "es"}}'
    jsonResult += ', {"fNum": '+str(x[4])+', "fType": "NUMBER", "fFormat": {"fPattern": "#,###.##", "fLocale": "en-US"}, "fDisplayFormat": {"fPattern": "#,###.##", "fLocale": "es", "fLang": "es"}}'
    jsonResult += ', {"fNum": '+str(dataAgg.get_values()[c][0])+', "fType": "NUMBER", "fFormat": {"fPattern": "#,###.##", "fLocale": "en-US"}, "fDisplayFormat": {"fPattern": "#,###", "fLocale": "es", "fLang": "es"}}'
    c += 1
jsonResult += '], "fRows": '+str(len(dataAgg.index.values))+', "fCols": 6}}'

# Write json
with open("toneladas_transferencia_agregado.json", "w") as text_file:
    text_file.write(jsonResult)

# Export data for analysis
with open("data_analysis.csv", "w", newline="") as myfile:
    wr = csv.writer(myfile)
    for i in dataResp:
        wr.writerow(i)