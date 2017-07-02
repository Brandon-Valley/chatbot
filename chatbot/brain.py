import csv
import random
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
        self.PRE_CB_UI_STR = suPac['PRE_CB_UI_STR']
        self.POST_CB_UI_STR = suPac['POST_CB_UI_STR']
        self.POST_SENT_SPACE = suPac['POST_SENT_SPACE']
        self.OGgreetings = suPac['OG_GREETINGS']
        
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
            
            
#         self.saveMem()#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    def buildNewMem(self):#need to put in OG greetings
        print('No memory found, building new memory...')
        #build seed
        memSeed = self.memShell
        for phraseType, symb in self.phraseTypePuncDict.items():
            memSeed['phraseTypes'][phraseType] = {}
        #add OGgreetings
        for OGgreeting in self.OGgreetings:
            print(OGgreeting)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.addPhrase(OGgreeting, 'greetings', True)
        #plant seed
        self.saveMem(memSeed)
        self.loadMem()
        print('HAPPY BIRTHDAY!')
        print('')
        
    def loadMem(self):
        with open(self.MEM_PATH, 'rt') as csvfile:
            self.mem = {'data': 'null',
                        'phraseTypes':{'greetings':{},
                                       'statements':{}}}
            memReader = csv.DictReader(csvfile)
            for row in memReader:
                for phraseType, phraseDict in self.mem['phraseTypes'].items():
                   self.mem['phraseTypes'][phraseType][row[phraseType]] = row[phraseType+'Data'] 
   
    def saveMem(self, mem = testMem):
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
               
    
    
    def executeCommand(self, command):
        print('Executing Command:', command)
        if command == 'print memory':
            print('Printing memory...')
            print(self.mem)
        elif command == 'backup memory':
            pass
        elif command == 'end':
            self.endProgram = True
        elif command == 'test':
            print('testing...')
            print(self.mem['phraseTypes']['greetings']['hi TEEEEEEEEEEEEST!'])#['respList']
            print((self.mem['phraseTypes']['greetings']['hi TEEEEEEEEEEEEST!']) is dict)
        else:
            print('ERROR: executeCommand()')
              
    def formatPhrase(self, phrase):                    
        #get list of all sentances (uncapitalized)
        sentList = self.splitSents(phrase)
        #capitalize first letter of every sentance 
        capSentList = []
        for sent in sentList:
            capSentList.append(self.capSent(sent))  
        #put it all together into one phrase
        finalPhrase = ''
        for sent in capSentList:
            finalPhrase = finalPhrase + self.POST_SENT_SPACE + sent  
        #clean then return
        finalPhrase = finalPhrase.strip()
        return finalPhrase
        
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
        
    def correctlyPunctuated(self, phrase):
        for punc in self.PUNC_LIST:
            if phrase.endswith(punc) == True:
                return True
        return False
            
    def randFromDict(self, dict):
        key, val = random.choice(list(dict.items()))
        randDict = {'key': key,
                    'val': val}
        return randDict
        
    def getGreeting(self):#improve!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        randGreetDict = self.randFromDict(self.mem['phraseTypes']['greetings'])
        greeting = randGreetDict['key']
        return greeting
        
    def getResponse(self):#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.numResponses += 1
        return 'response'
    
    def getLast(self, list):
        lastItemPos = len(list) - 1
        lastItem = list[lastItemPos]
        return lastItem
        
    def logInteraction(self):
        #get input and output
        unFormattedInput = self.getLast(self.inList)
        input = self.formatPhrase(unFormattedInput)
        output = self.getLast(self.outList)
        
        #save input as valid response to output if not already
        outPhraseType = self.getPhraseType(output)
        if outPhraseType == 'greetings':
            #if self.mem['phraseTypes']['greetings'][output]['stats']['OG'] == True:#put bback in !!!!!!!!!!!!!!!!!
                #pass#how to deal with og greetings???????????????????????????????????
            pass
        #add input to output's respList if not already there
        if input not in self.mem['phraseTypes'][outPhraseType][output]['respList']:
            self.mem['phraseTypes'][outPhraseType][output]['respList'].append(input)
        
        #save input as new phrase if it doesnt already exists
        inPhraseType = self.getPhraseType(input)
        if input not in self.mem['phraseTypes'][inPhraseType]:
            self.addPhrase(self, input, inPhraseType)

        
        #if input not in 
        
    def addPhrase(self, phrase, phraseType, OGgreeting = False):
        if OGgreeting == False:
            self.mem['phraseTypes'][phraseType][phrase] = self.phraseDataShell
            self.mem['phraseTypes'][phraseType][phrase]['stats'] = {'OGgreeting': True}
        else:
            pass#how to deal with OGgreetings????????????????????????????????????????
        
        
    def getPhraseType(self, phrase):
        if phrase in self.mem['phraseTypes']['greetings']:
            return 'greetings'
        else:
            for phraseType, punc in self.phraseTypePuncDict.items():
                if phraseType != 'greeting':
                    if phrase.endswith(punc) == True:
                        return phraseType
                else:
                    pass #put an error here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
    def isGreeting(self, phrase):#if you never use this again just pput it in getPhraseType#NEED???????????
        for curPhrase, phraseData in self.mem['phraseTypes']['greetings']:
            if curPhrase == phrase:
                return True
        return False
            

 