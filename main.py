import pygame,os,sys,math,string
import dijkstra,display,potential_field,file_operation
from pygame.locals import *
MAX_COST=10086
BLOCK=3
FLAT=0
SOURCE=1
TARGET=2
TRIAL=4
WIN_WIDTH=1024
WIN_HEIGHT=768
DEFAULT_FRAME_WIDTH=50
BLACK=(0,0,0)
BLOCK_COLOR=(128,128,128)
FLAT_COLOR=(255,255,255)
SOURCE_COLOR=(0,255,255)
TARGET_COLOR=(0,0,255)
TRIAL_COLOR=(0,255,0)
FPS=120
def return_index(row,col,row_index,col_index):
    return row_index*col+col_index
def connectivity_detection_overflow_version(matrix,src_index,tar_index):
    row=len(matrix)
    col=len(matrix[0])
    if src_index==tar_index:
        return True
    s_row=src_index/col
    s_col=src_index%col
    t_row=tar_index/col
    t_col=tar_index%col
    checked_matrix=[]
    for i in range(row):
        temp_buffer=[]
        for j in range(col):
            temp_buffer.append(False)
        checked_matrix.append(temp_buffer)
    result_list=[]
    checked_matrix[s_row][s_col]=True
    if potential_field.in_range(row,col,s_row-1,s_col):
        s_index=return_index(row,col,s_row-1,s_col)
        if checked_matrix[s_row-1][s_col]==False:
            if connectivity_detection(matrix,s_index,tar_index):
                return True
    if potential_field.in_range(row,col,s_row-1,s_col+1):
        s_index=return_index(row,col,s_row-1,s_col+1)
        if checked_matrix[s_row-1][s_col+1]==False:
            if connectivity_detection(matrix,s_index,tar_index):
                return True
    if potential_field.in_range(row,col,s_row,s_col+1):
        s_index=return_index(row,col,s_row,s_col+1)
        if checked_matrix[s_row][s_col+1]==False:
            if connectivity_detection(matrix,s_index,tar_index):
                return True
    if potential_field.in_range(row,col,s_row+1,s_col+1):
        s_index=return_index(row,col,s_row+1,s_col+1)
        if checked_matrix[s_row+1][s_col+1]==False:
            if connectivity_detection(matrix,s_index,tar_index):
                return True
    if potential_field.in_range(row,col,s_row+1,s_col):
        s_index=return_index(row,col,s_row+1,s_col)
        if checked_matrix[s_row+1][s_col]==False:
            if connectivity_detection(matrix,s_index,tar_index):
                return True
    if potential_field.in_range(row,col,s_row+1,s_col-1):
        s_index=return_index(row,col,s_row+1,s_col-1)
        if checked_matrix[s_row+1][s_col-1]==False:
            if connectivity_detection(matrix,s_index,tar_index):
                return True
    if potential_field.in_range(row,col,s_row,s_col-1):
        s_index=return_index(row,col,s_row,s_col-1)
        if checked_matrix[s_row][s_col-1]==False:
            if connectivity_detection(matrix,s_index,tar_index):
                return True
    if potential_field.in_range(row,col,s_row-1,s_col-1):
        s_index=return_index(row,col,s_row-1,s_col-1)
        if checked_matrix[s_row-1][s_col-1]==False:
            if connectivity_detection(matrix,s_index,tar_index):
                return True

    return False

def main():
    screen=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    # about read tile information from file
    '''
    infile=open('readin.txt')
    row,col=[int(i) for i in infile.readline().split()]
    matrix=[]
    for i in range(row):
        matrix.append([int(part) for part in infile.readline().split()])

    tar_index=-1
    src_index=-1
    for i in range(row):
        for j in range(col):
            if(matrix[i][j]==TARGET):
                tar_index=i*col+j
            elif(matrix[i][j]==SOURCE):
                src_index=i*col+j
    '''

    # input manage
    '''
    row=input('Please enter the row number:')
    col=input('Please enter the col number:')
    matrix=[]
    trial=[]
    for i in range(row):
        temp_list=[]
        for j in range(col):
            temp_list.append(FLAT)
        matrix.append(temp_list)
    '''
    trial=[]
    matrix,row,col=file_operation.read_in_file('matrix_data.txt')

    start_x,start_y,tile_length=display.display_path(screen,matrix,row,col,trial)
