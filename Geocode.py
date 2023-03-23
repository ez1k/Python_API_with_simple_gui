import PySimpleGUI as sg
import os
import pandas as pd
from functions import collect_data, get_data, create_chart, create_Excel


local_path = os.path.expanduser('~\\Documents\\Python_API_with_simple_gui\\')
if not os.path.exists(local_path):
    local_path = os.path.expanduser('~\\Documents\\github\\Python_API_with_simple_gui\\')

layout = [
    [sg.Text('Select a file to import:')],
    [sg.Input(key='_FILE_'), sg.FileBrowse()],
    [sg.Button('Import'), sg.Button('Add to file'),  sg.Button('Cancel')],
]

window = sg.Window('Weather API', layout)

data = {'country': [],
        'city': [],
        'Temperature':[],
        'Wind Speed':[],
        'Pressure':[],
        'Humidity': [],
        'Description': []
        }
df = pd.DataFrame(data)

while True:
    if os.path.exists(local_path+"list.csv"):
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'Import':
            filename = values['_FILE_']
            if filename == "":
                sg.popup(f'The file {filename} is empty.')
            else:
                try:
                    df = pd.read_csv(filename, delimiter=';')
                    df = df.append(collect_data(df), ignore_index=True)
                except pd.errors.ParserError:
                    sg.popup(f'The file {filename} is wrong.')
        elif event == 'Add to file':
            layout = [
                [sg.Text('Enter Country:'), sg.InputText(key='_COUNTRY_')],
                [sg.Text('Enter City:'), sg.InputText(key='_CITY_')],
                [sg.Button('Submit')]
            ]
            window_test = sg.Window('Single Test', layout)
            while True:
                event_test, values_test = window_test.read()
                if event_test == sg.WIN_CLOSED or event_test == 'Cancel':
                    break
                elif event_test == 'Submit':
                    country = values_test['_COUNTRY_']
                    city = values_test['_CITY_']
                    weather = get_data(country, city)
                    single = {'country': country, 'city': city, 'Temperature': weather.temperature , 
                              'Wind Speed': weather.wind_speed, 'Pressure': weather.pressure, 'Humidity': weather.humidity, 'Description': weather.description} 
                    if weather.description != 'no data':
                        df = df.append(single, ignore_index=True)
                    
            window_test.close()

    else:
        sg.popup('Excel Sample file')


sg.popup(f"Result saved in: " + local_path)
window.close()

create_Excel(df,local_path)
create_chart(local_path + "results.xlsx", "temperature in Celsius", "cities", "temperature", 'B', 'C', 'H1')
create_chart(local_path + "results.xlsx", "Wind in km/h", "cities", "wind speed", 'B', 'D', 'H16')

