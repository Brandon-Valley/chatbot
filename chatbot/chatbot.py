
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
work = r'C:\Users\valleba\Documents\personal\chatbot\memoryTEST6.csv'

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

