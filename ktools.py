# ktools: KiCad tools
# rev 1 - shabaz - first version

# usage:
# From KiCad PCB Editor, go to Tools->Scripting Console
# From the scripting console, select File->Open and select this file

import pcbnew
import csv 

def welcome():
    print("Welcome to ktools v0.1")

# tLists all footprint references, and the component value and co-ordinates
# if format is "python" then a Python script is generated to move footprints to the current co-ordinates
def list_coords(format = ""):
    brd = pcbnew.GetBoard()
    fp_list = brd.GetFootprints()
    csvData = []        # list of save to csv file
    python_code = ""    # string of python code to move footprints

    if format == "python":
        python_code += "import pcbnew\n"
        python_code += "brd = pcbnew.GetBoard()\n"
        python_code += "def move_items():\n"

    for fp in fp_list:
        vect = fp.GetPosition()
        orient = fp.GetOrientation()
        if format == "":
            csvData.append([fp.GetReference(), fp.GetValue(), vect.x/1e6, vect.y/1e6, orient.AsDegrees()])
            print(f"{fp.GetReference()},{fp.GetValue()},{vect.x/1e6},{vect.y/1e6},{orient.AsDegrees()}")
        elif format == "python":
            print(f'    fx = brd.FindFootprintByReference("{fp.GetReference()}")')
            python_code += f'    fx = brd.FindFootprintByReference("{fp.GetReference()}")\n'
            python_code += "    if fx is not None:\n"
            python_code += f'        fx.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPoint({vect.x}, {vect.y})))\n'
            python_code += f'        fx.SetOrientation(pcbnew.EDA_ANGLE({orient.AsDegrees()}, pcbnew.DEGREES_T))\n'

    if format == "python":
        python_code += '    pcbnew.Refresh()\n'
        # write to move_items.py in user home directory
        with open('move_items.py', 'w', newline='') as pyfile:
            pyfile.write(python_code)
        
    else:
        # write to csv file, in user home directory
        with open('coords.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csvData)


if __name__ == '__main__':
    welcome()
    list_coords()
    list_coords("python")
