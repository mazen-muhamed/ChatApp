import re
from typing import Optional

AutoReplyRules = [
    {
        "keywords" : ["Hello", "Hi", "Hey", "ahlan", "Greetings"],
        "reply" : "Hello! iam AI Bot How can i assist you today?"
    },
    {
        "keywords" : ["help", "support", "issue", "problem"],
        "reply" : "I see you need assistance. Please describe your issue in more detail. "
    },
    {
        "keywords" : ["thank you", "thanks", "appreciate"],
        "reply" : "You're welcome!"
    },
    {
        "keywords" : ["are you human", "human", "How old are you", "What are you doing"],
        "reply" : "Iam just an AI bot, iam here to assist you if you have any questions you can ask and i will try me best"
    },
]

def findBestAnswers(message: str)->Optional[str]:
    lower_msg = message.lower().strip()
    for rule in AutoReplyRules:
        for keyword in rule["keywords"]:
            if keyword in lower_msg:
                return rule["reply"]
    return None

## Default Reply if no keyword matches..
def fallBackResponse()->str:
    pass