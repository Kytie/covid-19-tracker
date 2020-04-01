import yaml
import argparse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='Get coronavirus stats')
parser.add_argument('-s', '--stat', type=str, help='Type of stat you want produced.')
parser.add_argument('-d', '--days', type=int, help='Number of days to filter by.')
args = parser.parse_args()

statsFile=open('./stats-file.txt', 'w+')

with open('covid-19.yaml') as file:
    dataFile = yaml.load(file, Loader=yaml.FullLoader)
    worldData = dataFile['World']
    countryData = dataFile['Country']

if args.stat:
    if(str.lower(args.stat) == 'change'):
        if args.days:
            today = datetime.today().date()
            targetDate = today - timedelta(days=args.days)
            todayEntry = {}
            targetEntry = {}
            dataFound = True
            print("Changes since: {}".format(targetDate), file=statsFile)
            for entry in worldData:
                if(todayEntry and targetEntry):
                    break
                if(entry['Date'] == today):
                    todayEntry = entry
                if(entry['Date'] == targetDate):
                    targetEntry = entry
            
            if(not todayEntry):
                print("Today's data not found for world.", file=statsFile)
                print(file=statsFile)
                dataFound = False
            if(not targetEntry):
                print("Target date data not found for world.", file=statsFile)
                print(file=statsFile)
                dataFound = False
            if(dataFound) :
                print("World:" + 
                    "\n\tConfirmed: {}".format(todayEntry["Confirmed"] - targetEntry["Confirmed"]) +
                    "\n\tDeaths: {}".format(todayEntry["Deaths"] - targetEntry["Deaths"]) +
                    "\n\tRecovered: {}".format(todayEntry["Recovered"] - targetEntry["Recovered"]) +
                    "\n\tExisting: {}".format(todayEntry["Existing"] - targetEntry["Existing"]), file=statsFile
                )
                print("-----------------------------------------------", file=statsFile)

            for country in countryData:
                todayEntry = {}
                targetEntry = {}
                dataFound = True
                for entry in countryData[country]:
                    if(todayEntry and targetEntry):
                        break
                    if(entry['Date'] == today):
                        todayEntry = entry
                    if(entry['Date'] == targetDate):
                        targetEntry = entry
                if(not todayEntry):
                    print("Today's data not found for country: {}".format(country), file=statsFile)
                    print(file=statsFile)
                    dataFound = False
                if(not targetEntry):
                    print("Target date data not found for country: {}".format(country), file=statsFile)
                    print(file=statsFile)
                    dataFound = False
                if(dataFound):
                    print("{}:".format(country) +
                        "\n\tConfirmed: {}".format(todayEntry["Confirmed"] - targetEntry["Confirmed"]) +
                        "\n\tDeaths: {}".format(todayEntry["Deaths"] - targetEntry["Deaths"]) +
                        "\n\tRecovered: {}".format(todayEntry["Recovered"] - targetEntry["Recovered"]) +
                        "\n\tExisting: {}".format(todayEntry["Existing"] - targetEntry["Existing"]), file=statsFile
                    )
                    print(file=statsFile)
        else:
            print("No days given.")
    elif(str.lower(args.stat) == 'deaths'):
        if not args.days:
            args.days = 0
        for daysSpan in range (0, args.days + 1):
            today = datetime.today().date()
            targetDate = today - timedelta(days=daysSpan)
            todayEntry = {}
            dataFound = True
            print("{} Death Stastistics".format(targetDate), file=statsFile)
            for entry in worldData:
                if(entry['Date'] == targetDate):
                    todayEntry = entry
                    break
            if(not todayEntry):
                print("Today's data not found for world.", file=statsFile)
                dataFound = False
            if(dataFound):
                print("World:" + 
                    "\n\tConfirmed Cases: {}".format(todayEntry["Confirmed"]) +
                    "\n\tDeaths: {}".format(todayEntry["Deaths"]) +
                    "\n\tPercent: {}%".format(round((todayEntry["Deaths"]/todayEntry["Confirmed"])*100, 2)), file=statsFile
                )
                print("-----------------------------------------------", file=statsFile)
            for country in countryData:
                dataFound = True
                todayEntry = {}
                for entry in countryData[country]:
                    if(entry['Date'] == targetDate):
                        todayEntry = entry
                        break
                if(not todayEntry):
                    print("Today's data not found for country: {}".format(country), file=statsFile)
                    print(file=statsFile)
                    dataFound = False
                if(dataFound):
                    print("{}:".format(country) + 
                        "\n\tConfirmed Cases: {}".format(todayEntry["Confirmed"]) +
                        "\n\tDeaths: {}".format(todayEntry["Deaths"]) +
                        "\n\tPercent: {}%".format(round((todayEntry["Deaths"]/todayEntry["Confirmed"])*100, 2)), file=statsFile
                    )
                    print(file=statsFile)
    else:
        print("Unrecognised Stat.")
else:
    print("No arguments given.")

statsFile.close()
