from pathlib import Path
import pandas as  pd


def initial_setup():
    file = Path("data.xlsx")
    if file.exists():
        return True
    else:
        data = pd.DataFrame({'LAST NAME':[],'FIRST NAME':[],'ID':[],'Comments':[]})
        writer = pd.ExcelWriter('data.xlsx')
        data.to_excel(writer,'Data', index = False)
        writer.save()

def add():
    print('added')

def remove():
    print('removed')

def charge():
    print('charged')
