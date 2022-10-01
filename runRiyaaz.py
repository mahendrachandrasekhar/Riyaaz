import getopt
import os
import mainRiyaaz
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:],"hp:o:s:r:l:t:a:x:y:b:m:k:i:",["inputPitch=", "outFileSuffix=", "speed=", "inputRaag=", "includeLibraryPaltas=", "inputPattern=", "includeAarohAvaroh=", "includeBasicPattern2=", "includeBasicPattern3=", "includeBasicPaltas=", "includeMerukhand=", "merukhandPattern=", "instrument="])
except getopt.GetoptError:
    print ('GeneratePalta.py -p <Pitch> -o <OutputFileSuffix> -s <Speed>')
    sys.exit(2)


inputPitch = ''
outFileSuffix = ''
speed = ''
inputRaag = ''
includeLibraryPaltas = False
inputPattern = ''
includeAarohAvaroh = False
includeBasicPattern2 = False
includeBasicPattern3 = False
includeBasicPaltas = False
includeMerukhand = False
merukhandPattern = ''
instrument = ''

for opt, arg in opts:
    if opt == '-h':
        print ('GeneratePalta.py -p Pitch -o OutputFileSuffix - s Speed')
        sys.exit()
    elif opt in ("-p", "--inputPitch"):
        inputPitch = arg
    elif opt in ("-o", "--outFileSuffix"):
        outFileSuffix = arg
    elif opt in ("-s", "--speed"):
        speed = arg
    elif opt in ("-r", "--inputRaag"):
        inputRaag = arg
    elif opt in ("-l", "--includeLibraryPaltas"):
        includeLibraryPaltas = arg
    elif opt in ("-t", "--inputPattern"):
        inputPattern = arg
    elif opt in ("-a", "--includeAarohAvaroh"):
        includeAarohAvaroh = arg
    elif opt in ("-x", "--includeBasicPattern2"):
        includeBasicPattern2 = arg
    elif opt in ("-y", "--includeBasicPattern3"):
        includeBasicPattern3 = arg
    elif opt in ("-b", "--includeBasicPaltas"):
        includeBasicPaltas = arg
    elif opt in ("-m", "--includeMerukhand"):
        includeMerukhand = arg
    elif opt in ("-k", "--merukhandPattern"):
        merukhandPattern = arg
    elif opt in ("-i", "--instrument"):
        instrument = arg

mainRiyaaz.run(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument)

##python runRiyaaz.py --inputPitch C# --outFileSuffix g --speed quarter --inputRaag Bilawal --includeLibraryPaltas False --inputPattern '' --includeAarohAvaroh True --includeBasicPattern2 True --includeBasicPattern3 True --includeMerukhand False --merukhandPattern "" --instrument "Reed Organ"
##python runRiyaaz.py --inputPitch C# --outFileSuffix g --speed quarter --inputRaag Bilawal --includeAarohAvaroh True --includeBasicPattern2 True --includeBasicPattern3 True --includeMerukhand False --merukhandPattern "" --instrument "Reed Organ"
##python runRiyaaz.py --inputPitch C# --outFileSuffix g --speed quarter --inputRaag Bilawal --includeLibraryPaltas False --inputPattern '' --includeAarohAvaroh True --includeBasicPattern2 True --includeBasicPattern3 True --includeBasicPaltas True --includeMerukhand False --merukhandPattern "" --instrument "Reed Organ"
##python runRiyaaz.py --inputPitch C# --outFileSuffix g --speed quarter --inputRaag Bilawal --includeAarohAvaroh True --includeBasicPattern2 True --includeBasicPattern3 True --includeMerukhand False --merukhandPattern "" --instrument "Reed Organ" --includeBasicPaltas True