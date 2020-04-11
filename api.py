from pathlib import Path
import pandas as pd
from openpyxl import load_workbook
import xlrd
import openpyxl


def initial_setup():
    file = Path("data.xlsx")
    if file.exists():
        return True
    else:
        data = pd.DataFrame({'LAST NAME':[],'FIRST NAME':[],'ID':[],'Comments':[],'Amount Due':[]})
        writer = pd.ExcelWriter('data.xlsx')
        data.to_excel(writer,'Data', index = False)
        writer.save()

def generate_ID(reader):
    if len(reader) == 0:
        ID_number = 123456
        return ID_number
    else:
        book = xlrd.open_workbook('Data.xlsx')
        sheet = book.sheet_by_index(0)
        ID_number = sheet.cell_value(len(reader),2) + 1
        return ID_number

#################3 Add, Remove, and Charge Functions ##########################
def add():
    last_name = input('Last Name: ')
    first_name = input('First Name: ')

    #add to excel sheet
    book = load_workbook('data.xlsx')
    writer = pd.ExcelWriter('data.xlsx', engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}  # iterates through book.worksheets to make dictionary
    reader = pd.read_excel(r'data.xlsx')    # read file (used in next line for length)

    ID_number = generate_ID(reader)
    print('')
    print('The Patient has been added:\nThe ID number for %s, %s is %d' % (last_name,first_name,ID_number))

    comment = input('Do you have any comments to add about this patient? ')

    new_patient = pd.DataFrame({'LAST NAME':[last_name],'FIRST NAME':[first_name],'ID':[ID_number],'Comments':[comment],'Amount Due':[0]})
    new_patient.to_excel(writer,sheet_name = 'Data',index = False, header = False, startrow=len(reader)+1)
    writer.save()


def remove():
    creds = info()
    data = pd.read_excel(r'data.xlsx')
    writer = pd.ExcelWriter('data.xlsx')
    wb = xlrd.open_workbook('data.xlsx')
    sheet = wb.sheet_by_index(0)

    # ID given
    if creds[1] == None:
        data2 = data[~data['ID'].isin([str(creds[0])])]
        data2.to_excel(writer,sheet_name = 'Data',index = False)
        writer.save()

    # name given
    else: #finds if both names belong to same row, then gets ID_number
        for x in range(1,len(data)+1):
            if sheet.cell_value(x, 0) == creds[0] and sheet.cell_value(x, 1)== creds[1]:
                ID_number = sheet.cell_value(x,2)
                data2 = data[~data['ID'].isin([ID_number])]
                data2.to_excel(writer,sheet_name = 'Data',index = False)
                writer.save()


    print('removed')

def charge():
    creds= info()
    data = pd.read_excel(r'data.xlsx')
    writer = pd.ExcelWriter('data.xlsx')
    wb = xlrd.open_workbook('data.xlsx')
    sheet = wb.sheet_by_index(0)

    # ID given
    if creds[1] == None:
        for x in range(1,len(data)+1):
            if sheet.cell_value(x, 2) == int(creds[0]):
                print('good')
                # add on new value to old amount
                amount = sheet.cell_value(x,4)
                amount += int(input('Charge amount (USD): '))
                data.at[x-1,'Amount Due'] = amount

                data.to_excel(writer,sheet_name = 'Data',index = False)
                writer.save()


    # name given
    else:
        for x in range(1,len(data)+1):
            if sheet.cell_value(x, 0) == creds[0] and sheet.cell_value(x, 1)== creds[1]:

                # add on new value to old amount
                amount = sheet.cell_value(x,4)
                amount += int(input('Charge amount (USD): '))
                data.at[x-1,'Amount Due'] = amount

                # update_patient = pd.DataFrame({'LAST NAME':[sheet.cell_value(x, 0)],'FIRST NAME':[sheet.cell_value(x, 1)],'ID':[sheet.cell_value(x, 2)],'Comments':[sheet.cell_value(x, 3)],'Amount Due':[amount]})
                data.to_excel(writer,sheet_name = 'Data',index = False)
                writer.save()

    print('charged')
###############################################################################
def info():
    print("")
    choice = input('Would you like to search by name or ID?: ')
    if choice == 'name' or choice == "Name":
        last_name = input('Last Name: ')
        first_name = input('First Name: ')
        return [last_name,first_name]
    elif choice == 'id' or choice == "ID":
        ID_number = input('ID_number: ')
        return [ID_number, None]
    else:
        print("Please select a valid option")
        info()
