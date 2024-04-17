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

![image](https://github.com/minhha273/Comalicious/assets/93338351/83ca0221-374d-4b1d-97ae-5e194ee541d6)

It will scan pullrequests through the rules to check if any of our rules are violated. Then it will output the report output.html file

![image](https://github.com/minhha273/Comalicious/assets/93338351/27cbcd45-d8c0-4d93-8dc0-811bead431eb)

## Get file contains all file changes in commit
```
python FMalGit.py -changes $github_link -hash $commit_hash
```
where
- `$github_link`: github repository link
### Example
```
python FMalGit.py -changes https://github.com/minhha273/project -hash 0da38b34e8bae189f41b42caa99b34c748b6d7dc
```
![image](https://github.com/minhha273/Comalicious/assets/93338351/0317c2cc-bf51-40f9-95d7-31ca9e7f7499)