#    dijkstra's code
#    link_data=dijkstra.build_link(matrix,row,col)
#    trial=dijkstra.dijkstra(link_data,row,col,src_index,tar_index)
#    potential_filed code
    clock=pygame.time.Clock()
    src_index=-1
    tar_index=-1
    while 1:
        clock.tick(FPS)
        events=pygame.event.get()

        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN\
                    and event.key == K_ESCAPE):
                break



        keystate=pygame.key.get_pressed()
        if keystate[K_ESCAPE]:
            file_operation.write_in_file('matrix_data.txt',matrix,row,col)
            break
        #accomplished the function of inputting tile information
        #press b to draw blocks
        #press s to draw source tile
        #press t to draw target tile
        #press RETURN to recalculate dijkstra
        if keystate[K_b]:
            x,y=pygame.mouse.get_pos()
            for i in range(row):
                for j in range(col):
                    if matrix[i][j]==TRIAL:
                        matrix[i][j]=FLAT
            tile_x,tile_y=display.get_tile_xy(start_x,start_y,row,col,tile_length,x,y)
            if matrix[tile_y][tile_x]==SOURCE or matrix[tile_y][tile_x]==TARGET:
                pass
            else:
                bianchang=7
                temp_row=tile_y-bianchang/2
                temp_col=tile_x-bianchang/2

                for i in range(bianchang):
                    for j in range(bianchang):
                        if potential_field.in_range(row,col,temp_row+i,temp_col+j):
                            matrix[temp_row+i][temp_col+j]=BLOCK
        if keystate[K_e]:
            x,y=pygame.mouse.get_pos()
            for i in range(row):
                for j in range(col):
                    if matrix[i][j]==TRIAL:
                        matrix[i][j]=FLAT
            tile_x,tile_y=display.get_tile_xy(start_x,start_y,row,col,tile_length,x,y)
            if matrix[tile_y][tile_x]==SOURCE or matrix[tile_y][tile_x]==TARGET:
                pass
            else:
                matrix[tile_y][tile_x]=FLAT
        if keystate[K_s]:#keep only one source
            x,y=pygame.mouse.get_pos()
            tile_x,tile_y=display.get_tile_xy(start_x,start_y,row,col,tile_length,x,y)
            for i in range(row):
                for j in range(col):
                    if matrix[i][j]==SOURCE or matrix[i][j]==TRIAL:
                        matrix[i][j]=FLAT
            matrix[tile_y][tile_x]=SOURCE
            src_index=tile_y*col+tile_x
        if keystate[K_t]:#keep only one target
            x,y=pygame.mouse.get_pos()
            tile_x,tile_y= display.get_tile_xy(start_x,start_y,row,col,tile_length,x,y)
            for i in range(row):
                for j in range(col):
                    if matrix[i][j]==TARGET or matrix[i][j]==TRIAL:
                        matrix[i][j]=FLAT
            matrix[tile_y][tile_x]=TARGET
            tar_index=tile_y*col+tile_x
        if keystate[K_RETURN]:
            # dijkstra code
            '''
            link_data=dijkstra.build_link(matrix,row,col)
            trial=dijkstra.dijkstra(link_data,row,col,src_index,tar_index)
            display.display_path(screen,matrix,row,col,trial)
            '''
            #file_operation.write_in_file('matrix_data.txt',matrix,row,col)
            if tar_index==-1 or src_index==-1:
                pass
            else:
                print 'over'
                potential_matrix=potential_field.cal_potential_field(matrix,row,col,tar_index)
                #potential_field.potential_field_path(matrix,potential_matrix,row,col,src_index,tar_index)
                clannad=src_index
                while src_index!=tar_index:
                    #print src_index
                    #raw_input()
                    matrix,src_index=potential_field.potential_field_step(matrix,potential_matrix,row,col,src_index,tar_index)
                    display.display_matrix(screen,matrix,row,col,start_x,start_y,tile_length)
                    pygame.display.flip()
                    for i in range(FPS/30):
                        clock.tick(FPS)
                src_index=clannad



        display.display_matrix(screen,matrix,row,col,start_x,start_y,tile_length)
        pygame.display.flip()

if __name__=='__main__': main()
