import sys,os,math,constants
import dijkstra
from constants import *
def in_range(row,col,s_row,s_col):
    if s_row>=0 and s_row<row:
        if s_col>=0 and s_col<col:
            return True
    return False

def get_symmetry(centre_row,centre_col,temp_row,temp_col):
    return centre_row*2-temp_row,centre_col*2-temp_col



def trial_process(matrix,matrix_potential,row,col,trial_index):
    # trial_process with rect effection
    src_row=trial_index/col
    src_col=trial_index%col
    max_dis=2
    step=PASSED_EFFECT/max_dis
    matrix_potential[src_row][src_col]=MAX_COST
    temp_effect=PASSED_EFFECT

    for i in range(1,max_dis):
        temp_effect=PASSED_EFFECT/(i+5)
        #print temp_effect
        start_row1=src_row-i
        start_col1=src_col+i
        for j in range(i*2):
            temp_row=start_row1+j
            temp_col=start_col1
            if in_range(row,col,temp_row,temp_col):
                matrix_potential[temp_row][temp_col]+=temp_effect
        start_row2=src_row+i
        start_col2=src_col+i
        for j in range(i*2):
            temp_row = start_row2
            temp_col=start_col2-j
            if in_range(row,col,temp_row,temp_col):
                matrix_potential[temp_row][temp_col]+=temp_effect
        start_row3=src_row+i
        start_col3=src_col-i
        for j in range(i*2):
            temp_row=start_row3-j
            temp_col=start_col3
            if in_range(row,col,temp_row,temp_col):
                matrix_potential[temp_row][temp_col]+=temp_effect
        start_row4=src_row-i
        start_col4=src_col-j
        for j in range(i*2):
            temp_row=start_row4
            temp_col=start_col4+j
            if in_range(row,col,temp_row,temp_col):
                matrix_potential[temp_row][temp_col]+=temp_effect

'''
    for i in range(1,max_dis+1):
        for j in range(i):
            temp_row=src_row+i-j
            temp_col=src_col-j
            if in_range(row,col,temp_row,temp_col):
                matrix_potential[temp_row][temp_col]+=temp_effect
            # and it's symmetry
            sym_row,sym_col=get_symmetry(src_row,src_col,temp_row,temp_col)
            if in_range(row,col,sym_row,sym_col):
                matrix_potential[sym_row][sym_col]+=temp_effect
            temp_row=src_row+j
            temp_col=src_col+i-j
            if in_range(row,col,temp_row,temp_col):
                matrix_potential[temp_row][temp_col]+=temp_effect
            # and it's symmetry
            sym_row,sym_col=get_symmetry(src_row,src_col,temp_row,temp_col)
            if in_range(row,col,sym_row,sym_col):
                matrix_potential[sym_row][sym_col]+=temp_effect
'''


def block_process(matrix,matrix_3d,row,col,src_index):
    # Let's think about how a block affect other tiles
    # set the max distance a block can effect is 4
    # this has a monotone effect
    # get a diamond effect field
    src_row=src_index/col
    src_col=src_index%col
    max_dis=5
    step=BLOCK_EFFECT/max_dis
    temp_effect=BLOCK_EFFECT
    matrix_3d[src_row][src_col].append(MAX_COST)
    for i in range(1,max_dis+1):
        for j in range(i):
            temp_row=src_row+i-j
            temp_col=src_col-j
            if in_range(row,col,temp_row,temp_col):
                matrix_3d[temp_row][temp_col].append(temp_effect)
            # and it's symmetry
            sym_row,sym_col=get_symmetry(src_row,src_col,temp_row,temp_col)
            if in_range(row,col,sym_row,sym_col):
                matrix_3d[sym_row][sym_col].append(temp_effect)
            temp_row=src_row+j
            temp_col=src_col+i-j
            if in_range(row,col,temp_row,temp_col):
                matrix_3d[temp_row][temp_col].append(temp_effect)
            # and it's symmetry
            sym_row,sym_col=get_symmetry(src_row,src_col,temp_row,temp_col)
            if in_range(row,col,temp_row,temp_col):
                matrix_3d[sym_row][sym_col].append(temp_effect)
        #can only change the following line to simulate the potential field's effect
        temp_effect=BLOCK_EFFECT-BLOCK_EFFECT/(max_dis*max_dis)*i*i

