import sys,math,pygame,dijkstra
from pygame.locals import *
from constants import *
def display_matrix(screen,matrix,row,col,start_x,start_y,length):
    for i in range(row):
        for j in range(col):
            pygame.draw.rect(screen,BLACK,[start_x+j*length,start_y+i*length,length-1,length-1],2)
            color=(0,0,0)
            if(matrix[i][j]==BLOCK):
                color=BLOCK_COLOR
            elif(matrix[i][j]==FLAT):
                color=FLAT_COLOR
            elif(matrix[i][j]==SOURCE):
                color=SOURCE_COLOR
            elif(matrix[i][j]==TARGET):
                color=TARGET_COLOR
            elif(matrix[i][j]==TRIAL):
                color=TRIAL_COLOR
            pygame.draw.rect(screen,color,[start_x+j*length,start_y+i*length,length-2,length-2])

def display_potential_field(screen,potential_matrix,row,col,start_x,start_y,length):
    for i in range(row):
        for j in range(col):
            pygame.draw.rect(screen,BLACK,[start_x+j*length,start_y+i*length,length-1,length-1],2)
            percent=potential_matrix[i][j]/MAX_COST
            color=(int(percent*255),int(percent*255),int(percent*255))
            print color
            pygame.draw.rect(screen,color,[start_x+j*length,start_y+i*length,length-2,length-2])


def display_path(screen,matrix,row,col,trial):
    width=WIN_WIDTH-2*DEFAULT_FRAME_WIDTH
    height=WIN_HEIGHT-2*DEFAULT_FRAME_WIDTH
    avg_len1=width/col
    avg_len2=height/row
    length=min(avg_len1,avg_len2)
    start_x=(WIN_WIDTH-length*col)/2
    start_y=(WIN_HEIGHT-length*row)/2
    for i in range(len(trial)-2):
        temp_y=trial[i+1]/col
        temp_x=trial[i+1]%col
        matrix[temp_y][temp_x]=TRIAL
    display_matrix(screen,matrix,row,col,start_x,start_y,length)
    return start_x,start_y,length


def get_tile_xy(start_x,start_y,row,col,length,x,y):
    tempx=(x-start_x)/length
    tempy=(y-start_y)/length
    if tempx<0:
        tempx=0
    elif tempx>=col:
        tempx=col-1
    if tempy<0:
        tempy=0
    elif tempy>=row:
        tempy=row-1
    return tempx,tempy
'''

        if keystate[K_UP]:
            position_up-=5
        if keystate[K_DOWN]:
            position_up+=5
        if keystate[K_LEFT]:
            position_left-=5
        if keystate[K_RIGHT]:
            position_left+=5
        screen.fill(BLACK)
        screen.blit(image,(position_left,position_up))
        pygame.display.flip()'''
