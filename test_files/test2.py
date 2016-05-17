import sys,os
data_file=open("myfile.txt",'r')
while True:
    text_line =[int(i)for i in data_file.readline().split()]
    if len(text_line)==0:
        break
    print text_line
