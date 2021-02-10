import time
import enchant
import re
from WordCount import Word_Count

Test_Phrase = """At three o’clock precisely I was at Baker Street, but Holmes had not
yet returned. The landlady informed me that he had left the house
shortly after eight o’clock in the morning. I sat down beside the
fire, however, with the intention of awaiting him, however long he
might be. I was already deeply interested in his inquiry, for, though
it was surrounded by none of the grim and strange features which
were associated with the two crimes which I have already recorded,
still, the nature of the case and the exalted station of his client
gave it a character of its own. Indeed, apart from the nature of the
investigation which my friend had on hand, there was something in his
masterly grasp of a situation, and his keen, incisive reasoning, which
made it a pleasure to me to study his system of work, and to follow the
quick, subtle methods by which he disentangled the most inextricable
mysteries. So accustomed was I to his invariable success that the very
possibility of his failing had ceased to enter into my head."""

print("Hello! This is a test of your typing speed.")
User_Response = input("Are you ready?")
if User_Response == "":
    print("All right! Here we go!")
    print("Type the following the text and press enter when you are done:")
    print("******SAMPLE TEXT FOR TYPING SPEED TEXT*****")
    print(Test_Phrase)
    print("******SAMPLE TEXT FOR TYPING SPEED TEXT*****")
    Time_Start = input("Your time will start when you press Enter....")
    T_Start = time.time()
    User_Phrase = input("Timer Started. Press Enter at any point to stop the timer.")
    T_End = time.time()
    print("Calculating...Hold Tight!")
    T_Total = round((T_End - T_Start),1)
    User_Char_Count = len(User_Phrase)
    User_Typing_Speed = round(((User_Char_Count/5)/T_Total),1)*60
    User_Words = Word_Count(User_Phrase)
    ErrCheck = enchant.Dict("en_US")
    Errs = 0
    for word in User_Words:
        WordCheck = ErrCheck.check(word)
        if not WordCheck:
            Errs += 1
    User_Typing_Speed_Corrected = User_Typing_Speed - Errs
    print(f'You typed at {User_Typing_Speed_Corrected} WPM (Words Per Minute).\nYou made {Errs} mistakes.')

