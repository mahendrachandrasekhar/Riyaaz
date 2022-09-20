#!/usr/bin/python
import sys
import getopt
import pandas as pd
import os
import PySimpleGUI as sg
import warnings
import textwrap
from datetime import datetime
from datetime import date
from subprocess import check_output

def permutation(lst):
 
    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []
 
    # If there is only one element in lst then, only
    # one permutation is possible
    if len(lst) == 1:
        return [lst]
 
    # Find the permutations for lst if there are
    # more than 1 characters
 
    l = [] # empty list that will store current permutation
 
    # Iterate the input(lst) and calculate the permutation
    for i in range(len(lst)):
       m = lst[i]
 
       # Extract lst[i] or m from the list.  remLst is
       # remaining list
       remLst = lst[:i] + lst[i+1:]
 
       # Generating all permutations where m is first
       # element
       for p in permutation(remLst):
           l.append([m] + p)
    return l
 
def merukhand(basicList,patternLength):
    ##Get a flattened permutation for the list.
    merukhandList = [int(i) for i in [item for items in permutation(basicList) for item in items]]
    finalList = [] 
    for a in range(patternLength):
        currlist = []
        for b in merukhandList:
           currItem = a + b
           if currItem == patternLength:
               currItem = 100
           elif currItem > patternLength:
               currItem = 100 + currItem - patternLength
           currlist.append(currItem)
        finalList.append(currlist)
    return finalList

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
        #try:
        #    opts, args = getopt.getopt(sys.argv[1:],"hp:o:s:r:t:b:",["inputPitch=", "outFileSuffix=", "speed=","inputRaag=","inputPattern=","includeBasicPatterns="])
        #except getopt.GetoptError:
        #    print ('GeneratePalta.py -p <Pitch> -o <OutputFileSuffix> -s <Speed>')
        #    sys.exit(2)
        #for opt, arg in opts:
        #    if opt == '-h':
        #        print ('GeneratePalta.py -p Pitch -o OutputFileSuffix - s Speed')
        #        sys.exit()
        #    elif opt in ("-p", "--inputPitch"):
        #        inputPitch = arg
        #    elif opt in ("-o", "--outFileSuffix"):
        #        outFileSuffix = arg
        #    elif opt in ("-s", "--speed"):
        #        speed = arg
        #    elif opt in ("-r", "--inputRaag"):
        #        inputRaag = arg
        #    elif opt in ("-t", "--inputPattern"):
        #        inputPattern = arg
        #    elif opt in ("-b", "--includeBasicPatterns"):
        #        includeBasicPatterns = arg
        
        print ('Input Pitch is ', inputPitch)
        print ('File Suffix is ', outFileSuffix)
        print ('Raaga Selected is ', inputRaag)
        print ('Generating your paltas. Please wait...')
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
        #print(os.path.dirname(os.path.realpath(__file__)))
        
        #TO DO... Change to current directory.
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        
        #Get the Raaga table
        RaagaTable = pd.read_csv("RaagasNotationsAndMusicXMLNotations.csv")
        
        #Get the basic Aaroh Avaroh 
        AarohAvarohBasic = pd.read_csv("Aaroh-Avaroh-Basic.csv")
        AarohAvarohBasic.drop('Notation',axis=1,inplace=True)
        
        #Get the Aaroh Avaroh including the next Octave.
        AarohAvarohExtended = pd.read_csv("Aaroh-Avaroh-Extension.csv")
        #The File template used will generate blank rows, so remove it out
        AarohAvarohExtended.drop(AarohAvarohExtended.index[(AarohAvarohExtended["Raag"].isnull())],axis=0,inplace=True)
        
        AarohAvaroh = pd.concat([AarohAvarohBasic, AarohAvarohExtended])
        
        if inputRaag == '':
            RaagList = pd.read_csv("RaagaList.csv")
        else:
            d = {'RaagaName': [inputRaag]}
            RaagList = pd.DataFrame(data=d)
        
        
        ##############
        Scale=inputPitch
        ##############
        
        for Raag in RaagList['RaagaName']:
            
            fout = open("output\\"+Raag+Scale+outFileSuffix+".xml", mode='w')
        
            fout.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            fout.write('<!-- MusicXML symbolic note types range from 1024th notes to maxima notes: 1024th, 512th, 256th, 128th, 64th, 32nd, 16th, eighth, quarter, half, whole, breve, long, and maxima.-->\n')
            fout.write('<score-partwise version="3.1">\n')
            fout.write('  <defaults>\n')
            fout.write('    <scaling>\n')
            fout.write('      <millimeters>7</millimeters>\n')
            fout.write('      <tenths>40</tenths>\n')
            fout.write('      </scaling>\n')
            fout.write('    <page-layout>\n')
            fout.write('      <page-height>2400.69</page-height>\n')
            fout.write('      <page-width>2016.74</page-width>\n')
            fout.write('      <page-margins type="even">\n')
            fout.write('        <left-margin>85.7143</left-margin>\n')
            fout.write('        <right-margin>85.7143</right-margin>\n')
            fout.write('        <top-margin>85.7143</top-margin>\n')
            fout.write('        <bottom-margin>85.7143</bottom-margin>\n')
            fout.write('        </page-margins>\n')
            fout.write('      <page-margins type="odd">\n')
            fout.write('        <left-margin>30.7143</left-margin>\n')
            fout.write('        <right-margin>30.7143</right-margin>\n')
            fout.write('        <top-margin>85.7143</top-margin>\n')
            fout.write('        <bottom-margin>85.7143</bottom-margin>\n')
            fout.write('        </page-margins>\n')
            fout.write('      </page-layout>\n')
            fout.write('    <word-font font-family="Edwin" font-size="10"/>\n')
            fout.write('    <lyric-font font-family="Edwin" font-size="10"/>\n')
            fout.write('    </defaults>\n')
        
            fout.write('  <credit page="1">\n')
            fout.write('    <credit-type>title</credit-type>')
            fout.write('    <credit-words justify="center" valign="top" font-size="22">Raag '+ Raag +' - Sujaan Music.\nNotations:Sa->S, Komal Re->r, Shudda Re->R, Komal Ga->g, Shudda Ga ->G,Shudda Ma ->m,\nTeevra Ma->M,Pa->P, Komal Dha->d, Shudda Dha->D, Komal Ni->n,Shudda Ni->N</credit-words>\n')
            fout.write('    </credit>\n')
            fout.write('  <part-list>')
            fout.write('    <score-part id="P1">\n')
            fout.write('      <part-name>Raag ' + Raag + '</part-name>\n')
            fout.write('      <score-instrument id="P1-I1">\n')
            fout.write('      <instrument-name></instrument-name>\n')
            fout.write('      </score-instrument>\n')
            fout.write('      <midi-device id="P1-I1" port="1"></midi-device>\n')
            fout.write('      <midi-instrument id="P1-I1">\n')
            fout.write('      <midi-channel>1</midi-channel>\n')
            
            if instrument == 'Reed Organ':
               fout.write('      <midi-program>21</midi-program>\n')
            elif instrument == 'Piano':
               fout.write('      <midi-program>1</midi-program>\n')
            
            fout.write('      <pan>0</pan>\n')
            fout.write('      </midi-instrument>\n')
            fout.write('    </score-part>\n')
            fout.write('  </part-list>\n')
            fout.write('  <part id="P1">\n')
        
        
            ##Logic
            ##Get all the notes for the Raag in a table
            CurrentRaag = AarohAvaroh.loc[AarohAvaroh['Raag'] == Raag]
            AarohLength = len((CurrentRaag.loc[(CurrentRaag['Sequence'] <= 100) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")]))
            AvarohLength = len((CurrentRaag.loc[(CurrentRaag['Sequence'] <= 100) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")]))
            MeasureNumber=0
        ##########################################
        
            if includeAarohAvaroh:
                ##BASIC AAROH AND AVAROH
                
                fout.write('<measure number="'+str(MeasureNumber)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">AAROH</words></direction-type></direction>')
            
                for a in range(AarohLength):
                    currPattern = a + 1
                    if currPattern == AarohLength:
                        currPattern = 100
                    elif currPattern > AarohLength:
                        currPattern = 100 + currPattern - AarohLength
                        
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                    fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
            
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                    fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                    fout.write('\n')
            
                fout.write('  </measure>\n')
            	
                MeasureNumber +=1
                
                fout.write('<measure number="'+str(MeasureNumber)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">AVAROH</words></direction-type></direction>')
            
                for a in range(AvarohLength):
                    currPattern = a + 1
                    if currPattern == AvarohLength:
                        currPattern = 100
                    elif currPattern > AvarohLength:
                        currPattern = 100 + currPattern - AvarohLength
                        
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                    fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
            
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                    fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                    fout.write('\n')
            
                fout.write('  </measure>\n')
                #BASIC AAROH AND AVAROH - END
        
        ##########################################
            if includeBasicPattern2:
                #Pattern type 1-- BEGIN - Aaroh (SS,SR, SG...)
                firstNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == 1) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                firstXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == firstNote) & (RaagaTable['Scale'] == Scale)]
                strToPrefix = (firstXML['XMLNotation']).to_string(index=False)
                
                fout.write('<measure number="'+str(MeasureNumber)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">Pattern 1 - AAROH</words></direction-type></direction>')
            
                for a in range(AarohLength):
                    currPattern = a + 1
                    if currPattern == AarohLength:
                        currPattern = 100
                    elif currPattern > AarohLength:
                        currPattern = 100 + currPattern - AarohLength
                        
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                    fout.write(strToPrefix.replace("eighth",speed) + strToWrite.replace("begin","end").replace("eighth",speed))
            
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                    fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                    fout.write('\n')
            
                fout.write('  </measure>\n')
                #Pattern type 1-- END
            	
                MeasureNumber +=1
                #Pattern type 1-- BEGIN - Avaroh
                firstNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == 1) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                firstXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == firstNote) & (RaagaTable['Scale'] == Scale)]
                strToPrefix = (firstXML['XMLNotation']).to_string(index=False)
                
                fout.write('<measure number="'+str(MeasureNumber)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">Pattern 1 - AVAROH</words></direction-type></direction>')
            
                for a in range(AvarohLength):
                    currPattern = a + 1
                    if currPattern == AvarohLength:
                        currPattern = 100
                    elif currPattern > AvarohLength:
                        currPattern = 100 + currPattern - AvarohLength
                        
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                    fout.write(strToPrefix.replace("eighth",speed) + strToWrite.replace("begin","end").replace("eighth",speed))
            
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                    fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                    fout.write('\n')
            
                fout.write('  </measure>\n')
                #Pattern type 1-- END (SS,SR, SG...)
                MeasureNumber +=1
            ##########################################
            if includeBasicPattern3:
                #Pattern type 2-- BEGIN (S, SRS,SRGRS, SRGMGRS...)
                fout.write('<measure number="'+str(MeasureNumber)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">Pattern 2 - AAROH</words></direction-type></direction>')
                strPrefixUp=""
                strPrefixDown=""
            
                for a in range(1,AarohLength,1):
                    #print(strToPrefix)
                    currPattern = a
                    #print("Looping Up"+str(currPattern))
            
                    if currPattern == AarohLength:
                        currPattern = 100
                    elif currPattern > AarohLength:
                        currPattern = 100 + currPattern - AarohLength
                        
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strCurr = (CurrentXML['XMLNotation']).to_string(index=False)
                    strToWriteUp = strPrefixUp.replace("eighth",speed) + strCurr.replace("begin","end").replace("eighth",speed)
                    strPrefixUp = strToWriteUp
                    fout.write(strToWriteUp)
            
                    for b in range(a-1,0,-1):
                        
                        currPattern = b
                        #print("Looping Down"+str(currPattern))
                        if currPattern == AarohLength:
                            currPattern = 100
                        elif currPattern > AarohLength:
                            currPattern = 100 + currPattern - AarohLength
                        CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                        CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                        strCurr = (CurrentXML['XMLNotation']).to_string(index=False)
                        strToWriteDown = strCurr.replace("begin","end").replace("eighth",speed)
                        fout.write(strToWriteDown)
            
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                    fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                    fout.write('\n')
                fout.write('  </measure>\n')
            
                #Pattern type 2-- END
            
                #Pattern type 2-- BEGIN Avaroh
                fout.write('<measure number="'+str(MeasureNumber)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">Pattern 1 - AVAROH</words></direction-type></direction>')
                strPrefixUp=""
                strPrefixDown=""
            
                for a in range(1,AvarohLength,1):
                    #print(strToPrefix)
                    currPattern = a
                    #print("Looping Up"+str(currPattern))
            
                    if currPattern == AvarohLength:
                        currPattern = 100
                    elif currPattern > AvarohLength:
                        currPattern = 100 + currPattern - AvarohLength
                        
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strCurr = (CurrentXML['XMLNotation']).to_string(index=False)
                    strToWriteUp = strPrefixUp.replace("eighth",speed) + strCurr.replace("begin","end").replace("eighth",speed)
                    strPrefixUp = strToWriteUp
                    fout.write(strToWriteUp)
            
                    for b in range(a-1,0,-1):
                        
                        currPattern = b
                        #print("Looping Down"+str(currPattern))
                        if currPattern == AvarohLength:
                            currPattern = 100
                        elif currPattern > AvarohLength:
                            currPattern = 100 + currPattern - AvarohLength
                        CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                        CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                        strCurr = (CurrentXML['XMLNotation']).to_string(index=False)
                        strToWriteDown = strCurr.replace("begin","end").replace("eighth",speed)
                        fout.write(strToWriteDown)
            
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                    fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                    fout.write('\n')
                fout.write('  </measure>\n')
            
                #Pattern type 2-- END
        
            ##########################################
            ###Pattern 3: Basic Platas only till Sa
            ##########################################

            if includeBasicPaltas:
                BasicPaltaList = pd.read_csv("ListOfBasicPaltas.csv")
                for palta in BasicPaltaList['PatlaNotation']:
                    Pattern=str(palta)
                    patternLen = len(Pattern)
                    fout.write('<measure number="'+str(MeasureNumber+1)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">PATTERN:'+Pattern+' - AAROH</words></direction-type></direction>')
                    MeasureNumber +=1
                    
                    for a in range(AarohLength):
            
                        #Loop through pattern for Aaroh
                        patternCnt = 0
                        printPattern = True
                        printList = []
                        
                        for p in Pattern:
                            currPattern = int(p) + a
                            patternCnt +=1
                            
                            if currPattern == AarohLength:
                                currPattern = 100
                            elif currPattern > AarohLength:
                                currPattern = 100 + currPattern - AarohLength
                                printPattern = False
                            
                            CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
            
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
            
                            if patternCnt == 1:
                                finalStrToWrite = strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">')
                            elif patternCnt == patternLen:
                                finalStrToWrite = strToWrite.replace("begin","end").replace("eighth",speed)
                            else:
                                finalStrToWrite = strToWrite.replace("begin","continue").replace("eighth",speed)
                            
                            printList.append(finalStrToWrite)
                        
                        if printPattern:
                            for pl in printList:
                                fout.write(pl)
                                fout.write('\n')
            
                        # Find how many notes are missing for the 8 Beat and add Z note
                        #MissingNotes = 4 - len(Pattern)%4
                        #if MissingNotes == 4:
                        #    MissingNotes = 0
            
                        # Loop Through missing notes and add the unpitched note
                        #for m in range(MissingNotes):
                        #    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                        #    fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                        #    fout.write('\n')
            
                    fout.write('  </measure>\n')
                    fout.write('<measure number="'+str(MeasureNumber+1)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">PATTERN:'+Pattern+' - AVAROH</words></direction-type></direction>')
                    MeasureNumber +=1
                    for a in range(AvarohLength):
            
                        #Loop through pattern for Aaroh
                        patternCnt = 0
                        printPattern = True
                        printList = []
                        
                        for p in Pattern:
                            currPattern = int(p) + a
                            patternCnt +=1
            
                            if currPattern == AvarohLength:
                                currPattern = 100
                            elif currPattern > AvarohLength:
                                currPattern = 100 + currPattern - AvarohLength
                                printPattern = False    
                                
                            #Search Sequence in CurrentRaag and get the LyricalNote
                            CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
            
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                            if patternCnt == 1:
                                finalStrToWrite = strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">')
                            elif patternCnt == patternLen:
                                finalStrToWrite = strToWrite.replace("begin","end").replace("eighth",speed)
                            else:
                                finalStrToWrite = strToWrite.replace("begin","continue").replace("eighth",speed)
                            
                            printList.append(finalStrToWrite)
                            
                        if printPattern:
                            for pl in printList:
                                fout.write(pl)
                                fout.write('\n')

                        # Find how many notes are missing for the 8 Beat and add Z note
                        MissingNotes = 4 - len(Pattern)%4
                        if MissingNotes == 4:
                            MissingNotes = 0
            
                        # Loop Through missing notes and add the unpitched note
                        for m in range(MissingNotes):
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                            fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                            fout.write('\n')
            
            
                    fout.write('  </measure>\n')
            ###########################################

            ##########################################

            includePaltas = False
            if includeLibraryPaltas:
                includePaltas = True
            if inputPattern != '':
                includePaltas = True

            if includePaltas:
                if includeLibraryPaltas:
                    PaltaList1 = pd.read_csv("ListOfPaltas.csv")
                if inputPattern != '':
                    newPattern = []
                    for p in (inputPattern.split('\n')):
                        newPattern.append(int(p))
                    d = {'PatlaNotation': newPattern}
                    PaltaList2 = pd.DataFrame(data=d)
                
                if includeLibraryPaltas and inputPattern != '':
                    PaltaList = PaltaList1.append(PaltaList2)
                elif includeLibraryPaltas:
                    PaltaList = PaltaList1
                elif inputPattern != '':
                    PaltaList = PaltaList2
                    
                
                print(PaltaList)    

                for palta in PaltaList['PatlaNotation']:
                    Pattern=str(palta)
                    fout.write('<measure number="'+str(MeasureNumber+1)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">PATTERN:'+Pattern+' - AAROH</words></direction-type></direction>')
                    MeasureNumber +=1
                    
                    for a in range(AarohLength):
            
                        #Loop through pattern for Aaroh
                        patternCnt = 0
                        patternLen = len(Pattern)
            
                        for p in Pattern:
                            currPattern = int(p) + a
                            patternCnt +=1
                            
                            if currPattern == AarohLength:
                                currPattern = 100
                            elif currPattern > AarohLength:
                                currPattern = 100 + currPattern - AarohLength
                            #print(currPattern)    
                            #Search Sequence in CurrentRaag and get the LyricalNote
                            CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
            
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
            
                            if patternCnt == 1:
                                fout.write (strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">'))
                            elif patternCnt == patternLen:
                                fout.write (strToWrite.replace("begin","end").replace("eighth",speed))
                            else:
                                fout.write (strToWrite.replace("begin","continue").replace("eighth",speed))
                            fout.write('\n')
            
                        # Find how many notes are missing for the 8 Beat and add Z note
                        MissingNotes = 4 - len(Pattern)%4
                        if MissingNotes == 4:
                            MissingNotes = 0
            
                        # Loop Through missing notes and add the unpitched note
                        for m in range(MissingNotes):
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                            fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                            fout.write('\n')
            
                    fout.write('  </measure>\n')
                    fout.write('<measure number="'+str(MeasureNumber+1)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">PATTERN:'+Pattern+' - AVAROH</words></direction-type></direction>')
                    MeasureNumber +=1
                    for a in range(AvarohLength):
            
                        #Loop through pattern for Aaroh
                        patternCnt = 0
                        patternLen = len(Pattern)
                        
                        for p in Pattern:
                            currPattern = int(p) + a
                            patternCnt +=1
            
                            if currPattern == AvarohLength:
                                currPattern = 100
                            elif currPattern > AvarohLength:
                                currPattern = 100 + currPattern - AvarohLength
                            #print(currPattern)    
                            #Search Sequence in CurrentRaag and get the LyricalNote
                            CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
            
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                            if patternCnt == 1:
                                fout.write (strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">'))
                            elif patternCnt == patternLen:
                                fout.write (strToWrite.replace("begin","end").replace("eighth",speed))
                            else:
                                fout.write (strToWrite.replace("begin","continue").replace("eighth",speed))
                            
                            
                            fout.write('\n')
            
                        # Find how many notes are missing for the 8 Beat and add Z note
                        MissingNotes = 4 - len(Pattern)%4
                        if MissingNotes == 4:
                            MissingNotes = 0
            
                        # Loop Through missing notes and add the unpitched note
                        for m in range(MissingNotes):
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                            fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                            fout.write('\n')
            
            
                    fout.write('  </measure>\n')
            ###########################################
        
            ##########################################
            ###Merukhand 
            ##########################################
            if includeMerukhand:
                fout.write('<measure number="'+str(MeasureNumber)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">MERUKHAND - AAROH</words></direction-type></direction>')
                AarohList = merukhand(merukhandPattern,AarohLength)

                for currList in AarohList:
                    currCount = 0;
                    for currPattern in currList:
                        currCount += 1
                        CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                        CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                        strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)

                        if currCount in( 1,25,49,73,97):
                            fout.write (strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">'))
                        elif currCount == len(currList):
                            fout.write (strToWrite.replace("begin","end").replace("eighth",speed))
                        else:
                            fout.write (strToWrite.replace("begin","continue").replace("eighth",speed))
            
                        CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                        fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                        fout.write('\n')
            
                        if currCount in( 24,48,72,96):
                            fout.write('  </measure>\n')
                            MeasureNumber +=1
                            fout.write('<measure number="'+str(MeasureNumber)+'">\n')

                    fout.write('  </measure>\n')
                    MeasureNumber +=1
                    fout.write('<measure number="'+str(MeasureNumber)+'">\n')

                fout.write('  </measure>\n')
                MeasureNumber +=1
                fout.write('<measure number="'+str(MeasureNumber)+'">\n<direction placement="above"><direction-type><words relative-y="10.00">MERUKHAND - AVAROH</words></direction-type></direction>')
                AvarohList = merukhand(merukhandPattern,AvarohLength)
                for currList in AvarohList:
                    currCount = 0;
                    for currPattern in currList:
                        currCount += 1
                        CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                        CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                        strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                        if currCount in( 1,25,49,73,97):
                            fout.write (strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">'))
                        elif currCount == len(currList):
                            fout.write (strToWrite.replace("begin","end").replace("eighth",speed))
                        else:
                            fout.write (strToWrite.replace("begin","continue").replace("eighth",speed))
            
                        CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                        fout.write ((CurrentXML['XMLNotation']).to_string(index=False))
                        fout.write('\n')
            
                        if currCount in( 24,48,72,96):
                            fout.write('  </measure>\n')
                            MeasureNumber +=1
                            fout.write('<measure number="'+str(MeasureNumber)+'">\n')

                    fout.write('  </measure>\n')
                    MeasureNumber +=1
                    fout.write('<measure number="'+str(MeasureNumber)+'">\n')
                fout.write('  </measure>\n')     
            ###########################################
            fout.write('  </part>\n')
            fout.write('</score-partwise>\n')
        
            fout.close()
            check_output('"MuseScore3.exe" "output\\'+Raag+Scale+outFileSuffix+'.xml" ' +'-o "output\\'+Raag+Scale+outFileSuffix+'.pdf"', shell=True)
            check_output('"MuseScore3.exe" "output\\'+Raag+Scale+outFileSuffix+'.xml" ' +'-o "output\\'+Raag+Scale+outFileSuffix+'.mp3"', shell=True)
            print ('Your files are generated in the output directory under this folder. Please open the PDF and the MP3 to sing along')
    
    window.close()
    exit(0)

if __name__ == '__main__':
    main()