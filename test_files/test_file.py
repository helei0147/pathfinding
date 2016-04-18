import sys,os
def file_out(file_obj,mylist):
    tempstring=''
    for i in mylist:
        tempstring=tempstring+str(i)
        tempstring=tempstring+' '
    tempstring=tempstring+'\n'
    file_obj.write(tempstring)

def main():
    mylist=[]
    for i in range(10):
        mylist.append(i)
    myfile=open('myfile.txt','w')
    file_out(myfile,mylist)
    myfile.close()


if __name__ =='__main__':
    main()
