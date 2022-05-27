import PySimpleGUI as sg
from cryptograbber import *

layout = [
    [sg.Text('type search keys use commas to query multiple no spaces')],
    [sg.Input(),sg.Button('Save Keys', key='-SAVE_KEYS-')],
    [sg.Button('Run Facebook',key='-RUN_FACEBOOK-'),sg.Button('Run All',key='-RUN_ALL-')]
]

keys = []


window = sg.Window('Web Scraper',layout)

while True:
    event,values = window.read()

    if event == sg.WIN_CLOSED:
        break
   
    if event == '-SAVE_KEYS-':
        sKeys = values[0].split(',')
        keys = sKeys
    # this stereo sounds strange
    if event == '-RUN_FACEBOOK-':
        if len(keys) == 0:
            print('please input keys')
            continue
        fKeys = filter(keys)
        scrapeF(fKeys)
        print('done')

   
    if event == '-RUN_ALL-':
        if len(keys) == 0:
            print('please input keys')
            continue
        fKeys = filter(keys)
        print(len(fKeys),'matches found starting scrape')
        scrapeAll(fKeys)
        print('done')
       
window.close()
