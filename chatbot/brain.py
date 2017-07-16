import csv
import random
import ast#??????????????????????????????????
import json
from pathlib import Path

# what's your name? phill. really?  is that a real name? im excited!

testMem = {'data': 'null',
           'phraseTypes':{
                             'greetings': 
                                          {'hi!': 
                                                  {'respList': ['howdy!', 'sup dawg?'],
                                                   'stats': 'null'                    },
                                           'howdy!': 
                                                    {'respList': ['hey there good buddy!'],
                                                     'stats': 'null'                       }},
                             'statements': {'I like dogs.':{'respList':['null'],
                                                            'stats': 'null'    }}}}

class Brain:
    def __init__(self, suPac):
        self.MEM_PATH = suPac['MEMORY_PATH']
        self.COMMAND_LIST = suPac['COMMAND_LIST']
        self.PUNC_LIST = suPac['PUNC_LIST']
        self.OGgreetings = suPac['OG_GREETINGS']
        
        self.UI_NUM_SPACES_BEFORE_OUTPUT = suPac['UI_NUM_SPACES_BEFORE_OUTPUT']
        self.UI_LINE_LENGTH = suPac['UI_LINE_LENGTH']
        self.UI_NUM_SPACES_BEFORE_INPUT = suPac['UI_NUM_SPACES_BEFORE_INPUT']
        self.UI_INPUT_PROMT_SYMBOL = suPac['UI_INPUT_PROMT_SYMBOL']
        
        
        self.mem = {}
        self.inList = []
        self.outList = []
        self.endProgram = False
        self.numResponses = 0
        
        self.memShell = {'data': 'null',
                         'phraseTypes': {}}
                         
        self.phraseDataShell = {'respList': [],
                                'stats': 'null'}
                                
        self.phraseTypePuncDict = {'greetings' : None,
                                   'statements': '.',
                                   'questions' : '?',
                                   'bangs'     : '!'   }
        
        #build
        memFile = Path(self.MEM_PATH)
        if memFile.exists():
            self.loadMem()
        else:
            self.buildNewMem()
            
            
#==========================================================================================
#==========================================================================================
#
#   "PUBLIC"
#
#==========================================================================================
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

    def getGreeting(self):#improve!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -right now just rand!!!!!!!!!!!!
        randGreetDict = self.randFromDict(self.mem['phraseTypes']['greetings'])
        greeting = randGreetDict['key']
        return greeting
        
        
    def getResponse(self):
        self.numResponses += 1
        
        #get input
        unFormattedInput = self.getLast(self.inList)
        input = self.formatPhrase(unFormattedInput)
        
        #check to see if a response to input is already in memory
        knownResp = self.respInMem(input)
        if knownResp == False:
            response = self.guessResp(input)
        else:
            response = knownResp
        return response
        
        
    def executeCommand(self, command):
        self.fancyPrint('Executing Command: ' + command, self.UI_NUM_SPACES_BEFORE_OUTPUT)
        print('')
        if command == 'print memory':
            print('Printing memory...')
            print(self.mem)
        elif command == 'backup memory':
            pass
        elif command == 'end':
            self.endProgram = True
        elif command == 'test':
            self.fancyPrint('This is a test. i am putting one space at the end.', 1)
        else:
            print('ERROR: executeCommand()')

            
    def logInteraction(self):
        #get input and output and related info
        unFormattedInput = self.getLast(self.inList)
        input = self.formatPhrase(unFormattedInput)
        output = self.getLast(self.outList)
        outPhraseType = self.getPhraseType(output)
        if 'OGgreeting' in self.mem['phraseTypes'][outPhraseType][output]['stats']:
            outOGgreetStat = self.mem['phraseTypes'][outPhraseType][output]['stats']['OGgreeting']
        else:
            outOGgreetStat = False
          
        #add input to output's respList if not already there
        if input not in self.mem['phraseTypes'][outPhraseType][output]['respList']:
            self.mem['phraseTypes'][outPhraseType][output]['respList'].append(input)
           
        #find inPhraseType 
        if outPhraseType == 'greetings' and outOGgreetStat == True:#if output is OGgreeting, input is now a new greeting
            inPhraseType = 'greetings'
        else:
            inPhraseType = self.getPhraseType(input)
       
        #save input as new phrase if it doesnt already exists
        if input not in self.mem['phraseTypes'][inPhraseType]:
            self.addPhrase(input, inPhraseType)
            
        #save to csv
        self.saveMem(self.mem)

    #prints and logs outPhrase
    def output(self, outPhrase):
        self.fancyPrint(outPhrase, self.UI_NUM_SPACES_BEFORE_OUTPUT)
        self.outList.append(outPhrase)
        self.numResponses += 1
    
        
    #prompts for, logs, then returns user input
    def getInput(self):
        preInSpaceStr = ' ' * self.UI_NUM_SPACES_BEFORE_INPUT
        inPhrase = input(preInSpaceStr + self.UI_INPUT_PROMT_SYMBOL)
        self.inList.append(inPhrase)
        return inPhrase        
    
    
    #makes user feel bad for being dumb
    def scold(self, scoldType):
        if scoldType == 'incorect punctuation':
           scoldStr = 'Please use correct punctuation you uncultured swine! Lets try that again...'
        else:
            pass#add more lator
        self.fancyPrint(scoldStr, self.UI_NUM_SPACES_BEFORE_OUTPUT)
        print('')
   
   
    def formatPhrase(self, phrase):    
        postSentSpace = ' ' #this really should be a UI option but changing it might break fancyPrint and I am lazy                
        #get list of all sentances (uncapitalized)
        sentList = self.splitSents(phrase)
        #capitalize first letter of every sentance 
        capSentList = []
        for sent in sentList:
            capSentList.append(self.capSent(sent))  
        #put it all together into one phrase
        finalPhrase = ''
        for sent in capSentList:
            finalPhrase = finalPhrase + postSentSpace + sent  
        #clean then return
        finalPhrase = finalPhrase.strip()
        return finalPhrase  
      
    def correctlyPunctuated(self, phrase):
        for punc in self.PUNC_LIST:
            if phrase.endswith(punc) == True:
                return True
        return False       

    def getLast(self, list):
        lastItemPos = len(list) - 1
        lastItem = list[lastItemPos]
        return lastItem        
   
