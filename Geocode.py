import PySimpleGUI as sg
import os
import pandas as pd
from functions import create_table, collect_data, get_data, create_excel_chart


local_path = os.path.expanduser('~\\Documents\\Python_API_with_simple_gui\\')


layout = [
    [sg.Text('Select a file to import:')],
    [sg.Input(key='_FILE_'), sg.FileBrowse()],
    [sg.Button('Import'), sg.Button('find'),  sg.Button('Cancel')],
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
                    create_table(df)
                    df.to_excel(local_path + "results.xlsx")
                    sg.popup(f"Result saved in: " + local_path)
                except pd.errors.ParserError:
                    sg.popup(f'The file {filename} is wrong.')
        elif event == 'find':
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
                weather = get_data(country, city)
                sg.popup(weather.__str__())


    else:

        sg.popup('Excel Sample file')
        data = {'country': ['USA', 'Canada', 'France', 'Germany', 'Japan', 'Poland'],
            'city': ['New York', 'Toronto', 'Paris', 'Berlin', 'Tokyo', 'Warsaw']}

        df = pd.DataFrame(data)
        df.to_excel(local_path+"list.xlsx")

window.close()

create_excel_chart(local_path + "results.xlsx", "temperature in Celsius", "cities", "temperature", 'B', 'C', 'H1')
create_excel_chart(local_path + "results.xlsx", "Wind in km/h", "cities", "wind speed", 'B', 'D', 'H16')

