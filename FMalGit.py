#!/usr/bin/env python3
import sys, requests, argparse, subprocess
from pydriller import Repository
from datetime import datetime, timezone, timedelta
import os
from github import Github

#Get commit infomation
# def process_commit (repo):
#     print(f"Processing :{repo}")
#     minner=Repository(repo)
#     for commit in minner.traverse_commits():
#         commit_info=CommitInfo(commit)
#         commits_info.append(commit_info)
#     for commit_info in commits_info:   
#         print ("Hash: {}\nauthor: {}\nemail: {}\ndate: {}\nmsg: {}\n------\n".
#                format(commit_info.hash,commit_info.author,commit_info.email,commit_info.date,commit_info.message))

def generate_html_report(repo):

    scan_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = f"<h1>Commit Scan Report - {scan_datetime}</h1>"
    html_content += """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Commit Details</title>
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
    """
    return html_content


def create_report(repo):
    html_content = generate_html_report(repo)
    current_directory = os.path.dirname(__file__)
    html_file_name = "report.html"
    html_file_path = os.path.join(current_directory, html_file_name)
    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)
    return html_file_path


#line of code information        
def extract_nloc(repo):
    print(f"Extracting NLoC from: {repo}")
    total_nloc = 0
    miner = Repository(repo)
    for commit in miner.traverse_commits():
        commit_nloc = sum(mod.nloc for mod in commit.modified_files if mod.nloc is not None)
        print(f"Commit {commit.hash}: NLoC = {commit_nloc}")
        total_nloc += commit_nloc
    print(f"Total NLoC in the repository: {total_nloc}")     

#line changed information
def extract_changed_lines(repo,commit_hash=None):
    output_directory = os.path.join(os.getcwd(),"change_file")
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = f"{get_repo_name(repo)}_change_file.txt"
    file_path = os.path.join(output_directory,output_file_path)
    #repo = g.get_repo(f"{get_user_name(repo)}/{get_repo_name(repo)}")
    with open(file_path, "w") as output_file:

        print(f"Extracting changed lines from: {repo}")
        miner = Repository(repo)
        for commit in miner.traverse_commits():
            if commit_hash and commit_hash!=commit.hash: continue
            print(f"Commit {commit.hash}:")
            for file in commit.modified_files:
                print(f"    Modified file: {file.filename}")

                # Print added lines
                for line in file.diff_parsed['added']:
                    print(f"                                    added")
                    print(f"        + {line[1]}")
                    
                # Print deleted lines
                for line in file.diff_parsed['deleted']:
                    print(f"                                    deleted")
                    print(f"        - {line[1]}")
                    
            #print("------\n")

            print("------\n")
            
            output_file.write("Commit Hash: " + commit.hash + "\n")
            output_file.write("Author: "+ commit.author.name + "\n")
            output_file.write("Date: " + str(commit.author_date) + "\n")
            output_file.write("File Change: " + file.filename + "\n")
            for modified_file in commit.modified_files:
                for line in modified_file.diff_parsed['added']: 
                    output_file.write("Add : \n" + str(line) + "\n")
                for line in modified_file.diff_parsed['deleted']: 
                    output_file.write("Delete : \n" + str(line) + "\n")
            output_file.write("--------------------------------------------------------\n\n")

# def get_changed_file(repo,commit_hash):
#     output_directory = os.path.join(os.getcwd(), 'changed_files')
#     os.makedirs(output_directory, exist_ok=True)
#     print(f"Get changed file from: {repo}")
#     for commit in Repository(repo).traverse_commits():
#         if commit_hash == commit.hash:
#             for mod in commit.modified_files:
#                 file_path=os.path.join(output_directory,f"{commit.hash}_{mod.new_path.replace('/','_')}")
#                 with open(file_path,'w') as output_file:
#                     output_file.write(mod.source_code)
#                 print(f"File saved :{file_path}")    
#             break

            
        print('--------------------')
        command = f"python solution.py --changefile '{file_path}' --rulefolder ./rules "
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

g = Github("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")




