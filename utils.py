import numpy as np

def get_distance(pos_1,pos_2,torus,width,height):

    x1, y1 = pos_1
    x2, y2 = pos_2

    dx = np.abs(x1 - x2)
    dy = np.abs(y1 - y2)

    if torus:
        dx = min(dx, width - dx)
        dy = min(dy, height - dy)

    return np.sqrt(dx * dx + dy * dy) 

def get_direction(pos_1,pos_2,width,height):

    x1, y1 = pos_1
    x2, y2 = pos_2

    if x1!=x2:
      dx = (x2-x1)/np.abs(x2 - x1)
    else:
      dx=0

    if y1!=y2:
      dy = (y2-y1)/np.abs(y2 - y1)
    else:
      dy=0

    new_direction=(dx,dy)
    distance=get_distance(pos_1,pos_2,False,width,height)
    toroidal_distance=get_distance(pos_1,pos_2,True,width,height)

    if distance>toroidal_distance:
        new_direction=(-dx,-dy)

    dx,dy=new_direction
    new_direction=(int(dx),int(dy))  #converte gli indici da float a interi

    return new_direction

def calculate_resulting_dir(dir_1,dir_2):  #la dir_2 al massimo può solo deviare la dir_1
    resulting_dir=dir_1

    if dir_1==(0,1):
        if dir_2 in ((-1,-1),(0,-1),(-1,0)):
            resulting_dir=(-1,0)
        elif dir_2 in ((1,0),(1,-1)):
            resulting_dir=(1,1)
    
    if dir_1==(1,1):
        if dir_2 in ((-1,1),(-1,0),(-1,-1)):
            resulting_dir=(0,1)
        elif dir_2 in ((0,-1),(1,-1)):
            resulting_dir=(1,0)

    if dir_1==(1,0):
        if dir_2 in ((-1,1),(-1,0),(0,1)):
            resulting_dir=(1,1)
        elif dir_2 in ((-1,0),(1,-1)):
            resulting_dir=(1,-1)

    if dir_1==(1,-1):
        if dir_2 in ((-1,1),(-1,0),(-1,-1)):
            resulting_dir=(0,-1)
        elif dir_2 in ((0,1),(1,1)):
            resulting_dir=(1,0)

    if dir_1==(0,-1):
        if dir_2 in ((-1,1),(-1,0),(0,1)):
            resulting_dir=(-1,-1)
        elif dir_2 in ((1,0),(1,1)):
            resulting_dir=(1,-1)

    if dir_1==(-1,-1):
        if dir_2 in ((-1,1),(0,1),(1,1)):
            resulting_dir=(-1,0)
        elif dir_2 in ((1,0),(1,-1)):
            resulting_dir=(0,-1)

    if dir_1==(-1,0):
        if dir_2 in ((0,1),(1,1),(1,0)):
            resulting_dir=(-1,1)
        elif dir_2 in ((0,-1),(1,-1)):
            resulting_dir=(-1,-1)

    if dir_1==(-1,1):
        if dir_2 in ((1,1),(1,0),(1,-1)):
            resulting_dir=(0,1)
        elif dir_2 in ((0,-1),(-1,-1)):
            resulting_dir=(-1,0)
            
    return resulting_dir