def target_process(matrix,matrix_potential,row,col,src_index):
    # on the foundation of block_process
    # if there is a path approching the target
    # that node has a smaller value
    # src_row=src_index/col
    # src_col=src_index%col
    # max_dis=max(row,col)
    # step=TARGET_EFFECT/max_dis
    # temp_effect=TARGET_EFFECT
    # matrix_potential[src_row][src_col]=TARGET_EFFECT*3
    # for i in range(1,max_dis+1):
    #     for j in range(i):
    #         temp_row=src_row+i-j
    #         temp_col=src_col-j
    #         if in_range(row,col,temp_row,temp_col):
    #             matrix_potential[temp_row][temp_col]+=temp_effect
    #         # and it's symmetry
    #         sym_row,sym_col=get_symmetry(src_row,src_col,temp_row,temp_col)
    #         if in_range(row,col,sym_row,sym_col):
    #             matrix_potential[sym_row][sym_col]+=temp_effect
    #         temp_row=src_row+j
    #         temp_col=src_col+i-j
    #         if in_range(row,col,temp_row,temp_col):
    #             matrix_potential[temp_row][temp_col]+=temp_effect
    #         # and it's symmetry
    #         sym_row,sym_col=get_symmetry(src_row,src_col,temp_row,temp_col)
    #         if in_range(row,col,sym_row,sym_col):
    #             matrix_potential[sym_row][sym_col]+=temp_effect
    #     # can only change the following line to simulate the potential field's effect
    #     temp_effect=TARGET_EFFECT-TARGET_EFFECT/(max_dis*max_dis)*i*i
    src_row=src_index/col
    src_col=src_index%col
    matrix_potential[src_row][src_col]=TARGET_EFFECT*5
    for i in range(row):
        for j in range(col):
            dis=((src_row-i)**2+(src_col-j)**2)**0.5
            if dis!=0:
                matrix_potential[i][j]+=TARGET_EFFECT/dis


def cal_potential_field(matrix,row,col,tar_index):
    matrix_3d=[]
    for i in range(row):
        temp_list=[]
        for j in range(col):
            temp_list.append([])
        matrix_3d.append(temp_list)
    # now matrix_3d has three dimensions

    # check the matrix and fill the matrix_3d with blocks' effect'
    for i in range(row):
        for j in range(col):
            index=i*col+j
            if matrix[i][j]==BLOCK:
                block_process(matrix,matrix_3d,row,col,index)

    matrix_potential=[]
    # fill the matrix_potential with the max value
    for i in range(row):
        temp_list=[]
        for j in range(col):
            max_effect=0
            if len(matrix_3d[i][j])==0:
                max_effect=0
            else:
                max_effect=max(matrix_3d[i][j])
            temp_list.append(max_effect)
        matrix_potential.append(temp_list)
    # process the target
    # target has a bigger effect domain
    target_process(matrix,matrix_potential,row,col,tar_index)
    # pre-process complete
    return matrix_potential

def potential_field_path(matrix,potential_matrix,row,col,src_index,tar_index):
    src_row=src_index/col
    src_col=src_index%col
    tar_row=tar_index/col
    tar_col=tar_index%col
    cur_row=src_row
    cur_col=src_col
    while cur_row!=tar_row or cur_col!=tar_col:
        min_potential=MAX_COST
        min_row=-1
        min_col=-1
        for direction in range(8):
            temp_row,temp_col=dijkstra.get_adjacent_index(row,col,cur_row,cur_col,direction)
            if in_range(row,col,temp_row,temp_col):
                if potential_matrix[temp_row][temp_col]<min_potential \
                   and potential_matrix[temp_row][temp_col]<MAX_COST:
                    min_potential=potential_matrix[temp_row][temp_col]
                    min_row=temp_row
                    min_col=temp_col
        trial_process(matrix,potential_matrix,row,col,min_row*col+min_col)
        cur_row=min_row
        cur_col=min_col
        matrix[min_row][min_col]=TRIAL
    return matrix

def potential_field_step(matrix,potential_matrix,row,col,src_index,tar_index):
    src_row=src_index/col
    src_col=src_index%col
    tar_row=tar_index/col
    tar_col=tar_index%col
    cur_row=src_row
    cur_col=src_col

    min_potential=MAX_COST
    min_row=-1
    min_col=-1
    for direction in range(8):
        temp_row,temp_col=dijkstra.get_adjacent_index(row,col,cur_row,cur_col,direction)

        if in_range(row,col,temp_row,temp_col):
            #print len(potential_matrix)
            if potential_matrix[temp_row][temp_col]<min_potential \
               and potential_matrix[temp_row][temp_col]<MAX_COST:
                min_potential=potential_matrix[temp_row][temp_col]
                min_row=temp_row
                min_col=temp_col
    trial_process(matrix,potential_matrix,row,col,min_row*col+min_col)
    print cur_row,cur_col
    #print potential_matrix[cur_row][cur_col],potential_matrix[min_row][min_col]
    cur_row=min_row
    cur_col=min_col
    src_index=cur_row*col+cur_col
    matrix[min_row][min_col]=TRIAL
    return matrix,src_index