def check_changed_file_pullreq(repo,hash=None,author=None):
    output_directory = os.path.join(os.getcwd(),"change_file_pull")
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = f"{get_repo_name(repo)}_change_pull.txt"
    file_path = os.path.join(output_directory,output_file_path)
    repo = g.get_repo(f"{get_user_name(repo)}/{get_repo_name(repo)}")
    with open(file_path, "w") as output_file:

# Lấy tất cả các yêu cầu kéo
        pull_requests = repo.get_pulls()
    
    # Lặp qua từng yêu cầu kéo
        for pull_request in pull_requests:
            # Lấy mã hash của yêu cầu kéo
            if hash and pull_request.head.sha != hash:
                continue
            if author and pull_request.user.login != author:
                continue
            pull_request_sha = pull_request.head.sha
            print("Pull Request SHA:", pull_request_sha)
            
            # Lấy ngày tạo của yêu cầu kéo
            created_at = pull_request.created_at
            print("Created at:", created_at)

            # Lấy tên đăng nhập của người gửi yêu cầu kéo
            login_name = pull_request.user.login
            print("Login Name:", login_name)
            
            # Lấy trạng thái của yêu cầu kéo (open, closed, merged)
            state = pull_request.state
            print("State:", state)
            
            # Lấy danh sách các tệp thay đổi trong yêu cầu kéo
            files = pull_request.get_files()

            # In ra thông tin về các tệp thay đổi
            for file in files:
                print("File:", file.filename)
                print("Changes:", file.changes)
                print("Patch:")
                print(file.patch)
                print("################################################################\n")

    
            output_file.write("Pull Request SHA: " + pull_request_sha + "\n")
            output_file.write("Author: "+ login_name + "\n")
            output_file.write("Date: " + str(created_at) + "\n")
            output_file.write("State: " + state + "\n")
            output_file.write("File Change: " + file.filename + "\n")
            output_file.write("Raw Change: \n" + file.patch + "\n\n")
            output_file.write("--------------------------------------------------------\n\n")

        command = f"python solution.py --changefile '{file_path}' --rulefolder ./rules "


