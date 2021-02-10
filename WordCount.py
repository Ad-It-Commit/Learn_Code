import re

def Word_Count(Search_In):
    Search_Pat = Search_In.lower()
    Search_Pat_Original = Search_In
    Split = re.compile(r"\w+",flags=re.I)
    Split_Strings = Split.findall(Search_Pat)
    Split_Strings_Original = Split.findall(Search_Pat_Original)
    WordCount_Analyzed = len(Split_Strings)
    #WordCount_Raw = len(Split_Strings_Original)
    return Split_Strings_Original
