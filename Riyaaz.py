#!/usr/bin/python
import sys
import pandas as pd
import os
from datetime import datetime
from datetime import date
from subprocess import check_output
import helperFunctions
import fileOperations

def cleanupFile(filename):
   check_output('rm ' +filename+'.* ', shell=True)

def getRaagList(myRaag):
    if myRaag == '':
        myRaagList = pd.read_csv("RaagaList.csv")
    else:
        d = {'RaagaName': [myRaag]}
        myRaagList = pd.DataFrame(data=d)
    return myRaagList

def getAarohAvaroh(basicFileName, extensionFileName):
    #Get the basic Aaroh Avaroh 
    AarohAvarohBasic = pd.read_csv(basicFileName)
    AarohAvarohBasic.drop('Notation',axis=1,inplace=True)
    
    #Get the Aaroh Avaroh including the next Octave.
    AarohAvarohExtended = pd.read_csv(extensionFileName)
    #The File template used will generate blank rows, so remove it out
    AarohAvarohExtended.drop(AarohAvarohExtended.index[(AarohAvarohExtended["Raag"].isnull())],axis=0,inplace=True)
    print(len(AarohAvarohExtended))
    return pd.concat([AarohAvarohBasic, AarohAvarohExtended])

def getCurrentPattern(n,len):
   if n == len:
       return 100
   elif n > len:
       return 100 + n - len
   else:
       return n

