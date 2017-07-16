import brain

#test and make sure that you cant have a statment and greeting be the same / mess stuff up
#maybe add something so that a response to a phrase cant be the same as a phrase? maybe funny if dont do??
#maybe make a phrase class?
#get rid of the r in front of the MEMORY_PATH
#make print mem cleaner/actually usable
#add undo/edit mem commands
home = r'C:\Users\Brandon\Documents\Personal Projects\chatbot\memoryTEST8.csv'
work = r'C:\Users\valleba\Documents\personal\chatbot\memoryTEST6.csv'

startUpPacket = {
                 'MEMORY_PATH': home,#C:\Users\valleba\Documents\personal\chatbot\memoryTEST.csv
                 'COMMAND_LIST': ['print memory','backup memory', 'end', 'test'],#belong here????????????
                 'PUNC_LIST': ['.','?','!'],
                 'OG_GREETINGS': ['Hi!', 'Howdy Partner!', 'Well hello there.'],
                 
                 'UI_NUM_SPACES_BEFORE_OUTPUT': 1,  #befor chatbot response 
                 'UI_LINE_LENGTH': 25,
                 'UI_NUM_SPACES_BEFORE_INPUT': 'built below' ,  #before user input
                 'UI_INPUT_PROMT_SYMBOL': ':'
                                                                                    }
numSpacesBeforeInput = startUpPacket['UI_NUM_SPACES_BEFORE_OUTPUT'] + startUpPacket['UI_LINE_LENGTH'] + 1
startUpPacket['UI_NUM_SPACES_BEFORE_INPUT'] = numSpacesBeforeInput

#make chatbot                                            
chatbot = brain.Brain(startUpPacket)

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
    chatbot.output(outPhrase)

    #get and log new inPhrase
    inPhrase = chatbot.getInput()
    
    contConvo = False

    #check input
    if inPhrase in chatbot.COMMAND_LIST:
        chatbot.executeCommand(inPhrase)
    elif chatbot.correctlyPunctuated(inPhrase) == False:
        chatbot.scold('incorect punctuation')
        
    else:
        contConvo = True
#         print('yay, legit input')
#         cPhrase = chatbot.formatPhrase(inPhrase)
#         chatbot.fancyPrint(inPhrase, 1)
        
        chatbot.logInteraction()
        
    





