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
            
            
#==========================================================================================
#==========================================================================================
#
#   "PUBLIC"
#
#==========================================================================================
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

    def getGreeting(self):#improve!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        randGreetDict = self.randFromDict(self.mem['phraseTypes']['greetings'])
        greeting = randGreetDict['key']
        return greeting
        
        
    def getResponse(self):#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.numResponses += 1
        response = 'response: for some reason i cant add a new greeting without all OGgreetings becomming False'
        return response
        
        
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

            
    def logInteraction(self):
        #get input and output and related info
        unFormattedInput = self.getLast(self.inList)
        input = self.formatPhrase(unFormattedInput)
        output = self.getLast(self.outList)
        outPhraseType = self.getPhraseType(output)
        outOGgreetStat = self.mem['phraseTypes'][outPhraseType][output]['stats']['OGgreeting']
          
        print('before adding input to respList:' ,self.mem['phraseTypes']['greetings']['Hi!']['stats']['OGgreeting'])#!!!!!!!!!!
       
        
        #add input to output's respList if not already there
        if input not in self.mem['phraseTypes'][outPhraseType][output]['respList']:
            print('!!!!!!!!!!!!!!adding phrase to resplist of: ', output)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.mem['phraseTypes'][outPhraseType][output]['respList'].append(input)
            self.mem['phraseTypes'][outPhraseType][output]['respList'].append('TEEEST')#!!!!!!
            self.mem['phraseTypes']['greetings']['Hi!']['respList'].append('hiiiiiiiiiiiiii')#!!!!!!
            
        print('mem:', self.mem)#!@!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        print('after adding input to respList:', self.mem['phraseTypes']['greetings']['Hi!']['stats']['OGgreeting'])#!!!!!!!!!!!!!!
        
        #find inPhraseType 
        if outPhraseType == 'greetings' and outOGgreetStat == True:
            inPhraseType = 'greetings'
        else:
            inPhraseType = self.getPhraseType(input)
       
        print('before saving input as new phrase:', self.mem['phraseTypes']['greetings']['Hi!']['stats']['OGgreeting'])#!!!!!!!!!!!!!!  

       
        #save input as new phrase if it doesnt already exists
        if input not in self.mem['phraseTypes'][inPhraseType]:
            self.addPhrase(input, inPhraseType)
            
        #save to csv
        print('before saveing to csv:', self.mem['phraseTypes']['greetings']['Hi!']['stats']['OGgreeting'])#!!!!!!!!!!!!!!  
        self.saveMem(self.mem)
       
      

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
        with open(self.MEM_PATH, 'rt') as csvfile:
            self.mem = {'data': 'null',
                        'phraseTypes':{'greetings':{},
                                       'statements':{}}}
            memReader = csv.DictReader(csvfile)
            for row in memReader:
                for phraseType, phraseDict in self.mem['phraseTypes'].items():
                   #print('ALL THIS SHIT IS IN THE LOAD MEM FUNC, STILL HERE TO MAKE SURE dict-->str PROBLEM FIXED')#!!!
                   #print('phraseType:', phraseType)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                   #print("row[phraseType+'Data']```: ", row[phraseType+'Data'])#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                   #print("not row[phraseType+'Data'] == None: ", not row[phraseType+'Data'])#!!!!!!!!!!!
                   #dont do rest if empyt field - if things are going slow maybe make this tell upper loops not to check this phrasetype anymore?????????????
                   if not not row[phraseType+'Data']:
                       #convert string to dict
                       phraseDataStr = row[phraseType+'Data'] #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       phraseDataDict = ast.literal_eval(phraseDataStr)
                       #add phraseData to mem
                       self.mem['phraseTypes'][phraseType][row[phraseType]] = phraseDataDict
                       
    def saveMem(self, mem):#maybe go back at end and remove this var!!!!!!!!!!!!!!!!!!!!!!!!
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
        #self.loadMem()
        print('HAPPY BIRTHDAY!')
        print('')
        
        
    #OGgreeting should only be true if you are tyring to add a new OGgreeting
    def addPhrase(self, phrase, phraseType, OGgreeting = False):
        print ('IN addPhrase:')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print ('Adding phrase: ', phrase)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        

        
        
        
        
        
        
        

import brain

#current problem is that in memoryTEST.csv, phraseData is currently saved as a string,
#the problem is PROBABLY happening when you made the csv so probably something in saveMem,
#if the problem doesnt pop out, might as well finish everything you need to in order to save your,
#own original mem = finish buildNewMem() by adding all the stuff for OGgreetings


#test and make sure that you cant have a statment and greeting be the same / mess stuff up
#maybe add something so that a response to a phrase cant be the same as a phrase? maybe funny if dont do??
#maybe make a phrase class?
#get rid of the r in front of the MEMORY_PATH
home = r'C:\Users\Brandon\Documents\Personal Projects\chatbot\memoryTEST2.csv'
work = r'C:\Users\valleba\Documents\personal\chatbot\memoryTEST5.csv'

startUpPacket = {
                 'MEMORY_PATH': work,#C:\Users\valleba\Documents\personal\chatbot\memoryTEST.csv
                 'COMMAND_LIST': ['print memory','backup memory', 'end', 'test'],#belong here????????????
                 'PUNC_LIST': ['.','?','!'],
                 'PRE_CB_UI_STR': ' ',  #befor chatbot response
                 'POST_CB_UI_STR': '     :',  #after chatbot response  #rename!!!!!!!!!!!!!!
                 'POST_SENT_SPACE': '  ',  #num spaces after sentance
                 'OG_GREETINGS': ['Hi!', 'Howdy Partner!', 'Well hello there.']
                                                                                    }
#make chatbot                                            
chatbot = brain.Brain(startUpPacket)
# chatbot.buildNewMem()#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#greet user and get first response
#greeting = chatbot.getGreeting()
#inPhrase = input(greeting + chatbot.POST_CB_UI_STR)

contConvo = True

#start loop
while chatbot.endProgram == False:

    #form outPhrase
    if contConvo == True:
        if chatbot.numResponses == 0:
            outPhrase = chatbot.getGreeting()
        else:
            outPhrase = chatbot.getResponse()
    else:
        outPhrase = chatbot.getLast(chatbot.outList)
        
    #print and log output
    print(chatbot.PRE_CB_UI_STR + outPhrase)
    chatbot.outList.append(outPhrase)#put these 2 somewhere else  VVVV???????????????
    chatbot.numResponses += 1
    
    #get and log new inPhrase
    inPhrase = input(chatbot.POST_CB_UI_STR)
    chatbot.inList.append(inPhrase)
    
    contConvo = False

    #check input
    if inPhrase in chatbot.COMMAND_LIST:
        chatbot.executeCommand(inPhrase)
    elif chatbot.correctlyPunctuated(inPhrase) == False:
        print(chatbot.PRE_CB_UI_STR + 'Please use correct punctuation you uncultured swine!  Lets try that again.')
        #maybe make it print last response??????????????????????????????????????
    else:
        contConvo = True
        print('yay, legit input')
        cPhrase = chatbot.formatPhrase(inPhrase)
        print(cPhrase)
        
        chatbot.logInteraction()
        
    



#brain = cbFuncs.loadBrain(BRAIN_PATH)

#print(brain)
#cbFuncs.saveBrain(BRAIN_PATH)

#cbFuncs.makeNewBrain(BRAIN_PATH)

#cbFuncs.addPhrase(BRAIN_PATH)



 