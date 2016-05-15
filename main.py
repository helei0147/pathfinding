import pygame,os,sys,math,string
import dijkstra,display,potential_field,file_operation
from pygame.locals import *
from astar import *
from constants import *
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
    pygame.init()
    screen=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
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
    pathfinding_mode=['A* Algorithm','Potential Field Algorithm','Combination']
    current_mode_index=2
    if pygame.font:
        myfont=pygame.font.Font(None,36)
    unchanged_src=0
    unchanged_tar=1
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
                bianchang=col//15
                temp_row=tile_y-bianchang/2
                temp_col=tile_x-bianchang/2

                for i in range(bianchang):
                    for j in range(bianchang):
                        if potential_field.in_range(row,col,temp_row+i,temp_col+j):
                            matrix[temp_row+i][temp_col+j]=BLOCK
        if keystate[K_c]:
            current_mode_index+=1
            current_mode_index=current_mode_index%len(pathfinding_mode)
            for i in range(row):
                for j in range(col):
                    if matrix[i][j]==TRIAL:
                        matrix[i][j]=FLAT
            matrix[unchanged_src//col][unchanged_src%col]=SOURCE
            matrix[unchanged_tar//col][unchanged_tar%col]=TARGET
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
                bianchang=col//10
                temp_row=tile_y-bianchang/2
                temp_col=tile_x-bianchang/2

                for i in range(bianchang):
                    for j in range(bianchang):
                        if potential_field.in_range(row,col,temp_row+i,temp_col+j):
                            matrix[temp_row+i][temp_col+j]=FLAT
        if keystate[K_s]:#keep only one source
            x,y=pygame.mouse.get_pos()
            tile_x,tile_y=display.get_tile_xy(start_x,start_y,row,col,tile_length,x,y)
            for i in range(row):
                for j in range(col):
                    if matrix[i][j]==SOURCE or matrix[i][j]==TRIAL:
                        matrix[i][j]=FLAT
            matrix[tile_y][tile_x]=SOURCE
            src_index=tile_y*col+tile_x
            unchanged_src=src_index
        if keystate[K_t]:#keep only one target
            x,y=pygame.mouse.get_pos()
            tile_x,tile_y= display.get_tile_xy(start_x,start_y,row,col,tile_length,x,y)
            for i in range(row):
                for j in range(col):
                    if matrix[i][j]==TARGET or matrix[i][j]==TRIAL:
                        matrix[i][j]=FLAT
            matrix[tile_y][tile_x]=TARGET
            tar_index=tile_y*col+tile_x
            unchanged_tar=tar_index
        if keystate[K_d]:
            potential_matrix=potential_field.cal_potential_field(matrix,row,col,unchanged_src,unchanged_tar)
            display.display_potential_field(screen,potential_matrix,row,col,start_x,start_y,tile_length)

        if keystate[K_RETURN]:
            if current_mode_index==0:
                # A Star
                graph=GridWithWeights(row,col)
                for i in range(row):
                    for j in range(col):
                        if matrix[i][j]==BLOCK:
                            graph.walls.append((i,j))
                start=(src_index/col,src_index%col)
                final=(tar_index/col,tar_index%col)
                came_from, cost_so_far=a_star_search(graph,start,final)
                path=reconstruct_path(came_from,start,final)
                for i in path:
                    temp_row=i[0]
                    temp_col=i[1]
                    matrix[temp_row][temp_col]=TRIAL
                matrix[unchanged_src//col][unchanged_src%col]=SOURCE
                matrix[unchanged_tar//col][unchanged_tar%col]=TARGET
            elif current_mode_index==1:
                # Potential Field Algorithm
                if tar_index==-1 or src_index==-1:
                    pass
                else:
                    print 'over'
                    potential_matrix=potential_field.cal_potential_field(matrix,row,col,unchanged_src,unchanged_tar)
                    # matrix=potential_field.potential_field_path(matrix,potential_matrix,row,col,src_index,tar_index)
                    # display.display_matrix(screen,matrix,row,col,start_x,start_y,tile_length)
#--------------------------------------------------
                    clannad=src_index
                    while src_index!=tar_index:
                        #print src_index
                        #raw_input()
                        matrix,src_index=potential_field.potential_field_step(matrix,potential_matrix,row,col,src_index,tar_index)
                        display.display_matrix(screen,matrix,row,col,start_x,start_y,tile_length)
                        pygame.display.flip()
                        clock.tick(FPS)
                    src_index=clannad
#--------------------------------------------------
                matrix[unchanged_src//col][unchanged_src%col]=SOURCE
                matrix[unchanged_tar//col][unchanged_tar%col]=TARGET
            elif current_mode_index==2:
                # combination
                potential_matrix=potential_field.cal_potential_field(matrix,row,col,unchanged_src,unchanged_tar)
                matrix=combination(matrix,potential_matrix,row,col,unchanged_src,unchanged_tar,col//3)
                matrix[unchanged_src//col][unchanged_src%col]=SOURCE
                matrix[unchanged_tar//col][unchanged_tar%col]=TARGET
                display.display_matrix(screen,matrix,row,col,start_x,start_y,tile_length)
                print 'combination over'
        mode_image,mode_rect=render_string(pathfinding_mode[current_mode_index],myfont,(0,255,0),(WIN_WIDTH/2,20))
        screen.fill((0,0,0))
        display.display_matrix(screen,matrix,row,col,start_x,start_y,tile_length)
        screen.blit(mode_image,mode_rect)
        pygame.display.flip()
#        display.display_matrix(screen,matrix,row,col,start_x,start_y,tile_length)


# -------------------------------------------
#
#             # dijkstra code
#
#             link_data=dijkstra.build_link(matrix,row,col)
#             trial=dijkstra.dijkstra(link_data,row,col,src_index,tar_index)
#             display.display_path(screen,matrix,row,col,trial)
#         display.display_matrix(screen,matrix,row,col,start_x,start_y,tile_length)
#         pygame.display.flip()
#
# -------------------------------------------

def render_string(current_string,font,color,rect_center=(0,0)):
    text=font.render(current_string,1,color)
    textpos=text.get_rect(center=rect_center)
    return text,textpos


def combination(matrix,potential_matrix,row,col,src_index,tar_index,max_manhattan_distance):
    src_row=src_index/col
    src_col=src_index%col
    tar_row=tar_index/col
    tar_col=tar_index%col
    print src_row,src_col,tar_row,tar_col
    cur_row=src_row
    cur_col=src_col
    print cur_row,cur_col
    while cur_row!=tar_row or cur_col!=tar_col:
        min_potential=MAX_COST
        min_row=-1
        min_col=-1
        for direction in range(8):
            temp_row,temp_col=dijkstra.get_adjacent_index(row,col,cur_row,cur_col,direction)

            if potential_field.in_range(row,col,temp_row,temp_col):
                print potential_matrix[temp_row][temp_col],
                if potential_matrix[temp_row][temp_col]<min_potential:
                    print temp_row,temp_col,
                    min_potential=potential_matrix[temp_row][temp_col]
                    min_row=temp_row
                    min_col=temp_col
        potential_field.trial_process(matrix,potential_matrix,row,col,min_row*col+min_col)
        cur_row=min_row
        cur_col=min_col
        print 'min(',min_row,min_col,')'
        matrix[min_row][min_col]=TRIAL
        m_distance=cal_manhattan_distance(cur_row*col+cur_col,tar_index,row,col)
        if m_distance<=max_manhattan_distance:
            break

    src_index=cur_row*col+cur_col
    print src_index,tar_index
    graph=GridWithWeights(row,col)
    for i in range(row):
        for j in range(col):
            if matrix[i][j]==BLOCK:
                graph.walls.append((i,j))
    start=(src_index//col,src_index%col)
    final=(tar_index//col,tar_index%col)
    came_from,cost_so_far=a_star_search(graph,start,final)
    path=reconstruct_path(came_from,start,final)
    for i in path:
        temp_row=i[0]
        temp_col=i[1]
        matrix[temp_row][temp_col]=TRIAL
    return matrix
def cal_manhattan_distance(src_index,tar_index,row,col):
    src_row=src_index/col
    src_col=src_index%col
    tar_row=tar_index/col
    tar_col=tar_index%col
    return abs(src_row-tar_row)+abs(src_col-tar_col)

if __name__=='__main__': main()
