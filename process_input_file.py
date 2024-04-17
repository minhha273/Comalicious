import os

def open_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

def split_into_sub_files(file_content: str):
    list_split = file_content.split('--------------------------------------------------------\n\n')
    try:
        list_split.remove('')
    except ValueError:
        pass
    return list_split

def get_list_splited_file(file_content: str):
    # folder_path = os.getcwd() + '/project_VD/change_file_pull'
    # file_path = folder_path + '/project_change_pull.txt'
    
    # file_content = open_file(file_path)
    lst_splited_file = split_into_sub_files(file_content=file_content)
    return lst_splited_file

def get_info_line(sub_file_content: str): #return a string
    list_line = sub_file_content.split('\n')
    list_line = list_line[:5]
    # info_dict = {key.strip(): value.strip() for key, value in (item.split(': ', 1) for item in list_line)}
    str_info = '\n'.join(list_line)
    return str_info

def get_file_name(sub_file_content: str):
    list_line = sub_file_content.split('\n')
    file_name = list_line[4].split(': ')[1]
    return file_name

if __name__ == "__main__":
    # folder_path = os.getcwd() + '/project_VD/change_file_pull'
    # file_path = folder_path + '/project_change_pull.txt'
    
    # file_content = open_file(file_path)
    # splited_file = split_into_sub_files(file_content=file_content)
    # print(splited_file[0])
    # print(get_info_line(splited_file[1]))
    pass