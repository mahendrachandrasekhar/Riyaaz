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

def printSelection(inputPitch, outFileSuffix, speed, inputRaag, includeLibraryPaltas, inputPattern, includeAarohAvaroh, includeBasicPattern2, includeBasicPattern3, includeBasicPaltas, includeMerukhand, merukhandPattern, instrument):
    print ('Input Pitch is ', inputPitch)
    print ('Speed is ', speed)
    print ('Raaga Selected is ', inputRaag)
    print ('includeLibraryPaltas ', includeLibraryPaltas)
    print ('includeAarohAvaroh ', includeAarohAvaroh)
    print ('includeBasicPattern2 ', includeBasicPattern2)
    print ('includeBasicPattern3 ', includeBasicPattern3)
    print ('includeBasicPaltas ', includeBasicPaltas)
    print ('includeMerukhand ', includeMerukhand)



#print(os.path.dirname(os.path.realpath(__file__)))
