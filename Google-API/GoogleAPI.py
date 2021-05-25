import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("WetterstationIT.json", scope)

client = gspread.authorize(creds)

locations = ("Euskirchen", "Muetzenich", "Schmidt")
parameters = ("Temperatur", "Humidity", "Pressure")

def measurement_data():

    location = input ("Bitte geben sie einen Ort ein ({}): ".format(locations))

    while location not in locations:
        print("Ort nicht verfügbar - Bitte erneut Eingeben.")
        location = input("Bitte geben Sie einen Ort ein ({}): ".format(locations))


    parameter = input ("Welchen Parameter möchten Sie abfragen? ({})\nBitte geben Sie einen Parameter ein: ".format(parameters))

    while parameter not in parameters:
        print("Parameter nicht verfügbar - Bitte erneut Eingeben.")
        parameter = input("Bitte geben Sie einen Parameter ein ({}): ".format(parameters))


    sheet = client.open(location).sheet1  # Open the spreadhseet
    data = sheet.get_all_records()  # Get a list of all records
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])

    def no_unit (data):
        no_unit_list = []
        for i in data:
            if parameter == "Temperatur":
                sep_no_unit = i["Temperatur"].split("C")
                no_unit_list.append(sep_no_unit)
            elif parameter == "Humidity":
                sep_no_unit = i["Humidity"].split("%")
                no_unit_list.append(sep_no_unit)
            elif parameter == "Pressure":
                sep_no_unit = i["Pressure"].split("hPa")
                no_unit_list.append(sep_no_unit)
            else:
                print("Parameter ungültig. Bitte neustarten")
        df_no_unit = pd.DataFrame(no_unit_list).drop(1, axis=1)
        return df_no_unit

    df_no_unit = no_unit(data)
    df_no_unit.rename(columns={0:"{}".format(parameter)}, inplace=True)


    df_datetime_parameter = df[["Date"]].join(df_no_unit)
    df_datetime_parameter_indexed = df_datetime_parameter.set_index("Date")
    df_datetime_parameter_indexed_convert = df_datetime_parameter_indexed[["{}".format(parameter)]].astype(float)
    all_data = df_datetime_parameter_indexed_convert

    return all_data

all_data = measurement_data()

print(all_data)
print(all_data.dtypes)
all_data.plot()
plt.show()