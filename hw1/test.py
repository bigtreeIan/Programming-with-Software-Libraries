from pathlib import Path

##def open_list(lis_t):
##    list2 = []
##    for i in lis_t:
##        if i != list:
##            list2.append(i)
##        else:
##            list2 =
##
##    return list2




def search_files(path):
    files_in_path = []
    try:
        for i in path.iterdir():
            files_in_path.append(i)
        return files_in_path

    except:
        return -1





def find_files(list_of_file,path):
    files = []
    for i in list_of_file:
        if i.is_file() == True:
            files.append(i)
            
        else:
            list_of_file = search_files(i)
            if list_of_file != -1:
                path_list_inside = find_files(list_of_file, i)
                files = files + path_list_inside

    return files

def main():
    path = Path('/Users/xuyihan/Desktop/EECS12/note')
    l = search_files(path)
    path_list = find_files(l,path)
    print(path_list)
 #   list3 = open_list(path_list)
#    print(list3)

main()
