import os
import re
import yaml
import process_input_file
import os
import argparse
from datetime import datetime, timezone, timedelta
OUTPUT_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/output.html"


def open_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

def read_rule(file_name):
    # with open(file_name, 'r') as file:
    #     return file.read()
    with open(file_name, 'r') as file:
        data = yaml.safe_load(file)
    return data


def get_plus_line(file_content: str):  # return a list
    split_ = file_content.split('\n')
    plus_line = [i for i in split_ if i.startswith('+')]
    for i in range(len(plus_line)):
        plus_line[i] = re.sub(r'^[+-]\s*', '', plus_line[i])
    return plus_line


def get_lst_pattern(rule_content: dict):
    lst_pattern = []
    try:
        # case1: only 1 pattern
        pattern = rule_content['rules'][0]['pattern']  # return to string
        lst_pattern.append(pattern)
    except:
        # case: multiple patterns
        # try:
        for patterns in rule_content['rules'][0]['patterns']:
            lst_pattern.append(patterns)
    return lst_pattern


def split_var_and_func(var_and_func: str):
    # nếu startwith ='$' thì có biến, ko thì chỉ có hàm
    var = []
    func = []
    # Check có dấu "=" hay không
    if var_and_func.__contains__(" = "):
        var.append(var_and_func.split(" = ")[0])
        var_and_func = var_and_func.split(" = ")[1]
    lst_split = var_and_func.split(".")
    if len(lst_split) == 1:
        func.append(lst_split[0])
    else:
        for ele in lst_split:
            if ele.startswith('$') and ele != '$FUNC':
                var.append(ele)
            else:
                func.append(ele)
    return var, func


def split_pattern_components(lst_pattern: list):  # split into 3 components
    lst_split_components = []

    for pattern in lst_pattern:
        # case1: has only 1 pattern
        open_bracket_index = pattern.find('(')  # get index of the first '('
        close_bracket_index = pattern.rfind(')')  # get index of the last ')'
        if open_bracket_index != -1:
            if pattern[open_bracket_index-1] == ' ':  # remove space before '('
                continue
            else:
                variable_and_function = pattern[:open_bracket_index]
                var, func = split_var_and_func(variable_and_function)
                parameters = pattern[open_bracket_index+1:close_bracket_index]
                # parameters = [ele.replace(" ","") for ele in parameters.split(",") if not ele.__contains__("...")]
                params = [ele.replace(" ", "") for ele in parameters.split(",")]
                # try:
                #     parameters.remove('')
                # except:
                #     pass
                # str_func = variable_and_function if not variable_and_function.startswith("$")
                dict_ = {
                    # "var_and_func": variable_and_function,
                    "variable": var,
                    "function": func,
                    "parameters": params
                }
                # lst_split_components.append((variable_and_function, parameters))
                lst_split_components.append(dict_)

        # case2: has multiple patterns
    return lst_split_components


def get_all_rules(rules_folder: str):
    # rules_folder = os.getcwd() + '/project_VD/rules'
    rules_list = os.listdir(rules_folder)
    all_rules = []  # list of all rules
    # import all rules
    for i in range(len(rules_list)):
        # read rule content
        # rule_content = read_rule(rules_folder + '/' + rules_list[3])
        rule_content = read_rule(rules_folder + '/' + rules_list[i])

        ##################### processing #####################
        rule_id = rule_content['rules'][0]['id']  # extract rule_id
        # rule dictionary contains rule_id and list of patterns
        rules = {'rule_id': rule_id}
        rules['message'] = rule_content['rules'][0]['message']
        rules['cwe'] = rule_content['rules'][0]['metadata']['cwe']

        lst_pattern = get_lst_pattern(rule_content)  # get list of patterns
        # print("Pattern in rule file: ", lst_pattern)
        # add lists patterns to rules dictionary
        rules['patterns'] = lst_pattern
        all_rules.append(rules)  # add rules to all_rules list

    return all_rules



def extract_info_from_string(info_string):
    info_dict = {}
    parts = info_string.split(':')
    pullrequest = parts[1].replace("Author", "")
    info_dict['Pull Request SHA'] = pullrequest
    info_dict['Author'] = (parts[2].replace("Date", ""))
    joined_string = ':'.join(parts[3:6])
    date = joined_string.split('+')
    info_dict['Date'] = date[0]
    info_dict['State'] = parts[7]
    info_dict['File Change'] = " " + parts[8]
    return info_dict

def writefile(output_file_path=OUTPUT_FILE_PATH):
    with open(output_file_path, "a") as f:
        f.write(f"""
            <div>
                <button onclick="toggleAllDetails()">Show All Commits</button>
            </div>
            """)