#==========================================================================================
#==========================================================================================
#
#   "PRIVATE"
#
#==========================================================================================
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV   

#==========================================================================================
#   "PRIVATE"   Interact with csv
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

    def loadMem(self):
        #build loadMemShell for basis of mem
        loadMemShell = self.memShell
        for phraseType, punc in self.phraseTypePuncDict.items():
            loadMemShell['phraseTypes'][phraseType] = {}
        self.mem = loadMemShell
        #load csv data into mem
        with open(self.MEM_PATH, 'rt') as csvfile:
#             self.mem = {'data': 'null',
#                         'phraseTypes':{'greetings':{},#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#                                        'statements':{}}}
            memReader = csv.DictReader(csvfile)
            for row in memReader:
                for phraseType, phraseDict in self.mem['phraseTypes'].items():         
                   if not not row[phraseType+'Data']:
                       #convert string to dict
                       phraseDataStr = row[phraseType + 'Data'] 
                       phraseDataDict = ast.literal_eval(phraseDataStr)
                       #add phraseData to mem
                       self.mem['phraseTypes'][phraseType][row[phraseType]] = phraseDataDict
                       
    def saveMem(self, mem):#maybe go back at end and remove this var??????????????
        with open(self.MEM_PATH, 'wt') as csvfile:
            fieldnames = []
            for memSection, sectionData in mem.items():
                #section specific load instructions
                if memSection == 'data':
                    fieldnames.append(memSection)
                if memSection == 'phraseTypes':
                    for phraseType, phrase in mem['phraseTypes'].items():
                        fieldnames.append(phraseType)
                        fieldnames.append((phraseType + 'Data'))
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
            writer.writeheader()
            
            #build rowDictList
            rowDictList = []
            for phraseType, phrases in mem['phraseTypes'].items():
                rdlPos = 0
                for phrase, phraseData in mem['phraseTypes'][phraseType].items():
                    if rowDictList == [] or rdlPos > (len(rowDictList) - 1):
                        rowDictList.append({})
                    rowDictList[rdlPos][phraseType] = phrase
                    rowDictList[rdlPos][(phraseType + 'Data')] = mem['phraseTypes'][phraseType][phrase]# used to = phraseType, fix!!!!!!!!!!!!!!!!!!!!
                    rdlPos +=1
            #write rows
            for rowDict in rowDictList:
               writer.writerow(rowDict)
        csvfile.close()
               
    
#==========================================================================================
#   "PRIVATE"   Edit self.mem
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV    

    def buildNewMem(self):#need to put in OG greetings
        print('No memory found, building new memory...')
        #add headers
        self.mem = self.memShell
        for phraseType, symb in self.phraseTypePuncDict.items():
            self.mem['phraseTypes'][phraseType] = {}
        
        #add OGgreetings
        for OGgreeting in self.OGgreetings:
            self.addPhrase(OGgreeting, 'greetings', True)
        
        #write to csv
        self.saveMem(self.mem)
        self.loadMem()#NEED!!!
        print('HAPPY BIRTHDAY!')
        print('')
        
        
    #OGgreeting should only be true if you are tyring to add a new OGgreeting
    def addPhrase(self, phrase, phraseType, OGgreeting = False):
        self.mem['phraseTypes'][phraseType][phrase] = self.phraseDataShell
        if OGgreeting == False:
            if phraseType == 'greetings':
                self.mem['phraseTypes'][phraseType][phrase]['stats'] = {'OGgreeting': False}
            #need something in stats for other phraseTypes???????????????????????????????????????
        else:
            self.mem['phraseTypes'][phraseType][phrase]['stats'] = {'OGgreeting':True}
            #more???????????????????????????????????????????????????????????????????????????
         
