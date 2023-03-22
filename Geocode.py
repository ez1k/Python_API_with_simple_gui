import pandas as pd
import os
import requests
import PySimpleGUI as sg

local_path = os.path.expanduser('~\\Documents\\github\\GeoKodowanie\\')

def get_data(country, city_name):
    WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q="
    api_key = "97d8990dc09a98a2a1479ec044bac0eb"
    complete_url = WEATHER_URL + city_name + "," + country + "&APPID=" + api_key + "&units=metric"
    
    response = requests.get(complete_url)
    json_Data = response.json()

    if json_Data["cod"] != "404":
        coordinates = json_Data["coord"]
        latitude = coordinates['lat']
        longitude = coordinates['lon']

        wind_data = json_Data['wind']
        wind_speed = wind_data['speed']
    
        main_data_weather = json_Data["main"]
        current_temperature = main_data_weather["temp"]
        current_pressure = main_data_weather["pressure"]
        current_humidity = main_data_weather["humidity"]
        
        weather_description = json_Data["weather"]
        weather_description = weather_description[0]["description"]
    
    else:
        print(" City Not Found ")

    
    
    return current_temperature, wind_speed, current_pressure, current_humidity, weather_description, latitude, longitude


def collect_data(df):
    for index, row in df.iterrows():
            current_temperature, wind_speed, current_pressure, current_humidity, weather_description, latitude, longitude = get_data(row['country'], row['city'])
            df.loc[index, 'Temperature'] = current_temperature  
            df.loc[index, 'Wind Speed'] = wind_speed
            df.loc[index, 'Pressure'] = current_pressure
            df.loc[index, 'Humidity'] = current_humidity
            df.loc[index, 'Description'] = weather_description
            df.loc[index, 'Latitude'] = latitude
            df.loc[index, 'Longitude'] = longitude
    return df




layout = [
    [sg.Text('Select a file to import:')],
    [sg.Input(key='_FILE_'), sg.FileBrowse()],
    [sg.Button('Import'), sg.Button('Cancel')],
    [sg.Button('TEST')],
    [sg.Button('single test')]
]

window = sg.Window('Weather API', layout)


while True:
    if os.path.exists(local_path+"list.xlsx"):
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'Import':
            filename = values['_FILE_']
            if filename == "":
                sg.popup(f'The file {filename} is empty.')
            else:
                try:
                    df = pd.read_excel(filename)
                    sg.popup(f'The file {filename} has been imported.\n\nNumber of rows: {len(df)}')
                    df = collect_data(df)
                    table_layout = [[col for col in df.columns]]
                    for row in df.itertuples(index=False):
                        table_layout.append(row)
                    table_window = sg.Window('Imported Data', [[sg.Table(table_layout)]])
                    table_window.read()
                    table_window.close()
                except pd.errors.EmptyDataError:
                    sg.popup(f'The file {filename} is empty.')
        elif event == 'TEST':
            df = pd.read_excel(local_path+"list.xlsx")
            df = collect_data(df)
            table_layout = [[col for col in df.columns]]
            for row in df.itertuples(index=False):
                table_layout.append(row)
            table_window = sg.Window('Imported Data', [[sg.Table(table_layout)]])
            table_window.read()
            table_window.close()
            df.to_excel(local_path+"results.xlsx")
            sg.popup(f"Check the list.xlsx in " + local_path)
        elif event == 'single test':
            layout = [
                [sg.Text('Enter Country:'), sg.InputText(key='_COUNTRY_')],
                [sg.Text('Enter City:'), sg.InputText(key='_CITY_')],
                [sg.Button('Submit')]
            ]
            window_test = sg.Window('Single Test', layout)
            event_test, values_test = window_test.read()
            if event_test == sg.WIN_CLOSED or event_test == 'Cancel':
                break
            elif event_test == 'Submit':
                country = values_test['_COUNTRY_']
                city = values_test['_CITY_']
                current_temperature, wind_speed, current_pressure, current_humidity, weather_description, latitude, longitude = get_data(country, city)
                sg.popup(f'Current Temperature: {current_temperature}\nWind Speed: {wind_speed}\nCurrent Pressure: {current_pressure}\nCurrent Humidity: {current_humidity}\nWeather Description: {weather_description}\nLatitude: {latitude}\nLongitude: {longitude}')
    else:
        sg.popup('Create a excel file with columns country, city and then import it')
        data = {'country': ['USA', 'Canada', 'France', 'Germany', 'Japan'],
            'city': ['New York', 'Toronto', 'Paris', 'Berlin', 'Tokyo']}
        df = pd.DataFrame(data)
        df.to_excel(local_path+"list.xlsx")
window.close()




