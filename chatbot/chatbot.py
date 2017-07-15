#test
import brain

#current problem is that in memoryTEST.csv, phraseData is currently saved as a string,
#the problem is PROBABLY happening when you made the csv so probably something in saveMem,
#if the problem doesnt pop out, might as well finish everything you need to in order to save your,
#own original mem = finish buildNewMem() by adding all the stuff for OGgreetings


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
                 'UI_NUM_SPACES_BEFORE_OUTPUT': 1,  #befor chatbot response 
                 'UI_LINE_LENGTH': 15,
                 'UI_NUM_SPACES_BEFORE_INPUT': 'built below' ,  #before user input
                 'UI_INPUT_PROMT_SYMBOL': ':',
                 'POST_SENT_SPACE': '  ',  #num spaces after sentance
                 'OG_GREETINGS': ['Hi!', 'Howdy Partner!', 'Well hello there.']
                                                                                    }
numSpacesBeforeInput = (startUpPacket['UI_NUM_SPACES_BEFORE_OUTPUT'] * 2) + startUpPacket['UI_LINE_LENGTH']
startUpPacket['UI_NUM_SPACES_BEFORE_INPUT'] = numSpacesBeforeInput

#make chatbot                                            
chatbot = brain.Brain(startUpPacket)
# chatbot.buildNewMem()#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#greet user and get first response
#greeting = chatbot.getGreeting()
#inPhrase = input(greeting + chatbot.UI_NUM_SPACES_BEFORE_INPUT)

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
    #print(chatbot.UI_NUM_SPACES_BEFORE_OUTPUT + outPhrase)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    chatbot.output(outPhrase)

    #get and log new inPhrase
    inPhrase = chatbot.getInput()
    
    contConvo = False

    #check input
    if inPhrase in chatbot.COMMAND_LIST:
        chatbot.executeCommand(inPhrase)
    elif chatbot.correctlyPunctuated(inPhrase) == False:
        print(chatbot.UI_NUM_SPACES_BEFORE_OUTPUT + 'Please use correct punctuation you uncultured swine!  Lets try that again.')
        #maybe make it print last response??????????????????????????????????????
    else:
        contConvo = True
#         print('yay, legit input')
#         cPhrase = chatbot.formatPhrase(inPhrase)
#         print(cPhrase)
        
        chatbot.logInteraction()
        
    





