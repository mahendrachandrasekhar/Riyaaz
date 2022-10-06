def initializeFile(xmlHandle, Raag, instrument):

    xmlHandle.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    xmlHandle.write('<!-- MusicXML symbolic note types range from 1024th notes to maxima notes: 1024th, 512th, 256th, 128th, 64th, 32nd, 16th, eighth, quarter, half, whole, breve, long, and maxima.-->\n')
    xmlHandle.write('<score-partwise version="3.1">\n')
    xmlHandle.write('  <defaults>\n')
    xmlHandle.write('    <scaling>\n')
    xmlHandle.write('      <millimeters>7</millimeters>\n')
    xmlHandle.write('      <tenths>40</tenths>\n')
    xmlHandle.write('      </scaling>\n')
    xmlHandle.write('    <page-layout>\n')
    xmlHandle.write('      <page-height>2400.69</page-height>\n')
    xmlHandle.write('      <page-width>4016.74</page-width>\n')
    xmlHandle.write('      <page-margins type="even">\n')
    xmlHandle.write('        <left-margin>85.7143</left-margin>\n')
    xmlHandle.write('        <right-margin>85.7143</right-margin>\n')
    xmlHandle.write('        <top-margin>85.7143</top-margin>\n')
    xmlHandle.write('        <bottom-margin>85.7143</bottom-margin>\n')
    xmlHandle.write('        </page-margins>\n')
    xmlHandle.write('      <page-margins type="odd">\n')
    xmlHandle.write('        <left-margin>30.7143</left-margin>\n')
    xmlHandle.write('        <right-margin>30.7143</right-margin>\n')
    xmlHandle.write('        <top-margin>85.7143</top-margin>\n')
    xmlHandle.write('        <bottom-margin>85.7143</bottom-margin>\n')
    xmlHandle.write('        </page-margins>\n')
    xmlHandle.write('      </page-layout>\n')
    xmlHandle.write('    <word-font font-family="Edwin" font-size="10"/>\n')
    xmlHandle.write('    <lyric-font font-family="Edwin" font-size="10"/>\n')
    xmlHandle.write('    </defaults>\n')

    xmlHandle.write('  <credit page="1">\n')
    xmlHandle.write('    <credit-type>title</credit-type>')
    xmlHandle.write('    <credit-words justify="center" valign="top" font-size="22">Raag ' + Raag +
                    ' - Sujaan Music.\nNotations:Sa->S, Komal Re->r, Shudda Re->R, Komal Ga->g, Shudda Ga ->G,Shudda Ma ->m,\nTeevra Ma->M,Pa->P, Komal Dha->d, Shudda Dha->D, Komal Ni->n,Shudda Ni->N</credit-words>\n')
    xmlHandle.write('    </credit>\n')
    xmlHandle.write('  <part-list>')
    xmlHandle.write('    <score-part id="P1">\n')
    xmlHandle.write('      <part-name>Raag ' + Raag + '</part-name>\n')
    xmlHandle.write('      <score-instrument id="P1-I1">\n')
    xmlHandle.write('      <instrument-name></instrument-name>\n')
    xmlHandle.write('      </score-instrument>\n')
    xmlHandle.write('      <midi-device id="P1-I1" port="1"></midi-device>\n')
    xmlHandle.write('      <midi-instrument id="P1-I1">\n')
    xmlHandle.write('      <midi-channel>1</midi-channel>\n')

    if instrument == 'Reed Organ':
        xmlHandle.write('      <midi-program>21</midi-program>\n')
    elif instrument == 'Harmonica':
        xmlHandle.write('      <midi-program>23</midi-program>\n')
    elif instrument == 'Harp':
        xmlHandle.write('      <midi-program>47</midi-program>\n')
    elif instrument == 'Voice':
        xmlHandle.write('      <midi-program>55</midi-program>\n')
    elif instrument == 'Koto':
        xmlHandle.write('      <midi-program>108</midi-program>\n')
    elif instrument == 'Shenai':
        xmlHandle.write('      <midi-program>112</midi-program>\n')
    elif instrument == 'Violin':
        xmlHandle.write('      <midi-program>41</midi-program>\n')
    elif instrument == 'Sitar':
        xmlHandle.write('      <midi-program>105</midi-program>\n')
    elif instrument == 'Cello':
        xmlHandle.write('      <midi-program>43</midi-program>\n')
    elif instrument == 'Ukulele':
        xmlHandle.write('      <midi-program>25</midi-program>\n')
    elif instrument == 'Guitar':
        xmlHandle.write('      <midi-program>26</midi-program>\n')
    else:
        xmlHandle.write('      <midi-program>21</midi-program>\n')

    xmlHandle.write('      <pan>0</pan>\n')
    xmlHandle.write('      </midi-instrument>\n')
    xmlHandle.write('    </score-part>\n')
    xmlHandle.write('  </part-list>\n')
    xmlHandle.write('  <part id="P1">\n')


def startMeasure(xmlHandle, header, myMeasure, myspeed):
    divisionMap = {"quarter": "1", "eighth": "2",
                   "16th": "4", "32nd": "8", "half": "0.5", "64th": "16"}
    division = divisionMap[myspeed]
    xmlHandle.write('<measure number="'+str(myMeasure) +
                    '"><print new-system="yes"></print>\n<direction placement="above"><direction-type><words relative-y="10.00">'+header+'</words></direction-type></direction>')
    xmlHandle.write('\n<attributes><divisions>'+division +
                    '</divisions><key><fifths>0</fifths></key><clef><sign>G</sign><line>2</line></clef></attributes>')


def writeEmptyNote(xmlHandle, lookupTable, myspeed):
    xmlLookup = lookupTable.loc[(lookupTable['LyricalNote'] == 'Z')]
    myStrToWrite = (xmlLookup['XMLNotation']).to_string(index=False).strip()
    xmlHandle.write(myStrToWrite.replace(
        "begin", "end").replace("eighth", myspeed))
    xmlHandle.write('\n')


def findAndWriteCurrentNoteWithPrefix(xmlHandle, myRaag, currPattern, Aaroh_Or_Avaroh, myStrToPrefix, myRaagaTable, myScale, mySpeed):
    myNote = ((myRaag.loc[(myRaag['Sequence'] == currPattern) & (
        myRaag['Aaroh_Avaroh'] == Aaroh_Or_Avaroh)])['LyricalNote']).to_string(index=False).strip()
    myXML = myRaagaTable.loc[(myRaagaTable['LyricalNote'] == myNote) & (
        myRaagaTable['Scale'] == myScale)]
    myStrToWrite = (myXML['XMLNotation']).to_string(index=False).strip()
    xmlHandle.write(myStrToPrefix.replace("eighth", mySpeed) +
                    myStrToWrite.replace("begin", "end").replace("eighth", mySpeed))
    return myNote


def endMeasure(xmlHandle, csvHandle, myStr):
    xmlHandle.write('  </measure>\n')
    if myStr != "":
        csvHandle.write(myStr)
    csvHandle.write('\n')
    return ""