def output(info_sub_file, rule: dict, status: bool = True, output_file_path=OUTPUT_FILE_PATH):
    # file_path = os.path.dirname(os.path.abspath(__file__))
    # path = file_path + output_file
    with open(output_file_path, "a") as f:
        info_dict = extract_info_from_string(info_sub_file)
        
        if status:
            #write to file         
            f.write('<div class="result commit-details" style="display: none;">\n'
                    f'<p><span style="color: red;">Pull Request SHA:</span> {info_dict["Pull Request SHA"]}</p>\n'
                    f'<p>Author: {info_dict["Author"]}</p>\n'
                    f'<p>Date: {info_dict["Date"]}</p>\n'
                    f'<p>State: {info_dict["State"]}</p>\n'
                    f'<p>File Change: {info_dict["File Change"]}</p>\n'
                    f'<p>rule_id: {rule["rule_id"]}</p>\n'
                    f'<p>message: {rule["message"]}</p>\n'
                    f'<p>cwe: {rule["cwe"]}</p>\n'
                    f'<hr>\n'
                    '</div>\n\n')



            #print to console
            print(info_sub_file)
            print("rule_id:", rule['rule_id'])
            print("message:", rule['message'])
            print("cwe:", rule['cwe'])
            print("\n")
        else:
            #print to console
            print("No malicious commits were found", end="\n\n")
            #write to file
            f.write('<div class="result commit-details" style="display: none;">\n'
                    f'<p>Pull Request SHA: {info_dict["Pull Request SHA"]}</p>\n'
                    f'<p>Author: {info_dict["Author"]}</p>\n'
                    f'<p>Date: {info_dict["Date"]}</p>\n'
                    f'<p>State: {info_dict["State"]}</p>\n'
                    f'<p>File Change: {info_dict["File Change"]}</p>\n'
                    f'<p>No malicious commits were found</p>\n'
                    f'<hr>\n'
                    '</div>\n\n')


    f.close()
    
# True: error, False: no error
# Check if split_pattern is in split_line
def compare_pattern_between_commit_and_line(split_line, split_pattern):
    for ele_line in split_line:
        for pattern in split_pattern:
            # if pattern['function'] == ele_line['function']:  # check function first
            if any(elem in pattern['function'] for elem in ele_line['function']):
                # check parameter part
                # case1: no parameter
                if pattern['parameters'] == [] and ele_line['parameters'] == []:
                    # print result
                    return True
                elif pattern['parameters'] == [] and ele_line['parameters'] != []:
                    # print("No error 1")
                    return False
                elif pattern['parameters'] != [] and ele_line['parameters'] == []:
                    # print("No error 2")
                    return False
                else:
                    if pattern['parameters'] == ['...']:  # case: func.(...)
                        # print result
                        return True
                    else:
                        if set(pattern['parameters']) == set(ele_line['parameters']):
                            # print result
                            return True
                        else:
                            for param in pattern['parameters']:  # pram: string
                                if param.__contains__('...'):
                                    for ele in ele_line['parameters']:
                                        regex_temp = param.replace(
                                            "...", "(.*)")
                                        regex_temp = regex_temp.replace(
                                            "'", "['|\"]")
                                        # re.search(regex_temp, ele_line['parameters']).group(1)
                                        if re.findall(regex_temp, ele):
                                            return True
            else:
                return False
    return False


def processing(sub_file_content, rules_folder:str, output_file_path:str=OUTPUT_FILE_PATH):
    
    info_sub_file = process_input_file.get_info_line(sub_file_content)  # get info of file
    # get lines needed to be checked
    lst_plus_line = get_plus_line(sub_file_content)

    # get list all rules
    lst_all_rules = get_all_rules(rules_folder)
    # print("List all rules: ", lst_all_rules, end="\n\n")

    # print("Pattern in commit: ", lst_plus_line, end="\n\n")
    # print("List lines start with +:", lst_plus_line, end="\n\n")
    splited_line = split_pattern_components(lst_plus_line)  # return a list
    # print("List of elements Splited line in commit:", splited_line, end="\n\n")

    num_error = 0
    checked = True

    for rule in lst_all_rules:
        if len(rule['patterns']) == 1:
            split_pattern = split_pattern_components(rule['patterns'])
            # print("Pattern: ", split_pattern)
            # True
            if compare_pattern_between_commit_and_line(splited_line, split_pattern):
                output(info_sub_file=info_sub_file, rule=rule, output_file_path=output_file_path)

            else:
                # print("No error", end="\n\n")
                num_error += 1
        else:  # multiple patterns
            lst_sub_patterns = []
            lst_sub_not_patterns = []
            for dict_pattern in rule['patterns']:
                if list(dict_pattern.keys())[0] == 'pattern':  # get 1 pattern
                    pattern_value = dict_pattern['pattern']
                    split_pattern = split_pattern_components([pattern_value])
                    # print("Pattern: ", split_pattern)
                    lst_sub_patterns.extend(split_pattern)

                elif list(dict_pattern.keys())[0] == 'pattern-not':
                    pattern_not_value = [dict_pattern['pattern-not']]
                    split_pattern = split_pattern_components(pattern_not_value)
                    # print("List of elements Splited patterns (not-pattern): ", split_pattern)
                    lst_sub_not_patterns.extend(split_pattern)
                    # Check nếu  = pattern-not --> không có trong commit (No error)
                    # print("List sub patterns: ", lst_sub_patterns)
                    # print("List sub not patterns: ", lst_sub_not_patterns)

                    # compare
                    check = 0
                    for pattern in lst_sub_patterns:
                        # True: #Có khả năng lỗi
                        if compare_pattern_between_commit_and_line(splited_line, [pattern]) == True:
                            for pattern_not in lst_sub_not_patterns:
                                # True
                                if compare_pattern_between_commit_and_line(splited_line, [pattern_not]) == True:
                                    # print("No error", end="\n\n")
                                    continue
                                else:
                                    # Output: error
                                    # output(info_sub_file, rule)
                                    check += 1
                        else:
                            # print("No error", end="\n\n")
                            continue
                    if check != 0:
                        output(info_sub_file=info_sub_file, rule=rule, output_file_path=output_file_path)
                    else:
                        # print("No error", end="\n\n")
                        num_error += 1

                elif list(dict_pattern.keys())[0] == 'metavariable-regex':
                    # dictionary
                    metavariable_regex = dict_pattern['metavariable-regex']
                    # print("Metavariable-regex: ", metavariable_regex)
                    # print("Split pattern:", split_pattern)

                    regex = pattern_value
                    regex = regex.replace(metavariable_regex['metavariable'], metavariable_regex['regex'])
                    regex = regex.replace("...", "(.*)")
                    check = 0
                    for line in lst_plus_line:
                        if re.findall(regex, line):
                            check += 1
                    if check != 0:
                        output(info_sub_file=info_sub_file, rule=rule, output_file_path=output_file_path)
                    else:
                        # print("No error", end="\n\n")
                        num_error += 1
    if num_error == len(lst_all_rules):
        output(info_sub_file=info_sub_file, rule=rule, status=False, output_file_path=output_file_path)
        checked = False
    return checked  