# Chạy lệnh bằng subprocess
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #stdout, stderr = process.communicate()



    
def scan_commits(repo, _hash=None, _author=None, _percent=0.0):
    num_commits = 0
    num_commits_violents = 0
    authors_info = check_T3_T5_T6(repo,10,20,30)
    html_content = generate_html_report(repo)
    current_directory = os.path.dirname(__file__)
    html_file_name = "report.html"
    html_file_path = os.path.join(current_directory, html_file_name)
    repo_name = repo.split('/')[-1].replace('.git', '')
    html_content += f"<h2>Repo name: {repo_name}</h2>"
    
    author_trust_status = {}

    html_content += """
    <div>
        <button onclick="toggleAllDetails()">Show All Commits</button>
    </div>
    """

    for commit in Repository(repo).traverse_commits():
            num_commits += 1
            percent_rules_violated = 0
          
            commit_hash = commit.hash
            url_parts = repo.split(".git")
            commit_url = f"{url_parts[0]}/commit/{commit_hash}"
            authored_time = commit.author_date
            authored_by = commit.author.name
            committed_time = commit.committer_date
            committed_by = commit.committer.name
            commit_message = commit.msg
            modified_files = len(commit.modified_files)

            # Lấy thông tin kiểm tra T3 của tác giả
            check_T3_status = authors_info.get(authored_by, {}).get('check_T3', False)
            check_T5_status = authors_info.get(authored_by, {}).get('check_T5', False)
            check_T6_status = authors_info.get(authored_by, {}).get('check_T6', False)

            author_trusted = True

    
            rule1, sensitive_files, total_lines_changed = check_R1(commit)
            rule2_3 = check_R2_R3(commit,repo,0.25)
            rule4 = typical_commit(commit)
            num_rules_checked = 4
            num_rules_violated = 0
            if not author_trusted:
                num_rules_violated += 1
            if not rule1:
                num_rules_violated += 1
            if not rule2_3:
                num_rules_violated += 1
            if not rule4:
                num_rules_violated += 1
            percent_rules_violated = (num_rules_violated / num_rules_checked) * 100

            if _percent is not None:
                if percent_rules_violated < float(_percent):
                    continue

            if _hash and commit_hash != _hash:
                continue
            if _author and authored_by !=_author:
                continue
            
            
            print(f"Commit: {commit_hash}")
            print(f"URL: {commit_url}")
            print(f"Authored on {authored_time} by {authored_by}")
            print(f"Committed on {committed_time} by {committed_by}")
            print(f"Commit Message: {commit_message}")
            print(f"This commit modified {modified_files} files.")   

            if sum([check_T3_status, check_T5_status, check_T6_status]) >= 2:
                print(f"{authored_by} is Trusted")
                html_content += f"""
                <div class="commit-details" style="display: none;">
                    <h2>Commit: {commit_hash}</h2>
                    <a href="{commit_url}">URL: {commit_url}</a>
                    <p>Authored on {authored_time} by {authored_by}</p>
                    <p>Committed on {committed_time} by {committed_by}</p>
                    <p>Commit Message: {commit_message}</p>
                    <p>This commit modified {modified_files} files.</p>
                    <p>{authored_by} is Trusted</p>
                    <p>{percent_rules_violated}% of Rules were Violated</p>
                    <hr>
                </div>
                """
                author_trust_status[authored_by] = "trusted"

            else:
                print( f"{authored_by} is Untrusted")
                html_content += f"""
                <div class="commit-details" style="display: none;">
                    <h2>Commit: {commit_hash}</h2>
                    <a href="{commit_url}">URL: {commit_url}</a>
                    <p>Authored on {authored_time} by {authored_by}</p>
                    <p>Committed on {committed_time} by {committed_by}</p>
                    <p>Commit Message: {commit_message}</p>
                    <p>This commit modified {modified_files} files.</p>
                    <p>{authored_by} is Untrusted</p>
                    <p>{percent_rules_violated}% of Rules were Violated</p>
                    <hr>
                </div>
                """
                author_trust_status[authored_by] = "untrusted"
                author_trusted = False
            
            if percent_rules_violated >= 50:
                num_commits_violents += 1
            print_sensitive_files(sensitive_files, total_lines_changed)
            print(f"{percent_rules_violated}% of Rules were Violated")
            print()      
            print()
    
    html_content += f"<h2>{num_commits_violents}/{num_commits} Commit were violated </h2>"
    html_content += "<h2>Authors Trust Status</h2>"
    html_content += "<table border='1'>"
    html_content += "<tr><th>Author</th><th>Trust Status</th></tr>"
    for author, status in author_trust_status.items():
        html_content += f"<tr><td>{author}</td><td>{status}</td></tr>"
    html_content += "</table>"

    html_content += """
    </body>
    </html>
    """

    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)


def get_user_name(repo_url):
    repo_url= str(sys.argv[2])
    parts = repo_url.split("/")
    username = parts[3]
    return username

def get_repo_name(repo_url):
    repo_name = repo_url.split('/')[-1].split('.git')[0]
    return repo_name

token = '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'


