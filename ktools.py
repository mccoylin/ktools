# ktools: KiCad tools
# rev 1 - shabaz - first version

# usage:
# From KiCad PCB Editor, go to Tools->Scripting Console
# From the scripting console, select File->Open and select this file
# run the script
# >>> exec(open('/path/scripting.py').read())

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
            csvData.append([fp.GetReference(), fp.GetValue(), vect.x/pcbnew.IU, vect.y/pcbnew.pcbIUScale.IU_PER_MM, orient.AsDegrees(), fp.GetLayerName()])
            print(f"{fp.GetReference()},{fp.GetValue()},{vect.x/pcbnew.pcbIUScale.IU_PER_MM},{vect.y/pcbnew.pcbIUScale.IU_PER_MM},{orient.AsDegrees()},{fp.GetLayerName()}")
        elif format == "python":
            print(f'    fx = brd.FindFootprintByReference("{fp.GetReference()}")')
            python_code += f'    fx = brd.FindFootprintByReference("{fp.GetReference()}")\n'
            python_code += f'    if fx is not None:\n'
            python_code += f'        fx.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPoint({vect.x}, {vect.y})))\n'
            python_code += f'        fx.SetOrientation(pcbnew.EDA_ANGLE({orient.AsDegrees()}, pcbnew.DEGREES_T))\n'
            #python_code += f'        layer = brd.GetLayerID("{fp.GetLayerName()}")\n'
            #python_code += f'        fx.SetLayer(self, layer)\n'


    if format == "python":
        python_code += '    pcbnew.Refresh()\n'
        python_code += f'\n'
        python_code += f'\n'
        python_code += f"if __name__ == '__main__':\n"
        python_code += f'    move_items()\n'
        # write to move_items.py in user home directory
        with open('move_items.py', 'w', newline='') as pyfile:
            pyfile.write(python_code)
        
    else:
        # write to csv file, in user home directory
        with open('coords.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csvData)


# get_board_outline: prints the board outline dimensions
def get_board_outline():
    bnds = []
    board = pcbnew.GetBoard()
    edge_cuts = board.GetLayerID("Edge.Cuts")
    outline = board.GetDrawings()
    for draw in outline:
        if draw.GetLayer() == edge_cuts:
            bnds.append(draw)
    
    # print length of bnds list
    print(f"Number of board outline segments: {len(bnds)}") 
    # save the bnds list to a file
    with open('board_outline.txt', 'w', newline='') as txtfile:
        for draw in bnds:
            txtfile.write(f"{draw.GetStart().x/pcbnew.pcbIUScale.IU_PER_MM},{draw.GetStart().y/pcbnew.pcbIUScale.IU_PER_MM},{draw.GetEnd().x/pcbnew.pcbIUScale.IU_PER_MM},{draw.GetEnd().y/pcbnew.pcbIUScale.IU_PER_MM}\n") 

    # draw the board outline
    outline = pcbnew.PCB_SHAPE(board)
    for draw in bnds:
        outline.SetShape(draw.GetShape())   

            



    #board = pcbnew.GetBoard()
    #board.Drawings().Clear()
    #for draw in bnds:
    #    board.Add(draw)
    #pcbnew.Refresh()


            


    '''
    # move_outline: moves the board outline to the current co-ordinates
    board.Drawings().Clear()
    for draw in bnds:
        board.Add(draw)
    pcbnew.Refresh()
    '''


def get_tracks(format = ''):
    board = pcbnew.GetBoard()
    tracks = board.GetTracks()

    if format == "python":
        # save to python code
        python_code = ""
        python_code += "import pcbnew\n\n"
        python_code += "brd = pcbnew.GetBoard()\n"
        python_code += "def move_tracks():\n"
        for track in tracks:
            print(track.GetStart(), track.GetLayer())
            python_code += f'    track = pcbnew.PCB_TRACK(brd)\n'
            python_code += f'    track.SetStart(pcbnew.VECTOR2I(pcbnew.wxPoint({track.GetStart().x}, {track.GetStart().y})))\n'
            python_code += f'    track.SetEnd(pcbnew.VECTOR2I(pcbnew.wxPoint({track.GetEnd().x}, {track.GetEnd().y})))\n'
            python_code += f'    track.SetWidth({track.GetWidth()})\n'
            python_code += f'    track.SetLayer({track.GetLayer()})\n'
            python_code += f'    brd.Add(track)\n'

        python_code += f'    pcbnew.Refresh()\n'
        python_code += f'\n'
        python_code += f'\n'
        python_code += f"if __name__ == '__main__':\n"
        python_code += f'    move_tracks()\n'
        # write to move_items.py in user home directory
        with open('move_tracks.py', 'w', newline='') as pyfile:
            pyfile.write(python_code)




if __name__ == '__main__':
    welcome()
    #list_coords()
    #list_coords("python")

    #get_board_outline()
    get_tracks('python')
    