def run(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument):
    
    txtstr = ''

    ### Set the pandas options so that they print poperly in the XML file
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    
    if merukhandPattern == '':
        merukhandPattern = list('123')
    else:
        merukhandPattern = list(merukhandPattern)
    
    helperFunctions.printSelection(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument)
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    #Get the Raaga table
    RaagaTable = pd.read_csv("RaagasNotationsAndMusicXMLNotations.csv")
    AarohAvaroh = getAarohAvaroh("Aaroh-Avaroh-Basic.csv","Aaroh-Avaroh-Extension.csv")
    RaagList = getRaagList(inputRaag)
    
    ##############
    Scale=inputPitch
    ##############
    
    for Raag in RaagList['RaagaName']:
        ##Initialize
        fouttxt = open(outFileSuffix+".csv", mode='w')
        fout = open(outFileSuffix+".xml", mode='w')
        fileOperations.initializeFile(fout,Raag,instrument)
        ##Logic
        ##Get all the notes for the Raag in a table
        CurrentRaag = AarohAvaroh.loc[AarohAvaroh['Raag'] == Raag]
        AarohLength = len((CurrentRaag.loc[(CurrentRaag['Sequence'] <= 100) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")]))
        AvarohLength = len((CurrentRaag.loc[(CurrentRaag['Sequence'] <= 100) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")]))
        MeasureNumber=0
        
        ##########################################
    
        if includeAarohAvaroh:
            ##BASIC AAROH AND AVAROH
            firstNote = ""
            firstXML = ""
            strToPrefix = ""
            
            fileOperations.startMeasure(fout,"AAROH",MeasureNumber,speed)

            for a in range(AarohLength):
                currPattern = getCurrentPattern(a + 1,AarohLength)
                fileOperations.findAndWriteCurrentNoteWithPrefix(CurrentRaag,currPattern,"Aaroh",strToPrefix,RaagaTable)
                fileOperations.writeEmptyNote(fout, RaagaTable, speed)
                txtstr = txtstr + firstNote + CurrentNote + ' '
        
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""

            MeasureNumber +=1
            fileOperations.startMeasure(fout,"AVAROH",MeasureNumber,speed)
        
            for a in range(AvarohLength):
                currPattern = getCurrentPattern(a + 1,AvarohLength)
                fileOperations.findAndWriteCurrentNoteWithPrefix(CurrentRaag,currPattern,"Avaroh",strToPrefix,RaagaTable)    
                fileOperations.writeEmptyNote(fout, RaagaTable, speed)
                txtstr = txtstr + firstNote + CurrentNote + ' '
        
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""
            #BASIC AAROH AND AVAROH - END
        
        ##########################################
        ##########################################
        if includeBasicPattern2:
            #Pattern type 1-- BEGIN - Aaroh (SS,SR, SG...)
            firstNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == 1) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
            firstXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == firstNote) & (RaagaTable['Scale'] == Scale)]
            strToPrefix = (firstXML['XMLNotation']).to_string(index=False)
            
            fileOperations.startMeasure(fout,"Pattern 1 - AAROH",MeasureNumber,speed)
        
            for a in range(AarohLength):
                currPattern = getCurrentPattern(a + 1,AarohLength)
                fileOperations.findAndWriteCurrentNoteWithPrefix(CurrentRaag,currPattern,"Aaroh",strToPrefix,RaagaTable)    
                fileOperations.writeEmptyNote(fout, RaagaTable, speed)
                txtstr = txtstr + firstNote + CurrentNote + ' '
        
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
            
            fileOperations.startMeasure(fout,"Pattern 1 - AVAROH",MeasureNumber,speed)
        
            for a in range(AvarohLength):
                currPattern = getCurrentPattern(a + 1,AvarohLength)
                fileOperations.findAndWriteCurrentNoteWithPrefix(CurrentRaag,currPattern,"Avaroh",strToPrefix,RaagaTable)    
                fileOperations.writeEmptyNote(fout, RaagaTable, speed)
                txtstr = txtstr + firstNote + CurrentNote + ' '
        
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""
            #Pattern type 1-- END (SS,SR, SG...)
            MeasureNumber +=1
        ##########################################
        ##########################################
        if includeBasicPattern3:
            #Pattern type 2-- BEGIN (S, SRS,SRGRS, SRGMGRS...)
            fileOperations.startMeasure(fout,"Pattern 2 - AAROH",MeasureNumber,speed)

            strPrefixUp=""
            strPrefixDown=""
            noteUp = ""
            noteDown = ""
        
            for a in range(1,AarohLength,1):
                currPattern = getCurrentPattern(a,AarohLength)
                    
                CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                strCurr = (CurrentXML['XMLNotation']).to_string(index=False)
                strToWriteUp = strPrefixUp.replace("eighth",speed) + strCurr.replace("begin","end").replace("eighth",speed)
                strPrefixUp = strToWriteUp
                fout.write(strToWriteUp)

                txtstr = txtstr + noteUp + CurrentNote
                noteUp = noteUp + CurrentNote

                for b in range(a-1,0,-1):
                    
                    currPattern = getCurrentPattern(b,AarohLength)
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strCurr = (CurrentXML['XMLNotation']).to_string(index=False)
                    strToWriteDown = strCurr.replace("begin","end").replace("eighth",speed)
                    fout.write(strToWriteDown)
        
                    noteDown = CurrentNote
                    txtstr = txtstr + noteDown

                txtstr = txtstr + ' '
                fileOperations.writeEmptyNote(fout, RaagaTable, speed)
                
            fout.write('  </measure>\n')
            fouttxt.write(txtstr)
            fouttxt.write('\n')
            txtstr = ""
        
            #Pattern type 2-- END
        
            #Pattern type 2-- BEGIN Avaroh
            fileOperations.startMeasure(fout,"Pattern 2 - AVAROH",MeasureNumber,speed)

            strPrefixUp=""
            strPrefixDown=""
            noteUp = ""
            noteDown = ""
        
            for a in range(1,AvarohLength,1):
                currPattern = getCurrentPattern(a,AvarohLength)
                    
                CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                strCurr = (CurrentXML['XMLNotation']).to_string(index=False)
                strToWriteUp = strPrefixUp.replace("eighth",speed) + strCurr.replace("begin","end").replace("eighth",speed)
                strPrefixUp = strToWriteUp
                fout.write(strToWriteUp)

                txtstr = txtstr + noteUp + CurrentNote
                noteUp = noteUp + CurrentNote
        
                for b in range(a-1,0,-1):
                    
                    currPattern = getCurrentPattern(b,AvarohLength)
                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
                    strCurr = (CurrentXML['XMLNotation']).to_string(index=False)
                    strToWriteDown = strCurr.replace("begin","end").replace("eighth",speed)
                    fout.write(strToWriteDown)
        
                    noteDown = CurrentNote
                    txtstr = txtstr + noteDown

                txtstr = txtstr + ' '
                fileOperations.writeEmptyNote(fout, RaagaTable, speed)

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
                    fileOperations.startMeasure(fout,'PATTERN:'+Pattern+' - AAROH',MeasureNumber,speed)

                    MeasureNumber +=1
                    for a in range(AarohLength):
            
                        #Loop through pattern for Aaroh
                        patternCnt = 0
                        printPattern = True
                        printList = []
                        
                        for p in Pattern:
                            patternCnt +=1
                            currPattern = getCurrentPattern(int(p) + a,AarohLength)
                            
                            if int(p) + a > AarohLength:
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
                    
                    fileOperations.startMeasure(fout,'PATTERN:'+Pattern+' - AVAROH',MeasureNumber,speed)
                    MeasureNumber +=1
                if not True in [int(i)>AvarohLength for i in Pattern]:
                    for a in range(AvarohLength):
            
                        #Loop through pattern for Aaroh
                        patternCnt = 0
                        printPattern = True
                        printList = []
                        
                        for p in Pattern:
                            currPattern = getCurrentPattern(int(p) + a,AvarohLength)
                            patternCnt +=1
            
                            if int(p) + a > AvarohLength:
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
                    fileOperations.startMeasure(fout,'PATTERN:'+Pattern+' - AAROH',MeasureNumber,speed)
                    MeasureNumber +=1
                    
                    for a in range(AarohLength):
            
                        #Loop through pattern for Aaroh
                        patternCnt = 0
                        patternLen = len(Pattern)
            
                        for p in Pattern:
                            currPattern = getCurrentPattern(int(p) + a,AarohLength)
                            patternCnt +=1
                            
                            #print(currPattern)    
                            #Search Sequence in CurrentRaag and get the LyricalNote
                            CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Aaroh")])['LyricalNote']).to_string(index=False)
                            txtstr = txtstr + CurrentNote
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
            
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
            
                            if patternCnt == 1:
                                fout.write (strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">'))
                            elif patternCnt == patternLen:
                                fout.write (strToWrite.replace("begin","end").replace("eighth",speed))
                                txtstr = txtstr + ' '
                            else:
                                fout.write (strToWrite.replace("begin","continue").replace("eighth",speed))
                            fout.write('\n')
            
                        # Find how many notes are missing for the 8 Beat and add Z note
                        MissingNotes = 4 - len(Pattern)%4
                        if MissingNotes == 4:
                            MissingNotes = 0
            
                        # Loop Through missing notes and add the unpitched note
                        for m in range(MissingNotes):
                            fileOperations.writeEmptyNote(fout, RaagaTable, speed)
            
                    fout.write('  </measure>\n')
                    fouttxt.write(txtstr)
                    fouttxt.write('\n')
                    txtstr = ""
                    
                    fileOperations.startMeasure(fout,'PATTERN:'+Pattern+' - AVAROH',MeasureNumber,speed)
                    MeasureNumber +=1
                    for a in range(AvarohLength):
            
                        #Loop through pattern for Aaroh
                        patternCnt = 0
                        patternLen = len(Pattern)
                        
                        for p in Pattern:
                            currPattern = getCurrentPattern(int(p) + a,AvarohLength)
                            patternCnt +=1
            
                            #print(currPattern)    
                            #Search Sequence in CurrentRaag and get the LyricalNote
                            CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (CurrentRaag['Aaroh_Avaroh'] == "Avaroh")])['LyricalNote']).to_string(index=False)
                            txtstr = txtstr + CurrentNote
                            CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (RaagaTable['Scale'] == Scale)]
            
                            strToWrite = (CurrentXML['XMLNotation']).to_string(index=False)
                            if patternCnt == 1:
                                fout.write (strToWrite.replace("eighth",speed).replace('<text>','<text font-size="20">'))
                            elif patternCnt == patternLen:
                                fout.write (strToWrite.replace("begin","end").replace("eighth",speed))
                                txtstr = txtstr + ' '
                            else:
                                fout.write (strToWrite.replace("begin","continue").replace("eighth",speed))
                            
                            
                            fout.write('\n')
            
                        # Find how many notes are missing for the 8 Beat and add Z note
                        MissingNotes = 4 - len(Pattern)%4
                        if MissingNotes == 4:
                            MissingNotes = 0
            
                        # Loop Through missing notes and add the unpitched note
                        for m in range(MissingNotes):
                            fileOperations.writeEmptyNote(fout, RaagaTable, speed)
            
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
            fileOperations.startMeasure(fout,'MERUKHAND - AAROH',MeasureNumber,speed)
            AarohList = helperFunctions.merukhand(merukhandPattern,AarohLength)

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
        
                    fileOperations.writeEmptyNote(fout, RaagaTable, speed)
        
                    if currCount in( 24,48,72,96):
                        fout.write('  </measure>\n')
                        MeasureNumber +=1
                        fileOperations.startMeasure(fout,'',MeasureNumber,speed)

                fout.write('  </measure>\n')
                fouttxt.write(txtstr)
                fouttxt.write('\n')
                txtstr = ""
                MeasureNumber +=1
                fileOperations.startMeasure(fout,'',MeasureNumber,speed)

            fout.write('  </measure>\n')
            MeasureNumber +=1
            fileOperations.startMeasure(fout,'MERUKHAND - AVAROH',MeasureNumber,speed)
            AvarohList = helperFunctions.merukhand(merukhandPattern,AvarohLength)
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
        
                    fileOperations.writeEmptyNote(fout, RaagaTable, speed)
        
                    if currCount in( 24,48,72,96):
                        fout.write('  </measure>\n')
                        MeasureNumber +=1
                        fileOperations.startMeasure(fout,'',MeasureNumber,speed)

                fout.write('  </measure>\n')
                fouttxt.write(txtstr)
                fouttxt.write('\n')
                txtstr = ""
                MeasureNumber +=1
                fileOperations.startMeasure(fout,'',MeasureNumber,speed)
            fout.write('  </measure>\n')     
        ###########################################
        fout.write('  </part>\n')
        fout.write('</score-partwise>\n')
    
        fout.close()
        fouttxt.close()
        #check_output('"mscore3" +outFileSuffix+'.xml" ' +'-o "output\\'+Raag+Scale+outFileSuffix+'.pdf"', shell=True)
        check_output('"mscore3" "' +outFileSuffix+'.xml" ' + '-o "' +outFileSuffix+'.mp3"', shell=True)
        #check_output('"MuseScore3.exe" "output\\'+Raag+Scale+outFileSuffix+'.xml" ' +'-o "output\\'+Raag+Scale+outFileSuffix+'.mp3"', shell=True)
        print ('Your files are generated in the output directory under this folder. Please open the PDF and the MP3 to sing along')

if __name__ == '__main__':
    main()
