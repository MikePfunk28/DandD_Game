import json

MOON_ASCII = """
       _.-'''-._
     .'   .-'``|'.
    /    /    -*- \\
   ;   <{      |   ;
   |    _\\ |       | 
   ;   _\\ -*- |    ;
    \\   \\  | -*-  /
    '._ '.__ |_.'
        '-----'

       ----------------------------------
      |        June, 20th, 1969          |
      |  Here Men from the Planet Earth  |
      |   First set Foot upon the Moon   |
      | We came in Peace for all Mankind |
       ----------------------------------
"""


def display_moon_landing():
    """Display moon landing ASCII art and message."""
    print(MOON_ASCII)
    input("Press Enter to continue...")


def get_questions():
    """Retrieve questions from a JSON file."""
    with open("nimc/notinmycloud/questions[0].json", "r", encoding="utf-8", errors="replace") as f:
        return json.load(fp=f)


def get_options():
    """Retrieve options from a JSON file."""
    with open("nimc/notinmycloud/options[0].json", "r", encoding="utf-8", errors="replace") as f:
        return json.load(f)

def get_answer():
    """Retrieve questions from a JSON file."""
    with open("nimc/notinmycloud/questions[0].json", "r", encoding="utf-8", errors="replace") as f:
        return json.load(fp=f)["answer"]

questions = get_questions()
options = get_options()

def start_interview():
    """Start the game's opening scene."""
    display_moon_landing()
    print("What is the difference between Continuous Delivery and Continuous Deployment?")
    for q in questions[:3]:
        print(f"\n{q['question']}")
        for i, option in enumerate(q["options"], start=1):
            print(f"{i}. {option}")
        user_answer = input("Choose the correct option (1-4): ")
        if q["options"][int(user_answer) - 1] == q["answer"]:
            print("Correct!")
        else:
            print("Incorrect! Try again.")
            return False
    print("Congratulations! You're hired.")
    return True

myquestions = get_questions()
print(myquestions[0]["question"])
print(myquestions[0]["options"])
print(myquestions[0]["answer"])