def check_T2(author_commits_list,author_name, repo_name):
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url=f"https://api.github.com/repos/{author_name}/{repo_name}/contributors", headers=headers)
    if response.status_code == 200:
        contributors = response.json()
        for contributor in contributors:
            login_name = contributor.get('login')
            response = requests.get(url=f"https://api.github.com/users/{login_name}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                created_at = data.get('created_at', '')

                    # Chuyển đổi chuỗi ngày tạo thành đối tượng datetime
                created_at_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')

                # Kiểm tra xem tài khoản có được tạo trong vòng 30 ngày gần đây không
                if created_at_date >= datetime.now() - timedelta(days=30):
                    print(f"Cảnh báo: Tài khoản của tác giả {login_name} đã được tạo trong vòng 30 ngày gần đây.")
                else:
                    print(f"{login_name} is trusted")
            else: 
                print(f"Can not find account {login_name}")
            
from collections import Counter

def check_T3_T5_T6(repo, threshold_T3, threshold_T5, threshold_T6):
    author_commits = get_author_commits(repo)
    violated_authors_T5 = []
    violated_authors_T6 = []

    for author, data in author_commits.items():
        commits = data['commits']
        commit_dates = [commit[1] for commit in commits]
        daily_commits_count = Counter(commit_dates)
        total_commits = len(commits)

        for daily_commits in daily_commits_count.values():
            if daily_commits / total_commits >= threshold_T5 / 100:
                violated_authors_T5.append(author)
                break
        
        if len(commits) < threshold_T3:
            data['check_T3'] = False           
        else:
            data['check_T3'] = True

        # Check T6
        sorted_commits = sorted(commits, key=lambda commit: commit[1])
        for i in range(1, len(sorted_commits)):
            commit_time_diff = sorted_commits[i][1] - sorted_commits[i-1][1]
            if commit_time_diff >= timedelta(days=threshold_T6):
                violated_authors_T6.append(author)
                break
      

    if violated_authors_T5:
        for author in violated_authors_T5:          
            author_commits[author]['check_T5'] = False

    if violated_authors_T6:
        for author in violated_authors_T6:
            author_commits[author]['check_T6'] = False


    return author_commits

 
def check_T7(repo_name, user_name):
    headers = {'Authorization': f'token {token}'}
    response = requests.get(f'https://api.github.com/repos/{user_name}/{repo_name}/pulls?state=closed', headers=headers)

    if response.status_code == 200:
        pulls = response.json()    
        user_pulls = {}
        user_rejected_pulls = {}
        for pull in pulls:
            #pull_request_hash = pull['head']['sha']
            if 'user' in pull:
                user_login = pull['user']['login']
                if user_login in user_pulls:
                    user_pulls[user_login] += 1
                else:
                    user_pulls[user_login] = 1

                if pull['state'] == 'closed' and pull['merged_at'] is None:
                    if user_login in user_rejected_pulls:
                        user_rejected_pulls[user_login] += 1
                    else:
                        user_rejected_pulls[user_login] = 1
            else:
                print("Pull request is missing user information.")
        
        # In ra tỷ lệ từ chối (T7) của mỗi người dùng
        for user, count in user_pulls.items():
            rejected_pulls = user_rejected_pulls.get(user, 0)
            rejection_rate = (rejected_pulls / count) * 100 if count > 0 else 0
            #print(f'Hash: {pull_request_hash}')
            print(f'User: {user}, Total Pull Requests: {count}, Rejected Pull Requests: {rejected_pulls}, Rejection Rate: {rejection_rate:.2f}%')
    else:
        print(f'Failed to fetch data. Status code: {response.status_code}')

def get_login_name():
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url=f"https://api.github.com/users/{author}", headers=headers)

def get_author_commits(repository):
    author_commits = {}  # A dictionary to hold the author names and their commits
    
    for commit in Repository(repository).traverse_commits():
        author_name = commit.author.name
        commit_time = commit.committer_date  # get commit time
        
        if author_name not in author_commits:
            author_commits[author_name] = {'commits': [], 'check_T3': False, 'check_T5': True, 'check_T6': True}

            
        # Add the commit hash and commit time to the list of this author's commits
        author_commits[author_name]['commits'].append((commit.hash, commit_time,commit.modified_files))
    
    return author_commits

    
#R1
def is_sensitive_file(file_path):
    sensitive_file_extensions = ['.xml', '.json', '.jar', '.ini', '.dat', '.cnf', '.yml', '.toml',
                             '.gradle', '.bin', '.config', '.exe', '.properties', '.cmd', '.build']
    # Kiểm tra xem tập tin có phải là tập tin nhạy cảm không dựa trên phần mở rộng của tên tập tin
    for ext in sensitive_file_extensions:
        if file_path.endswith(ext):
            return True
    return False
