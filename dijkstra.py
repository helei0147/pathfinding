import sys,os,math,string
MAX_COST=10086
BLOCK=3
FLAT=0
SOURCE=1
TARGET=2
TRIAL=4
WIN_WIDTH=1920
WIN_HEIGHT=1080
DEFAULT_FRAME_WIDTH=50

'''
rows=input("Please enter the number of rows:")
cols=input("Please enter the number of cols:")
matrix=[[]for i in range(rows)]
for i in range(rows):
    for j in range(cols):
        matrix[i].append(0)
source_row=input("Please enter the source's row:")
source_col=input("Please enter the source's col:")
target_row=input("Please enter the target's row:")
target_col=input("Please enter the target's col:")
'''
def cal_specific_tile(matrix,target):
    count=0
    for i in matrix:
        for j in i:
            if j==target:
                count+=1
    return count

def check_only_source_target(matrix):
    if cal_specific_tile(matrix,SOURCE)==1 and cal_specific_tile(matrix,TARGET):
        return True
    return False

def get_adjacent_index(row,col,src_row,src_col,direction):

    if direction==0:
        temp_row=src_row-1
        if temp_row<0:
            return -1,-1
        else:
            return temp_row,src_col
    elif direction==2:
        temp_col=src_col+1
        if temp_col==col:
            return -1,-1
        else:
            return src_row,temp_col
    elif direction==4:
        temp_row=src_row+1
        if temp_row==row:
            return -1,-1
        else:
            return temp_row,src_col
    elif direction==6:
        temp_col=src_col-1
        if temp_col<0:
            return -1,-1
        else:
            return src_row,temp_col
    elif direction==1:
        temp_col=src_col+1
        temp_row=src_row-1
        if temp_col==col or temp_row<0:
            return -1,-1
        else:
            return temp_row,temp_col
    elif direction==3:
        temp_row=src_row+1
        temp_col=src_col+1
        if temp_col==col or temp_row==row:
            return -1,-1
        else:
            return temp_row,temp_col
    elif direction==5:
        temp_row=src_row+1
        temp_col=src_col-1
        if temp_row==row or temp_col<0:
            return -1,-1
        else:
            return temp_row,temp_col
    elif direction==7:
        temp_row=src_row-1
        temp_col=src_col-1
        if temp_row<0 or temp_col<0:
            return -1,-1
        else:
            return temp_row,temp_col
def cal_dis(matrix,row,col,src_index,direction):
    adj_row,adj_col=get_adjacent_index(row,col,src_index/col,src_index%col,direction)
    #print adj_row,adj_col
    t_tile=matrix[adj_row][adj_col]
    s_tile=matrix[src_index/col][src_index-src_index/col*col]
    if t_tile==BLOCK or s_tile==BLOCK:
        return MAX_COST
    else:
        # Need a much more complex algorithm, but now is 1
        if direction%2==0:
            return 5
        else:
            return MAX_COST
def build_link(matrix,row,col):

    link_data=[]
    for i in range(row*col):
        adjacent_buffer=[]
        for j in range(8):
            src_row=i/col
            src_col=i%col
            adj_row,adj_col=get_adjacent_index(row,col,src_row,src_col,j)
            adjacent_index=adj_row*col+adj_col
            if adj_row==-1:
                adjacent_buffer.append((-1,MAX_COST))
            else:
                distance=cal_dis(matrix,row,col,i,j)
                adjacent_buffer.append((adjacent_index,distance))
        link_data.append(adjacent_buffer)
    return link_data

def dijkstra(link_data,row,col,src_index,tar_index):
    visited_list=[]
    dist_list=[]
    prev_list=[]
    for i in range(row*col):
        visited_list.append(False)
        dist_list.append(-1)
        prev_list.append(-1)
    visited_list[src_index]=True
    dist_list[src_index]=0
    while(visited_list.count(False)!=0):
        min_dist=MAX_COST
        min_index=-1
        min_prev=-1
        for i in range(row*col):
            if visited_list[i]==True:#check every added node
                #find the minimal dist to src_index
                for adj in range(8):
                    adj_index=link_data[i][adj][0]
                    if adj_index!=-1 and visited_list[adj_index]==False:#there exist a link to a visited node
                        temp_dist=dist_list[i]+link_data[i][adj][1]
                        if temp_dist<min_dist:
                            min_dist=temp_dist
                            min_index=link_data[i][adj][0]
                            min_prev=i
        if min_index==-1:
            print 'error exist, min_index is -1'
            return -1
       # print min_index
        dist_list[min_index]=min_dist
        prev_list[min_index]=min_prev
        visited_list[min_index]=True
        if min_index==tar_index:
            break
    #print prev_list
    trial=[]
    temp_index=tar_index
    trial.append(tar_index)
    while prev_list[temp_index]!=src_index:
        trial.append(prev_list[temp_index])
        temp_index=prev_list[temp_index]
    trial.append(src_index)
    trial.reverse()
    #print trial
    return trial
