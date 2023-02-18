#!/usr/bin/python
import sys
from timeit import repeat
import pandas as pd
import os
from datetime import datetime
from datetime import date
from subprocess import check_output
import helperFunctions
import fileOperations
import gsheetData

def cleanupFile(filename):
    check_output('rm ' + filename+'.* ', shell=True)


def getRaagList(myRaag):
    if myRaag == '':
        #myRaagList = pd.read_csv("Data-RaagaList.csv")
        myRaagList = gsheetData.get_gsheet("RaagaList")
    else:
        d = {'RaagaName': [myRaag]}
        myRaagList = pd.DataFrame(data=d)
    return myRaagList


def getAarohAvaroh(basicFileName, extensionFileName):
    # Get the basic Aaroh Avaroh
    #AarohAvarohBasic = pd.read_csv(basicFileName)
    AarohAvarohBasic = gsheetData.get_gsheet(basicFileName)
    AarohAvarohBasic.drop('Notation', axis=1, inplace=True)

    # Get the Aaroh Avaroh including the next Octave.
    #AarohAvarohExtended = pd.read_csv(extensionFileName)
    AarohAvarohExtended = gsheetData.get_gsheet(extensionFileName)
    # The File template used will generate blank rows, so remove it out
    AarohAvarohExtended.drop(AarohAvarohExtended.index[(
        AarohAvarohExtended["Raag"].isnull())], axis=0, inplace=True)

    return pd.concat([AarohAvarohBasic, AarohAvarohExtended])


def getCurrentPattern(n, len):
    if n == len:
        return 100
    elif n > len:
        return 100 + n - len
    else:
        return n


def getAarohAvarohLen(myRaag, myDirection):
    return len((myRaag.loc[(myRaag['Sequence'] <= 100) & (myRaag['Aaroh_Avaroh'] == myDirection)]))


def main():
    print('Do Nothing')