#==========================================================================================
#   "PRIVATE"   Read from self.mem
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV    
    
    #if respList to input not empty, return rand resp form respList,
    #if respList to input empty, return False
    def respInMem(self, input):
        respFound = False
        
        for phraseType in self.mem['phraseTypes']:
            #print('phraseType:', phraseType)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            for phrase in self.mem['phraseTypes'][phraseType]:
                #print('phrase:', phrase)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if phrase == input:
                    respList = self.mem['phraseTypes'][phraseType][phrase]['respList']
                    #print('respList:', respList)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    if respList != []:
                        response = random.choice(respList)
                        #print('resp:', response)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        return response
                    else:    
                        return False
        return False

    
    def guessResp(self, input):
        #pick random phraseType - build list of valid phraseTypes then choose random phraseType from list
        phraseTypeList = []
        for phraseType, phrase in self.mem['phraseTypes'].items():
           if phraseType != 'greetings' and  self.mem['phraseTypes'][phraseType] != {}:
                phraseTypeList.append(phraseType)
        #print('phraseTypeList:', phraseTypeList)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if phraseTypeList == []:
            return self.getGreeting()
        else:
            phraseType = random.choice(phraseTypeList)
        
        
#         phraseTypeFound = False
#         while(phraseTypeFound == False):
#             phraseTypeDict = self.randFromDict(self.mem['phraseTypes'])
#             phraseType = phraseTypeDict['key']
#             if phraseType != 'greetings':
#                 phraseTypeFound = True    
#         print('phraseType:', phraseType)#!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        #pick and return random phrase of chosen phraseType
        phraseDict = self.mem['phraseTypes'][phraseType]
        respDict = self.randFromDict(phraseDict)
        response = respDict['key']
        return response
              

    def getPhraseType(self, phrase):
        if phrase in self.mem['phraseTypes']['greetings']:
            return 'greetings'
        else:
            for phraseType, punc in self.phraseTypePuncDict.items():
                if phraseType != 'greetings':
                    if phrase.endswith(punc) == True:
                        return phraseType
                
            
    def isGreeting(self, phrase):#if you never use this again just pput it in getPhraseType#NEED???????????
        for curPhrase, phraseData in self.mem['phraseTypes']['greetings']:
            if curPhrase == phrase:
                return True
        return False
    
#==========================================================================================
#   "PRIVATE"   Other
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV  
    
    #should be used for any official print to screen
    def fancyPrint(self, printPhrase, numPreSpaces):#IS THIS FUNC StILL IN RIGHT SPOT??????????????????????????????????????????
        printList = []
        PreSpaceStr = ' ' * numPreSpaces
        
         #break up printPhrase into list of lines to print
        curPos = 0
        while (len(printPhrase) - curPos) > self.UI_LINE_LENGTH:
            addPos = self.UI_LINE_LENGTH
            while printPhrase[curPos + addPos] != ' ' and addPos != 0:#aPos = 0 means one word is bigger than UI_LINE_LENGTH
                addPos -= 1
            if addPos == 0:
                printList.append(printPhrase[curPos: (curPos + (self.UI_LINE_LENGTH - 1))] + '-')
                curPos += self.UI_LINE_LENGTH - 1
            else:
                addPos += 1 #this makes the space between words print at end of each line 
                printList.append(printPhrase[curPos: (curPos + addPos)])
                curPos += addPos
        printList.append(printPhrase[curPos:]) 
        
        #print broken up lines to screen
        for line in printList:
            print(PreSpaceStr + line)
                
                    
    def randFromDict(self, dict):
        key, val = random.choice(list(dict.items()))
        randDict = {'key': key,
                    'val': val}
        return randDict  
    
    
    def capSent(self, sent):
        firstLetter = sent[0]
        restOfSent = sent[1:]
        CapFirstLetter = firstLetter.upper()
        finalSent = CapFirstLetter + restOfSent
        return finalSent
  
  
    def splitSents(self, phrase):
        sentList = [phrase]
        for punc in self.PUNC_LIST:
            tempSentList = []
            for sent in sentList:
                if punc in sent:
                    splitSentList = sent.split(punc)
                    for sent in splitSentList:
                        tempSentList.append(sent)
                else:
                    tempSentList.append(sent)
                sentList = []
                for sent in tempSentList:
                    if self.correctlyPunctuated(sent) == True:
                        sentList.append(sent)
                    else:
                        sentList.append(sent + punc)
        #clean up
        cleanSentList = []
        for sent in sentList:
            if len(sent) != 1: #to get rid of extra punc
                cleanSentList.append(sent.strip())
        return cleanSentList
        
  

 