from constants import *
def write_in_file(filename,matrix,row,col):
    file_object=open(filename,'w')
    tempstring=''
    tempstring=tempstring+str(row)
    tempstring=tempstring+' '
    tempstring=tempstring+str(col)
    tempstring=tempstring+'\n'
    file_object.write(tempstring)
    print tempstring
    for i in range(row):
        for j in range(col):
            if matrix[i][j]==BLOCK:
                tempstring=''
                tempstring=tempstring+str(i)
                tempstring=tempstring+' '
                tempstring=tempstring+str(j)
                tempstring=tempstring+str('\n')
                file_object.write(tempstring)
    file_object.close()


def read_in_file(filename):
    file_obj=open(filename)
    templist=[int(i) for i in file_obj.readline().split()]
    print templist
    row=templist[0]
    col=templist[1]
    matrix=[]
    for i in range(row):
        temp=[]
        for j in range(col):
            temp.append(FLAT)
        matrix.append(temp)
    while True:
        templist=[int(i) for i in file_obj.readline().split()]
        if len(templist)==0:
            break;
        else:
            #print templist
            temp_row=templist[0]
            temp_col=templist[1]
            matrix[temp_row][temp_col]=BLOCK
    file_obj.close()
    return matrix,row,col
