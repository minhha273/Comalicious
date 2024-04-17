# Preparing
Move to project folder
```
cd Comalicious
```
# Installation
Use the package manager pip to install needed library in `requirements.txt`.
```
pip install -r requirements.txt
```
# Usage
## Scan commits
```
python FMalGit.py -onl $github_link
```
where
- `$github_link`: github repository link
### Example
```
python FMalGit.py -onl https://github.com/minhha273/project
```
Here is the content of :
![image](https://github.com/minhha273/Comalicious/assets/93338351/912ceab7-85c2-4e24-8acc-c583b7291f83)

## Get file contains all pull-request
```
python FMalGit.py -cfpullreq $github_link
```
where
- `$github_link`: github repository link
### Example
```
python FMalGit.py -cfpullreq https://github.com/minhha273/project
```
Here is the content of :

![alt text](images/image.png)

## Export to file
```
python solution.py --changefile $change_file_path --rulefolder $rules_folder_path --outputfile $output_path
```
where
- `$change_file_path`: path of the change pull file
- `$rules_folder_path`: path of the folder contains all file rules
- `$output_path`: path of output file (default: `./output.txt`)

## Example
### Export output with indicated output file
```
python solution.py --changefile '.\change_file_pull\project_change_pull.txt' --rulefolder .\rules --outputfile ./output1.txt
```
Here is result:
![alt text](images/output1.png)

### Export output with default output file
```
python solution.py --changefile '.\change_file_pull\project_change_pull.txt' --rulefolder .\rules
```
Here is result:
![alt text](images/output.png)
