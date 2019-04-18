###hw1
###Name: Yihan Xu / Zihao Gao
###ID: 47011405 / 35004695
###Date: 10/4/2015


from pathlib import Path
from shutil import *

###check if the path is correct, if it is correct, return the true path and -1,
###if not, return the wrong path and 1
def check_path(path):
    p = Path(path)
    if p.exists() == True:
        return p, -1
    else:
        return p, 1


###check if the python find a file or folder, if it is a folder, return p;
###if not return -1, in order to append the path of file into a list later.
def check_folder(path):
    p = path
    if p.is_file() == True:
        return -1
    else:
        return p    


def main():
    ###check the path that users input, if it is nothing, print error
    a = 0
    while a != -1:
        x = input()
        if x == '':
            x = 'error'
            
        ###call the check_path function to check the path    
        path, a = check_path(x)

        ###append the correct path to a list
        l = []
        
        if a == -1:
            for i in path.iterdir():
                l.append(i)
        ###print Error if the path is wrong
        if a == 1:
            print('Error')
    ###ask users to input the second line
    b = 0
    while b != -1:
        y = input()
        ###if users input nothing, change b = 0 and run the while again to ask users input again
        if y == '':
            b = 0
        ###if the users input N, get the file name which is start after a space
        elif y[0] == 'N':
            string = y[2:]
            lis = []
            for i in l:
                check = check_folder(i)
                ###if python find the file, append the path to a list and stop the while loop
                if check == -1:
                    if string == i.stem:
                        lis.append(i)
                        b = -1
        
            if lis == []:
                print('Error')
        ###if users input E, get the extension
        elif y[0] == 'E':
            ext = y[2:]
            lis = []
            for i in l:
                check = check_folder(i)
                ###if the path is a file, check if the extension users input equal
                ###to the extension in the path list and append the match one to a list
                if check == -1:
                    if ext == i.suffix:
                        lis.append(i)
                        b = -1
    
            if lis == []:
                print('Error')
        ###if users input S, get the size that users input and compare with the size
        ###file in path list append the match one to a list
        elif y[0] == 'S':
            size = y[2:]
            lis = []
            for i in l:
                check = check_folder(i)
                if check == -1:
                    if eval(size) <= i.stat().st_size:
                        lis.append(i)
                        b = -1

            if lis == []:
                print('Error')
        else:
            print('Error')


    c = 0       
    while c != -1:
        inp = input()
        ###if user input nothing, print Error
        if inp == '':
            b = 0
        ###if users input P, print the previous list                       
        elif inp[0] == 'P':
            print(lis)
            c= -1
        ###if users input F, 
        elif inp[0] == 'F':
            try:
                for i in lis:
                    ###ignore the system file then print the i and r
                    if i.stem != '.DS_Store':
                        f = i.open("r")
                        r = f.readline()
                        print(i)
                        print(r)
                        f.close()
                        c = -1
            except:
                print('This file is unreadable')
                continue
        ###if input T, use touch function
        elif inp[0] == 'T':
            for i in lis:
                i.touch()
                c = -1
        ###if input D, copy the file
        elif inp[0] == 'D':
            for i in lis:
                nfp = str(i) +'.dup'
                copy(str(i), nfp)
                c = -1
        ###else print Error                             
        else:
            print('Error')

main() 
    


    

    
