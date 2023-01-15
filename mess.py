# Ciupageanu Roland
# Project name : mess (a program that formats temperature measurements in excel format)
# Interface made using PySimpleGui
# Imported modules: mess_import_0, module/ class used for temperature measurements

import PySimpleGUI as sg
import pandas as pd
import numpy as np
import sys
import os

# Using this os.getcwd we can insert into a variable the path in which the program is located
working_directory = os.getcwd()


# This function will help us on saving the file
# The function will be used for saving the file name in all the modules(present only 1) that use excel files
def path_to_file(file_path):
    file_path_list = file_path.split("/")
    file = file_path_list[-1]
    return file

# Variable used to for showing messages
message = "Empty message"

# Variable used as a marker, in order to mark the name of the new/ modified files
marker = "$$$"

# Variable that will modify in order to show the working module
module = 0

sg.theme('Black') 

layout = [[sg.FileBrowse(initial_folder = working_directory, file_types = [("XLSX Files", "*.xlsx")]), sg.InputText(key = "-FILE_PATH-")],
          [sg.Button("Process Mess"),sg.Button("New module")],
          [sg.Exit()],
          [sg.Multiline(size=(50,10),key ="-ML-")]]

window = sg.Window('Ciupageanu Roland - Mess program', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    if event == "Process Mess":
        module = "You are currently working in the Temperature measurement module!"

        # Here we will store the path that we chosed
        xl_file = values["-FILE_PATH-"]

        # We are making a dataframe out of the file from the path FILE_PATH from the variable "xl_file" (our excel file)
        measurements = pd.read_excel(xl_file)

        # We import the Mess module, we create an object from the "big" table dataframe(where are the measurements)
        from mess_import_0 import Mess
        big_table = Mess(measurements)
        
        # We apply the first method process1, defined in the mess module (mess_import_0)
        big_table.process1()

        # Some important variables that are used trough the module/ program
        # Column number for the last point (We can acces trough: object.attribute.column)
        last_point = (len(big_table.df.columns))-1

        # Number if measurement points
        nr_points = len(big_table.df.columns[2:])

        # Number of measurements
        nr_mes = 0
        
        # Search in col 0, from line 1:
        for x in big_table.df.iloc[1:,0]:
            if x != 0:
                nr_mes += 1
        
        # We apply the process2 method on the big_table object, where we use the last_point attribute
        big_table.process2(last_point)

        # We create another object, small_table, in which the maximum values vill stay
        # A static method was used (we call this method by class.method)
        small_table = Mess(Mess.procesare3(big_table.df,nr_mes,nr_points,last_point))

        # Saving the file: saving with new name, in two sheets (created after the objects big_table and small_table)
        with pd.ExcelWriter("$$$" + path_to_file(xl_file)) as writer:
            big_table.df.to_excel(writer, sheet_name = "Temperatures",index = False)
            small_table.df.to_excel(writer, sheet_name = "Maxim", index = False)

        print("Successful processing! Check the file:", marker + path_to_file(xl_file))
        message = f"{module}\nSuccessful processing! Check the file {marker + path_to_file(xl_file)}"
        
        if Mess.alarm == 1:
            print("Attention! You have maximum values >70!")
            print("Replace manually!")  
            message += "\nAttention! You have maximum values >70!\nReplace manually" 
            
        # Update window (with variable message) after KEY -ML- , previously mapped in layout/ sg.multiline
        window["-ML-"].update(message)  

window.close()
