#!/usr/bin/python
import PySimpleGUI as sg
import warnings
import textwrap
import os
import mainRiyaaz

def main():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    patternText = 'Enter the palta patterns you want to generate (E.g. 1221)\nEnter each pattern in a new line'

    inputPitch = ''
    inputPattern = ''
    inputRaag = ''
    
    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Image('Sujaan.png', size=(616, 100))],
                [sg.Text('Select the Pitch',size=(50, None),font=("Bookman Old Style", 10)), sg.Combo(['A','A#','B','C','C#','D','D#','E','F','F#','G','G#'],default_value='C#',key='inputPitch')],
                [sg.Text('Enter the File Suffix you want',size=(50, None),font=("Bookman Old Style", 10)), sg.InputText(size=20,key='outFileSuffix')],
                [sg.Text('Select the speed',size=(50, None),font=("Bookman Old Style", 10)), sg.Combo(['1024th','512th','256th','128th','64th','32nd','16th','eighth','quarter','half','whole','breve','long','maxima'],default_value='quarter',key='speed')],
                [sg.Text('Select the Raaga',size=(50, None),font=("Bookman Old Style", 10)), sg.Combo(['AhirBhairav','Bhairav','Bhairavi','Bhimpalasi','Bhoopali','Bhupeshwari','Bihag','Bilawal','Charukeshi','Keerwani','Khamaj','Malkauns','Rageshree','Shivranjini','Todi','Vibhas','Yaman'],default_value='Bilawal',key='inputRaag')],
                
                [sg.Frame(layout=[
                [sg.Checkbox('Aaroh/Avaroh', font=("Bookman Old Style", 10), size=(30,1),key='includeAarohAvaroh',default=False),
                 sg.Checkbox('1st Note Fixed E.g. SS, SR, SG, ...', font=("Bookman Old Style", 10), size=(30,1),key='includeBasicPattern2',default=False)],
                [sg.Checkbox('Increasing Note E.g. S, SRS, SRGRS...', font=("Bookman Old Style", 10), size=(30,1),key='includeBasicPattern3',default=False),
                 sg.Checkbox('Some Built-in Notations', font=("Bookman Old Style", 10), size=(30,1),key='includeBasicPaltas',default=False)],
                ],title='Basic Patterns',font=("Bookman Old Style", 12,'bold'))],
               
                [sg.Frame(layout=[
                [sg.Checkbox('Include Palta Patterns from our in-built library.', font=("Bookman Old Style", 10,'bold'), size=(70,1),key='includeLibraryPaltas',default=False)],
                [sg.Text(patternText,size=(50, None),font=("Bookman Old Style", 10)), sg.Multiline(size=(20,5),key='inputPattern')],
                ],title='Generate your own Palta Patterns',font=("Bookman Old Style", 12,'bold'))],
                
                [sg.Frame(layout=[
                [sg.Checkbox('Merukhand', font=("Bookman Old Style", 10), size=(20,1),key='includeMerukhand',default=False),
                 sg.Text('Merukhand Pattern(Blank for default pattern)',size=(30, None),font=("Bookman Old Style", 10)), sg.InputText(size=20,key='merukhandPattern')],
                ],title='Advanced Patterns',font=("Bookman Old Style", 12,'bold'))],

                [sg.Text('Choose The Intrument',size=(50, None),font=("Bookman Old Style", 10)), sg.Combo(['Reed Organ','Piano'],default_value='Reed Organ',key='instrument')],
                [sg.Button('Ok'), sg.Button('Cancel')], 
                [sg.Text('Your pdf and mp3 files will be generated under\n '+os.getcwd()+'\output',font=("Bookman Old Style", 14))] ]
    
    # Create the Window
    window = sg.Window('Sujaan Riyaaz', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            exit(0)
        
        ##Read the inputs
        inputPitch              = values['inputPitch']
        outFileSuffix           = values['outFileSuffix']
        speed                   = values['speed']
        inputRaag               = values['inputRaag']
        includeLibraryPaltas    = values['includeLibraryPaltas']
        inputPattern            = values['inputPattern']
        includeAarohAvaroh      = values['includeAarohAvaroh']
        includeBasicPattern2    = values['includeBasicPattern2']
        includeBasicPattern3    = values['includeBasicPattern3']
        includeBasicPaltas      = values['includeBasicPaltas']
        includeMerukhand        = values['includeMerukhand']
        if values['merukhandPattern'] == '':
           merukhandPattern = list('123')
        else:
           merukhandPattern        = list(values['merukhandPattern'])
        instrument              = values['instrument']
        
        print('inputPitch           = ' + inputPitch          )
        print('outFileSuffix        = ' + outFileSuffix       )
        print('speed                = ' + speed               )
        print('inputRaag            = ' + inputRaag           )
        print('includeLibraryPaltas = ' + str(includeLibraryPaltas))
        print('inputPattern         = ' + inputPattern        )
        print('includeAarohAvaroh   = ' + str(includeAarohAvaroh  ))
        print('includeBasicPattern2 = ' + str(includeBasicPattern2))
        print('includeBasicPattern3 = ' + str(includeBasicPattern3))
        print('includeMerukhand     = ' + str(includeMerukhand    ))
        print('merukhandPattern     = ' + values['merukhandPattern'])
        print('instrument           = ' + instrument          )
        
        mainRiyaaz.run(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument)
        
        sg.Popup('Success','Your files are generated in the output directory.Please open the PDF and the MP3 to sing along')
    window.close()
    exit(0)

if __name__ == '__main__':
    main()