#R1 (check sensitive File)
def check_R1(commit):
    sensitive_files = []
    total_lines_changed = 0

    for modified_file in commit.modified_files:
        file_path = modified_file.new_path
        if file_path and is_sensitive_file(file_path):
            sensitive_files.append((file_path, modified_file.added_lines + modified_file.deleted_lines))
            total_lines_changed += modified_file.added_lines + modified_file.deleted_lines
    return not bool(sensitive_files), sensitive_files, total_lines_changed

def print_sensitive_files(sensitive_files, total_lines_changed):
    if sensitive_files:
        print(f"The commit changed {len(sensitive_files)} potentially 'sensitive' files:")
        if total_lines_changed == 0:
            print("No lines changed in sensitive files.")
        else:
            for file_path, lines_changed in sensitive_files:
                proportion = lines_changed / total_lines_changed * 100
                print(f"{file_path} - MODIFY - commit proportion: {proportion:.2f}%")
    else:
        print("The commit did not change any potentially 'sensitive' files.")


#R2,3
contributor_files_cache = {}

def check_R2_R3(commit, repo,threshold):
    contributor = commit.author.name
    touched_files = commit.modified_files
    touched_file_count = len(touched_files)

    # Kiểm tra xem danh sách đã được lưu trữ trong cache chưa
    if contributor in contributor_files_cache:
        contributor_files = contributor_files_cache[contributor]
    else:
        # Nếu chưa, lấy danh sách các tệp đã thay đổi bằng cách duyệt qua các commit
        contributor_files = set()
        for commit in Repository(repo).traverse_commits():
            if commit.author.name == contributor:
                for modification in commit.modified_files:
                    contributor_files.add(modification.filename)
        # Lưu trữ danh sách vào cache để sử dụng cho các lần kiểm tra sau
        contributor_files_cache[contributor] = contributor_files

    contributor_file_count = len(contributor_files)
    threshold_count = int(contributor_file_count * threshold)

    if touched_file_count > threshold_count:
        return False
    else:
        return True

def calculate_hunks(modified_files):
    total_hunks = 0
    for modified_file in modified_files:
        # Số dòng mã mới
        new_loc = modified_file.added_lines
        # Số dòng mã cũ
        old_loc = modified_file.deleted_lines

        # Tính delta
        delta = new_loc - old_loc

        # Ngưỡng để xác định số lượng hunks (ví dụ: 10)
        threshold = 10

        # Tính số lượng hunks
        hunks = delta // threshold
        total_hunks += hunks

    return total_hunks

#R4 
def typical_commit(commit):
        files = commit.files
        lines = commit.lines
        hunks = calculate_hunks(commit.modified_files)
        if (files >= 2 and files <= 4) or (lines <= 50 or hunks <=8):          
                return True
        else:
            return False
      



def main():
    parser = argparse.ArgumentParser(description=' App Description')

    # Add your command-line options here
    # For example:
    # parser.add_argument('--input', help='Input file path')
    # parser.add_argument('--output', help='Output file path')
    parser.add_argument('-nloc', help='Extract number of lines of code (NLoC)')
    parser.add_argument('-changes', help='Extract changed lines of code')
    parser.add_argument('-onl',help='Input file url')
    parser.add_argument('-hash', help='Display specific commit')
    parser.add_argument('-author',help='author name')
    parser.add_argument('-pullreq',help='Check pull request')
    parser.add_argument('-percent',help='violated rate')
    parser.add_argument('-gcf',help="Get changed file")
    parser.add_argument('-cfpullreq',help="Check File change in pull request")
    args = parser.parse_args()

    if args.nloc:
        extract_nloc(args.onl)
    if args.changes:
        repo= str(sys.argv[2])
        extract_changed_lines(repo,args.hash)  
    if args.gcf:
        repo=str(sys.argv[2])
        get_changed_file(repo,args.hash)    
    if args.onl:
        scan_commits(args.onl,args.hash,args.author,args.percent)
    if args.pullreq:
        repo= str(sys.argv[2])
        check_T7(get_repo_name(repo),get_user_name(repo)) 
    if args.cfpullreq:
        repo= str(sys.argv[2])
        check_changed_file_pullreq(repo,args.hash,args.author) 

if __name__ == "__main__":
    main()