def run(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument):

    txtstr = ''
    repeat = False

    # Set the pandas options so that they print poperly in the XML files
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    if merukhandPattern == '':
        merukhandPattern = list('123')
    else:
        merukhandPattern = list(merukhandPattern)

    helperFunctions.printSelection(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh,
                                   includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument)
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Get the Raaga table
    #RaagaTable = pd.read_csv("Data-RaagasNotationsAndMusicXMLNotations.csv")
    RaagaTable = gsheetData.get_gsheet("RaagasNotationsAndMusicXMLNotations")
    #AarohAvaroh = getAarohAvaroh("Data-Aaroh-Avaroh-Basic.csv", "Data-Aaroh-Avaroh-Extension.csv")
    AarohAvaroh = getAarohAvaroh("Aaroh-Avaroh-Basic", "Aaroh-Avaroh-Extension")
    RaagList = getRaagList(inputRaag)
    Scale = inputPitch

    for Raag in RaagList['RaagaName']:
        # Initialize files
        fouttxt = open(outFileSuffix+".csv", mode='w')
        fout = open(outFileSuffix+".xml", mode='w')
        fileOperations.initializeFile(fout, Raag, instrument)
        MeasureNumber = 0

        # Get all the notes for the Raag in a table
        CurrentRaag = AarohAvaroh.loc[AarohAvaroh['Raag'] == Raag]
        AarohLength = getAarohAvarohLen(CurrentRaag, "Aaroh")
        AvarohLength = getAarohAvarohLen(CurrentRaag, "Avaroh")

        fouttxt.write("Raag "+ inputRaag+"\n")

        ##########################################
        simplePatternCnt = 0
        for simplePattern in [includeAarohAvaroh, includeBasicPattern2]:
            ##########################################
            if simplePattern:

                for direction in ["Aaroh", "Avaroh"]:
                    for x in [True,repeat]:
                        if x:
                            fileOperations.startMeasure(
                                fout, direction, MeasureNumber, speed)
                            directionlen = getAarohAvarohLen(CurrentRaag, direction)

                            # Pattern Init
                            if simplePatternCnt == 0:  # BASIC AAROH AND AVAROH
                                firstNote = ""
                                firstXML = ""
                                strToPrefix = ""
                            # Pattern type 1-- BEGIN - Aaroh (SS,SR, SG...)
                            if simplePatternCnt == 1:
                                if direction == 'Aaroh':
                                    txtstr = 'Palta#:'+str(1)+'\n'
                                firstNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == 1) & (
                                    CurrentRaag['Aaroh_Avaroh'] == direction)])['LyricalNote']).to_string(index=False).strip()
                                firstXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == firstNote) & (
                                    RaagaTable['Scale'] == Scale)]
                                strToPrefix = (firstXML['XMLNotation']).to_string(index=False).strip()

                            for a in range(directionlen):
                                currPattern = getCurrentPattern(a + 1, directionlen)
                                CurrentNote = fileOperations.findAndWriteCurrentNoteWithPrefix(
                                    fout, CurrentRaag, currPattern, direction, strToPrefix, RaagaTable, Scale, speed)
                                fileOperations.writeEmptyNote(fout, RaagaTable, speed)
                                txtstr = txtstr + firstNote + CurrentNote + ' '

                            txtstr = fileOperations.endMeasure(fout, fouttxt, txtstr)
                            MeasureNumber += 1
                simplePatternCnt += 1
        ##########################################
        ##########################################
        if includeBasicPattern3:
            for direction in ["Aaroh", "Avaroh"]:
                # Pattern type 2-- BEGIN (S, SRS,SRGRS, SRGMGRS...)
                fileOperations.startMeasure(
                    fout, "Pattern 2 - "+direction, MeasureNumber, speed)
                directionlen = getAarohAvarohLen(CurrentRaag, direction)

                # Pattern Init
                strPrefixUp = ""
                strPrefixDown = ""
                noteUp = ""
                noteDown = ""

                for a in range(1, directionlen, 1):
                    currPattern = getCurrentPattern(a, directionlen)

                    CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (
                        CurrentRaag['Aaroh_Avaroh'] == direction)])['LyricalNote']).to_string(index=False).strip()
                    CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (
                        RaagaTable['Scale'] == Scale)]
                    strCurr = (CurrentXML['XMLNotation']).to_string(index=False).strip()
                    strToWriteUp = strPrefixUp.replace(
                        "eighth", speed) + strCurr.replace("begin", "end").replace("eighth", speed)
                    strPrefixUp = strToWriteUp
                    fout.write(strToWriteUp)

                    txtstr = txtstr + noteUp + CurrentNote
                    noteUp = noteUp + CurrentNote

                    for b in range(a-1, 0, -1):

                        currPattern = getCurrentPattern(b, directionlen)
                        CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (
                            CurrentRaag['Aaroh_Avaroh'] == direction)])['LyricalNote']).to_string(index=False).strip()
                        CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (
                            RaagaTable['Scale'] == Scale)]
                        strCurr = (CurrentXML['XMLNotation']).to_string(index=False).strip()
                        strToWriteDown = strCurr.replace(
                            "begin", "end").replace("eighth", speed)
                        fout.write(strToWriteDown)

                        noteDown = CurrentNote
                        txtstr = txtstr + noteDown

                    txtstr = txtstr + ' '
                    fileOperations.writeEmptyNote(fout, RaagaTable, speed)

                txtstr = fileOperations.endMeasure(fout, fouttxt, txtstr)

        ##########################################
        # Pattern 3: Basic Platas only till Sa
        ##########################################

        if includeBasicPaltas:
            #BasicPaltaList = pd.read_csv("Data-ListOfBasicPaltas.csv")
            BasicPaltaList = gsheetData.get_gsheet("ListOfBasicPaltas")
            currPaltaCount = 1
            printedPalta = True
            for palta in BasicPaltaList['PatlaNotation']:
                if printedPalta:
                    currPaltaCount+=1
                printedPalta = False
                Pattern = str(palta)
                patternLen = len(Pattern)

                txtstr = 'Palta#:'+str(currPaltaCount)+'\n'
                for direction in ["Aaroh", "Avaroh"]:
                    directionlen = getAarohAvarohLen(CurrentRaag, direction)
                    if not True in [int(i) > directionlen for i in Pattern]:
                        fileOperations.startMeasure(
                            fout, 'PATTERN:'+Pattern+' - ' + direction, MeasureNumber, speed)
                        MeasureNumber += 1
                        fout.write("<note><duration>1</duration><type>"+speed+"</type></note>")
                        for a in range(directionlen):

                            # Loop through pattern
                            patternCnt = 0
                            printPattern = True
                            printList = []

                            for p in Pattern:
                                patternCnt += 1
                                if (int(p) + a) > directionlen:
                                    printPattern = False
                                currPattern = getCurrentPattern(
                                    int(p) + a, directionlen)

                                CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (
                                    CurrentRaag['Aaroh_Avaroh'] == direction)])['LyricalNote']).to_string(index=False).strip()
                                txtstr = txtstr + CurrentNote
                                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (
                                    RaagaTable['Scale'] == Scale)]

                                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False).strip()

                                if patternCnt == 1:
                                    finalStrToWrite = strToWrite.replace("eighth", speed).replace(
                                        '<text>', '<text font-size="20">')
                                elif patternCnt == patternLen:
                                    finalStrToWrite = strToWrite.replace(
                                        "begin", "end").replace("eighth", speed)
                                    txtstr = txtstr + ' '
                                else:
                                    finalStrToWrite = strToWrite.replace(
                                        "begin", "continue").replace("eighth", speed)

                                printList.append(finalStrToWrite)

                            if printPattern:
                                printedPalta = True
                                for pl in printList:
                                    fout.write(pl)
                                    fout.write('\n')
                                    fouttxt.write(txtstr)
                                    txtstr = ""

                        txtstr = fileOperations.endMeasure(fout, fouttxt, "")

                fout.write('\n')
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
                currPaltaCount = 1
                printedPalta = True
                if includeLibraryPaltas:
                    #PaltaList1 = pd.read_csv("Data-ListOfPaltas.csv")
                    PaltaList1 = gsheetData.get_gsheet("ListOfPaltas")
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
                    if printedPalta:
                        currPaltaCount+=1
                    printedPalta = False
                    txtstr = 'Palta#:'+str(currPaltaCount)+'\n'
                    Pattern = str(palta)

                    for direction in ["Aaroh", "Avaroh"]:
                        directionlen = getAarohAvarohLen(
                            CurrentRaag, direction)
                        fileOperations.startMeasure(
                            fout, 'PATTERN:'+Pattern+' - ' + direction, MeasureNumber, speed)
                        MeasureNumber += 1
                        for i in range(4):
                            fout.write("<note><duration>1</duration><type>"+speed+"</type></note>")
                        for a in range(directionlen):

                            # Loop through pattern
                            patternCnt = 0
                            patternLen = len(Pattern)

                            for p in Pattern:
                                currPattern = getCurrentPattern(
                                    int(p) + a, directionlen)
                                patternCnt += 1

                                # print(currPattern)
                                # Search Sequence in CurrentRaag and get the LyricalNote
                                CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (
                                    CurrentRaag['Aaroh_Avaroh'] == direction)])['LyricalNote']).to_string(index=False).strip()
                                txtstr = txtstr + CurrentNote
                                CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (
                                    RaagaTable['Scale'] == Scale)]

                                strToWrite = (CurrentXML['XMLNotation']).to_string(index=False).strip()

                                if patternCnt == 1:
                                    fout.write(strToWrite.replace("eighth", speed).replace(
                                        '<text>', '<text font-size="20">'))
                                elif patternCnt == patternLen:
                                    fout.write(strToWrite.replace(
                                        "begin", "end").replace("eighth", speed))
                                    txtstr = txtstr + ' '
                                else:
                                    fout.write(strToWrite.replace(
                                        "begin", "continue").replace("eighth", speed))
                                fout.write('\n')

                            # Find how many notes are missing for the 8 Beat and add Z note
                            MissingNotes = 4 - len(Pattern) % 4
                            if MissingNotes == 4:
                                MissingNotes = 0

                            # Loop Through missing notes and add the unpitched note
                            for m in range(MissingNotes):
                                fileOperations.writeEmptyNote(
                                    fout, RaagaTable, speed)

                            printedPalta = True

                        txtstr = fileOperations.endMeasure(
                            fout, fouttxt, txtstr)

            except ValueError as e:
                print("Invalid input for Patterns.. It should be numbers on each line")

        ###########################################

        ##########################################
        # Merukhand
        ##########################################
        if includeMerukhand:
            for direction in ["Aaroh", "Avaroh"]:
                directionlen = getAarohAvarohLen(CurrentRaag, direction)
                fileOperations.startMeasure(
                    fout, 'MERUKHAND - ' + direction, MeasureNumber, speed)
                directionList = helperFunctions.merukhand(
                    merukhandPattern, directionlen)

                for currList in directionList:
                    currCount = 0
                    cycleCount = 0
                    for i in range(4):
                        fout.write("<note><duration>1</duration><type>"+speed+"</type></note>")
                    for currPattern in currList:
                        currCount += 1
                        CurrentNote = ((CurrentRaag.loc[(CurrentRaag['Sequence'] == currPattern) & (
                            CurrentRaag['Aaroh_Avaroh'] == direction)])['LyricalNote']).to_string(index=False).strip()
                        txtstr = txtstr + CurrentNote
                        cycleCount += 1
                        if cycleCount == len(merukhandPattern):
                            txtstr = txtstr + ' '
                            cycleCount = 0
                        CurrentXML = RaagaTable.loc[(RaagaTable['LyricalNote'] == CurrentNote) & (
                            RaagaTable['Scale'] == Scale)]
                        strToWrite = (CurrentXML['XMLNotation']).to_string(index=False).strip()

                        if currCount in (1, 25, 49, 73, 97):
                            fout.write(strToWrite.replace("eighth", speed).replace(
                                '<text>', '<text font-size="20">'))
                        elif currCount == len(currList):
                            fout.write(strToWrite.replace(
                                "begin", "end").replace("eighth", speed))
                        else:
                            fout.write(strToWrite.replace(
                                "begin", "continue").replace("eighth", speed))

                        fileOperations.writeEmptyNote(fout, RaagaTable, speed)

                        if currCount in (24, 48, 72, 96):
                            fout.write('  </measure>\n')
                            MeasureNumber += 1
                            fileOperations.startMeasure(
                                fout, '', MeasureNumber, speed)

                    txtstr = fileOperations.endMeasure(fout, fouttxt, txtstr)
                    MeasureNumber += 1
                    fileOperations.startMeasure(fout, '', MeasureNumber, speed)

                fout.write('  </measure>\n')
                MeasureNumber += 1
        ###########################################
        fout.write('  </part>\n')
        fout.write('</score-partwise>\n')

        fout.close()
        fouttxt.close()
        # check_output('"mscore3" +outFileSuffix+'.xml" ' +'-o "output\\'+Raag+Scale+outFileSuffix+'.pdf"', shell=True)
        check_output('"mscore3" "' + outFileSuffix+'.xml" ' +
                     '-o "' + outFileSuffix+'.mp3"', shell=True)
        #check_output('"MuseScore3.exe" "output\\'+Raag+Scale+outFileSuffix+'.xml" ' +'-o "output\\'+Raag+Scale+outFileSuffix+'.mp3"', shell=True)
        print('Your files are generated in the output directory under this folder. Please open the PDF and the MP3 to sing along')


if __name__ == '__main__':
    main()
