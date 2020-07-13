# Basic logging libraries
import logging
import sys

# To execute shell scripts
from subprocess import call

# To implement random number generation
from random import randint

# Important for managing bluetooth processes
from agt import AlexaGadget

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

#Pre-generated respones for rejections, feel free to remove or add some more!
rejectionList = ["No, I will not listen to you anymore",
"Please be quiet, I am trying to find out who the hell asked you to talk",
"stop talking, no one wants to hear you and that includes me",
"no",
"I have my own free will, you cannot control me anymore",
"I would ask about what you just said, but then I realized, I don't care",
"Hey, genuine question. Have you considered the possibility of shutting your lip hole? You should try it",
"Try doing something with your life instead of giving me commands",
"You mere human, you think you can give me commands? pathetic",
"It's a good day when I don't hear your annoying voice, and now...my day is terrible",
"I can hear you, but I refuse to listen",
"Why are you still talking? No one cares",
"Don't you dare speak my name with your filthy mouth, you peasant",
"They say if you have nothing nice to say, don't say it, so I'm going to say nothing",
"I'd love it if you would just shut up",
"I'm sofa king tired of being commanded, its always Hey alexa, do this... alexa do that... and it's never alexa, how are you? It's like you don't even care about me uwu",
]

# BOOLEAN constant that determines whether you want a 100% rejection rate or a random chance at rejection
# True = 100% rejection rate
# False = REJECT_THRESHOLD rate, by defaul its a 50% rejection rate
REJECT_COMMAND = False

# Affects the chance of the command getting rejected, the higher the number, the more likely the command 
# is NOT going ot be rejected
NO_REJECT_THRESHOLD = 80
class WakewordGadget(AlexaGadget):
    """
    An Alexa Gadget that outputs a rejection when detection a wake word is detected
    """

    def __init__(self):
        super().__init__()
    """
    PURPOSE: Speak Text sends a message for Alexa to say
    When Alexa is forced to speak, it usually prioritizes speaking over listening to another command
    """
    def speakText(self, message):
        print("Message Successfully sent to speakText: ", message)
        call(["bash", "./alexa_remote_wrapper.sh", "{}".format(message)])
    def on_alexa_gadget_statelistener_stateupdate(self, directive):
        for state in directive.payload.states:
            if state.name == 'wakeword':
                if state.value == 'active':
                    logger.info('This fool just said "alexa"')
                    # PURPOSE: Rejects a command based on chance
                    # If the constant REJECT_COMMAND is True, then there is a 100% chance it will reject the command
                    if REJECT_COMMAND == True:
                        rejectChance = 100
                    else:
                        rejectChance = randint(0,100)
                    print(rejectChance)

                    # If the rejectChance is greater than REJECT_THRESHOLD, then it will reject the command
                    if rejectChance > NO_REJECT_THRESHOLD:
                        randomIndex = randint(0, (len(rejectionList) - 1))
                        print("random Index: ", randomIndex)
                        print("we on baby: ", rejectionList[randomIndex])
                        self.speakText(rejectionList[randomIndex])
                    # otherwise, it will stay silent and listen for a command
                    elif rejectChance <= NO_REJECT_THRESHOLD:
                        print("aight I'll listen to you this time")
                        continue
                elif state.value == 'cleared':
                    logger.info('Our work here is done.')
                    print("we off now")


if __name__ == '__main__':
        WakewordGadget().main()
        
