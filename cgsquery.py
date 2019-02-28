import requests
import json
import csv

def coinUrl(objectIds):
    url = 'https://spatialservices.conservation.ca.gov/arcgis/rest/services/CGS_Earthquake_Hazard_Zones/SHP_ZoneInfo/MapServer/0/query?where='
    for obj in objectIds[:-1]:
        url += 'OBJECTID+%3D+' + str(obj) + '+OR+'
    # Append last objectId without 'OR' string
    url += 'OBJECTID+%3D+' + str(objectIds[-1])
    url += '&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson'
    return url

# Main function
count = 0
oids = []
with open("inids.txt") as infile:
    f = csv.writer(open("output.csv", "a+"))
    for line in infile:
        count += 1
        # remove , suffix and whitespace prefix on each line to get objectId only from input file
        objectid = line[2:-2]
        # create a list of objectIds
        oids.append(int(objectid))
        # After collecting 60 objectIds do HTTP request to spatialservices site
        if count % 2 == 0:
            print(oids)
            url = coinUrl(oids)
            oids.clear()
            response=requests.get(url)
            jsonData = json.loads(response.content)
            for x in jsonData['features']:
                city=x['attributes']['SITE_CITY']
                parcel=x['attributes']['PARCELAPN']
                obj=x['attributes']['OBJECTID']
                address=x['attributes']['FullStreetAddress']
                liq=x['attributes']['LiquefactionZone']
                if "LIES WITHIN a Liquefaction Zone" in liq:
                    liqval = "1"
                elif "NOT been EVALUATED by CGS for liquefaction hazards" in liq:
                    liqval = "NA"
                else:
                    liqval = "0"
                land=x['attributes']['LandslideZone']
                if "LIES WITHIN a Landslide Zone" in land:
                    landval = "1"
                elif "NOT been EVALUATED by" in land:
                    landval = "NA"
                else:
                    landval = "0"
                fault=x['attributes']['FaultZone']
                if "LIES WITHIN an Earthquake Fault Zone" in fault:
                    faultval = "1"
                elif "NOT WITHIN an Earthquake Fault Zone" in fault:
                    faultval = "0"
                else:
                    faultval = "NA"
                f.writerow([parcel,obj,address,city,liqval,landval,faultval])


'''
https://spatialservices.conservation.ca.gov/arcgis/rest/services/CGS_Earthquake_Hazard_Zones/SHP_ZoneInfo/MapServer/0/query?where=OBJECTID+%3D+2691002+OR+OBJECTID+%3D+2691003&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson
        #oids = list(range(2560881,2560884))
        #oids = [2450096,2450113,2450116]
        #f.writerow(["parcelapn", "objectid", "address", "site_city", "liquiefaction", "landslide", "faultzone"])
#response=requests.get('https://spatialservices.conservation.ca.gov/arcgis/rest/services/CGS_Earthquake_Hazard_Zones/SHP_ZoneInfo/MapServer/0/query?where=OBJECTID+%3E+1+AND+OBJECTID+%3C+3&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson')
'''
