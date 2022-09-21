#!/usr/bin/python
import sys
import pandas as pd
import os
from datetime import datetime
from datetime import date
from subprocess import check_output

def permutation(lst):
 
    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []
 
    # If there is only one element in lst then, only one permutation is possible
    if len(lst) == 1:
        return [lst]
 
    # Find the permutations for lst if there are more than 1 characters
    l = [] # empty list that will store current permutation
 
    # Iterate the input(lst) and calculate the permutation
    for i in range(len(lst)):
       m = lst[i]
 
       # Extract lst[i] or m from the list.  remLst is remaining list
       remLst = lst[:i] + lst[i+1:]
 
       # Generating all permutations where m is first
       # element
       for p in permutation(remLst):
           l.append([m] + p)
    
    return l
 
def merukhand(basicList,patternLength):
    try:
        ##Get a flattened permutation for the list.
        merukhandList = [int(i) for i in [item for items in permutation(basicList) for item in items]]
        finalList = [] 
        if patternLength > 5:
           print('Merukhand patternLength is too long')
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
    except ValueError as e:
        print("Invalid input for Merukhand Pattern")
        
def run(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument):
    
    txtstr = ''
    if merukhandPattern == '':
        merukhandPattern = list('123')
    else:
        merukhandPattern = list(merukhandPattern)
    
    print ('Input Pitch is ', inputPitch)
    print ('Speed is ', speed)
    print ('Raaga Selected is ', inputRaag)
    print ('includeLibraryPaltas ', includeLibraryPaltas)
    print ('includeAarohAvaroh ', includeAarohAvaroh)
    print ('includeBasicPattern2 ', includeBasicPattern2)
    print ('includeBasicPattern3 ', includeBasicPattern3)
    print ('includeBasicPaltas ', includeBasicPaltas)
    print ('includeMerukhand ', includeMerukhand)
    
    divisionMap = {"quarter": "1", "eighth": "2", "16th": "4", "32nd": "8"}
    division = divisionMap[speed]

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
        
        fouttxt = open(outFileSuffix+".csv", mode='w')
        fout = open(outFileSuffix+".xml", mode='w')
    
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
        else:
           fout.write('      <midi-program>21</midi-program>\n')

        
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
            
            fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">AAROH</words></direction-type></direction>')
            fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
        
            for a in range(AarohLength):
                currPattern = a + 1
                if currPattern == AarohLength:
                    currPattern = 100
                elif currPattern > AarohLength:
                    currPattern = 100 + currPattern - AarohLength
                    
                CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                txtstr = txtstr + CurrentNote + ' '
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
        
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                fout.write('\n')
        
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""

        	
            MeasureNumber +=1
            
            fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">AVAROH</words></direction-type></direction>')
            fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
        
            for a in range(AvarohLength):
                currPattern = a + 1
                if currPattern == AvarohLength:
                    currPattern = 100
                elif currPattern > AvarohLength:
                    currPattern = 100 + currPattern - AvarohLength
                    
                CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                txtstr = txtstr + CurrentNote + ' '
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
        
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                fout.write('\n')
                
        
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""
            #BASIC AAROH AND AVAROH - END
        print(txtstr)
    ##########################################
        if includeBasicPattern2:
            #Pattern type 1-- BEGIN - Aaroh (SS,SR, SG...)
            firstNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == 1) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
            firstXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == firstNote) & (RaagaTable['Scale'] == Scale)]
            strToPrefix = (firstXML['XMLNotation']).to_string(index=False)
            
            fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">Pattern 1 - AAROH</words></direction-type></direction>')
            fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
        
            for a in range(AarohLength):
                currPattern = a + 1
                if currPattern == AarohLength:
                    currPattern = 100
                elif currPattern > AarohLength:
                    currPattern = 100 + currPattern - AarohLength
                    
                CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                txtstr = txtstr + firstNote + CurrentNote + ' '
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToPrefix.replace("eighth",speed) + strToWrite.replace("begin","end").replace("eighth",speed))
        
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                fout.write('\n')
        
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""
            #Pattern type 1-- END
        	
            MeasureNumber +=1
            #Pattern type 1-- BEGIN - Avaroh
            firstNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == 1) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
            firstXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == firstNote) & (RaagaTable['Scale'] == Scale)]
            strToPrefix = (firstXML['XMLNotation']).to_string(index=False)
            
            fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">Pattern 1 - AVAROH</words></direction-type></direction>')
            fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
        
            for a in range(AvarohLength):
                currPattern = a + 1
                if currPattern == AvarohLength:
                    currPattern = 100
                elif currPattern > AvarohLength:
                    currPattern = 100 + currPattern - AvarohLength
                    
                CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                txtstr = txtstr + firstNote + CurrentNote + ' '
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToPrefix.replace("eighth",speed) + strToWrite.replace("begin","end").replace("eighth",speed))
        
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                fout.write('\n')
        
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""
            #Pattern type 1-- END (SS,SR, SG...)
            MeasureNumber +=1
        ##########################################
        if includeBasicPattern3:
            #Pattern type 2-- BEGIN (S, SRS,SRGRS, SRGMGRS...)
            fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">Pattern 2 - AAROH</words></direction-type></direction>')
            fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
            strPrefixUp=""
            strPrefixDown=""
            noteUp = ""
            noteDown = ""
        
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

                txtstr = txtstr + noteUp + CurrentNote
                noteUp = noteUp + CurrentNote

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
        
                    noteDown = CurrentNote
                    txtstr = txtstr + noteDown

                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                txtstr = txtstr + ' '
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                fout.write('\n')
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""
        
            #Pattern type 2-- END
        
            #Pattern type 2-- BEGIN Avaroh
            fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">Pattern 2 - AVAROH</words></direction-type></direction>')
            fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
            strPrefixUp=""
            strPrefixDown=""
            noteUp = ""
            noteDown = ""
        
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

                txtstr = txtstr + noteUp + CurrentNote
                noteUp = noteUp + CurrentNote
        
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
        
                    noteDown = CurrentNote
                    txtstr = txtstr + noteDown

                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                txtstr = txtstr + ' '
                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                fout.write('\n')
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""
        
            #Pattern type 2-- END
    
        ##########################################
        ###Pattern 3: Basic Platas only till Sa
        ##########################################

        if includeBasicPaltas:
            BasicPaltaList = pd.read_csv("ListOfBasicPaltas.csv")
            for palta in BasicPaltaList['PatlaNotation']:
                Pattern=str(palta)
                patternLen = len(Pattern)

                if not True in [int(i)>AarohLength for i in Pattern]:
                    fout.write('<measure number="'+str(MeasureNumber+1)+'"><print new-system="yes"></print><direction placement="above"><direction-type><words relative-y="10.00">PATTERN:'+Pattern+' - AAROH</words></direction-type></direction>\n')
                    fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
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
                            txtstr = txtstr + CurrentNote
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
            
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
            
                            if patternCnt == 1:
                                finalStrToWrite = strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">')
                            elif patternCnt == patternLen:
                                finalStrToWrite = strToWrite.replace("begin","end").replace("eighth",speed)
                                txtstr = txtstr + ' '
                            else:
                                finalStrToWrite = strToWrite.replace("begin","continue").replace("eighth",speed)
                            
                            printList.append(finalStrToWrite)
                        
                        if printPattern:
                            for pl in printList:
                                fout.write(pl)
                                fout.write('\n')
                                fouttxt.write(txtstr)
                                txtstr = ""
            
                    fout.write('  </measure>\n')
                    fouttxt.write('\n')
                    txtstr = ""
                    
                    fout.write('<measure number="'+str(MeasureNumber+1)+'"><print new-system="yes"></print><direction placement="above"><direction-type><words relative-y="10.00">PATTERN:'+Pattern+' - AVAROH</words></direction-type></direction>\n')
                    fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
                    MeasureNumber +=1
                if not True in [int(i)>AvarohLength for i in Pattern]:
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
                            txtstr = txtstr + CurrentNote
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
            
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                            if patternCnt == 1:
                                finalStrToWrite = strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">')
                            elif patternCnt == patternLen:
                                finalStrToWrite = strToWrite.replace("begin","end").replace("eighth",speed)
                                txtstr = txtstr + ' '
                            else:
                                finalStrToWrite = strToWrite.replace("begin","continue").replace("eighth",speed)
                            
                            printList.append(finalStrToWrite)
                            
                        if printPattern:
                            MeasureNumber +=1
                            for pl in printList:
                                fout.write(pl)
                                fout.write('\n')
                                fouttxt.write(txtstr)
                                txtstr = ""
            
                    fout.write('  </measure>\n')
                    fout.write('\n')
                    fouttxt.write('\n')
                    txtstr = ""
        ###########################################

        ##########################################

        includePaltas = False
        if includeLibraryPaltas:
            includePaltas = True
            print("includeLibraryPaltasincludeLibraryPaltasincludeLibraryPaltas")
        if inputPattern != '':
            includePaltas = True
            print("inputPatterninputPatterninputPattern")
            

        if includePaltas:
            try:
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
                    fout.write('<measure number="'+str(MeasureNumber+1)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">PATTERN:'+Pattern+' - AAROH</words></direction-type></direction>')
                    fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
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
                            txtstr = txtstr + CurrentNote + ' '
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
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                            fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                            fout.write('\n')
            
                    fout.write('  </measure>\n')
                    fouttxt.write(txtstr)
                    fouttxt.write('\n')
                    txtstr = ""
                    fout.write('<measure number="'+str(MeasureNumber+1)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">PATTERN:'+Pattern+' - AVAROH</words></direction-type></direction>')
                    fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
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
                            txtstr = txtstr + CurrentNote + ' '
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
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                            fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                            fout.write('\n')
           
            
                    fout.write('  </measure>\n')
                    fouttxt.write(txtstr)
                    fouttxt.write('\n')
                    txtstr = ""
            except ValueError as e:
                print("Invalid input for Patterns.. It should be numbers on each line")
    
        ###########################################
    
        ##########################################
        ###Merukhand 
        ##########################################
        if includeMerukhand:
            fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">MERUKHAND - AAROH</words></direction-type></direction>')
            fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
            AarohList = merukhand(merukhandPattern,AarohLength)

            for currList in AarohList:
                currCount = 0
                cycleCount = 0
                for currPattern in currList:
                    currCount += 1
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                    txtstr = txtstr + CurrentNote
                    cycleCount +=1
                    if cycleCount == len(merukhandPattern):
                       txtstr = txtstr + ' '
                       cycleCount = 0
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)

                    if currCount in( 1,25,49,73,97):
                        fout.write (strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">'))
                    elif currCount == len(currList):
                        fout.write (strToWrite.replace("begin","end").replace("eighth",speed))
                    else:
                        fout.write (strToWrite.replace("begin","continue").replace("eighth",speed))
        
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                    strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                    fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                    fout.write('\n')
        
                    if currCount in( 24,48,72,96):
                        fout.write('  </measure>\n')
                        MeasureNumber +=1
                        fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n')
                        fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')

                fout.write('  </measure>\n')
                fouttxt.write(txtstr)
                fouttxt.write('\n')
                txtstr = ""
                MeasureNumber +=1
                fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n')
                fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')

            fout.write('  </measure>\n')
            MeasureNumber +=1
            fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">MERUKHAND - AVAROH</words></direction-type></direction>')
            fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
            AvarohList = merukhand(merukhandPattern,AvarohLength)
            for currList in AvarohList:
                currCount = 0;
                cycleCount = 0
                for currPattern in currList:
                    currCount += 1
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                    txtstr = txtstr + CurrentNote
                    cycleCount +=1
                    if cycleCount == len(merukhandPattern):
                       txtstr = txtstr + ' '
                       cycleCount = 0
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                    if currCount in( 1,25,49,73,97):
                        fout.write (strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">'))
                    elif currCount == len(currList):
                        fout.write (strToWrite.replace("begin","end").replace("eighth",speed))
                    else:
                        fout.write (strToWrite.replace("begin","continue").replace("eighth",speed))
        
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == 'Z')]
                    strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                    fout.write(strToWrite.replace("begin","end").replace("eighth",speed))
                    fout.write('\n')
        
                    if currCount in( 24,48,72,96):
                        fout.write('  </measure>\n')
                        MeasureNumber +=1
                        fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n')
                        fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')

                fout.write('  </measure>\n')
                fouttxt.write(txtstr)
                fouttxt.write('\n')
                txtstr = ""
                MeasureNumber +=1
                fout.write('<measure number="'+str(MeasureNumber)+'"><print new-system="yes"></print>\n')
                fout.write('\n<attributes><divisions>'+division+'</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')
            fout.write('  </measure>\n')     
        ###########################################
        fout.write('  </part>\n')
        fout.write('</score-partwise>\n')
    
        fout.close()
        fouttxt.close()
        #check_output('"msore" +outFileSuffix+'.xml" ' +'-o "output\\'+Raag+Scale+outFileSuffix+'.pdf"', shell=True)
        check_output('"mscore3" "' +outFileSuffix+'.xml" ' + '-o "' +outFileSuffix+'.mp3"', shell=True)
        #check_output('"MuseScore3.exe" "output\\'+Raag+Scale+outFileSuffix+'.xml" ' +'-o "output\\'+Raag+Scale+outFileSuffix+'.mp3"', shell=True)
        print ('Your files are generated in the output directory under this folder. Please open the PDF and the MP3 to sing along')

if __name__ == '__main__':
    main()