def html_report(output_file_path: str=OUTPUT_FILE_PATH):
    if os.path.exists(OUTPUT_FILE_PATH):
        os.remove(OUTPUT_FILE_PATH)
    f = open(output_file_path, "a")
    scan_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Report Details</title>
            <style>
                .commit-details {
                    display: none;
                }
            </style>
            <script>
            function toggleAllDetails() {
                var commits = document.getElementsByClassName("commit-details");
                for (var i = 0; i < commits.length; i++) {
                    var commit = commits[i];
                    if (commit.style.display === "none") {
                        commit.style.display = "block";
                    } else {
                        commit.style.display = "none";
                    }
                }
            }
            </script>
        </head>
        <body>
    """)


    f.write(f"<h1>Commit Scan Report - {scan_datetime}</h1>")
    f.write(f"""
        <div>
            <button onclick="toggleAllDetails()">Show All Commits</button>
        </div>
    """)

def run(change_file_path: str, rules_folder: str, output_file_path: str=OUTPUT_FILE_PATH):
    # folder_path = os.getcwd() + '/project_VD/change_file_pull'
    # # file_list = os.listdir(folder_path)

    # rules_folder = os.getcwd() + '/project_VD/rules'
    html_report(output_file_path)
    
###################### test by run all file code ######################
    # read file content
    # project_change_pull.txt
    # file_content = open_file(change_folder_path + '/project_change_pull(new).txt')
    file_content = open_file(change_file_path)
    lst_sub_file_content = process_input_file.get_list_splited_file(file_content)

    count_violent = 0
    for i in range(len(lst_sub_file_content)):
        # file_name = process_input_file.get_file_name(lst_sub_file_content[i])
        # file_path = os.path.dirname(os.path.abspath(__file__))
        # output_file_path = file_path + output_file
        f = open(output_file_path, "a")
        f.write("\n\n")
        f.close()
        check = processing(lst_sub_file_content[i], rules_folder=rules_folder, output_file_path=output_file_path)                                                              
        if (check == True):
            count_violent += 1
    f = open(output_file_path, "a")
    f.write(f"<h2>{count_violent}/{len(lst_sub_file_content)} Commit were violated </h2>")
    f.close()
def add_argument():
    output_file_path = os.path.dirname(os.path.abspath(__file__)) + "/output.html"

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--rulefolder', type=str, help='Rules folder path')
    parser.add_argument('--changefile', type=str, help='Change pull-requests file path')
    parser.add_argument('--outputfile', type=str, help='Output file path', default=output_file_path)
    args = parser.parse_args()
    run(args.changefile, args.rulefolder, args.outputfile)

###############################################################
if __name__ == '__main__':
    # folder_path = os.getcwd() + '/project_VD/change_file_pull'
    # file_list = os.listdir(folder_path)

    # rules_folder = os.getcwd() + '/project_VD/rules'
    # # rules_list = os.listdir(rules_folder)

    # file_name = "/output1.txt"
    # change_file_path = os.path.dirname(os.path.abspath(__file__)) +'/change_file_pull/project_change_pull(new).txt'
    # rules_folder = os.path.dirname(os.path.abspath(__file__)) + '/rules'
    # output_file_path = os.path.dirname(os.path.abspath(__file__)) + file_name

    # run(change_file_path, rules_folder)
    add_argument()
    