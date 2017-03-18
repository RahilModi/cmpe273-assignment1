import sys

from github import Github, GithubException
from flask import Flask

splited_url = sys.argv[1].split('//')[1].split('/') #splits url first by '//' and then by delimiter '/'
user_name = splited_url[1] # stroes the username 
repository = splited_url[2] #stores the repo name

gh = Github() #creating Github object
user = gh.get_user(user_name)  #github user based on the username
repo = user.get_repo(repository) #github user repo based on the repository name

app = Flask(__name__)

#route the call for '/' 
@app.route('/')
def hello():
    return 'Hello welcome to docker based flask app'

#route the call for '/v1/<filename>'
@app.route('/v1/<filename>')
def get_File_Contents(filename):
    try:
        ext = filename.split('.')[1]
        if((ext == 'yml') or (ext == 'json')):  #checking file supported file format 'yml' or 'json'
            fileContent = repo.get_file_contents(filename)
            return fileContent.decoded_content
        else: #file format not found error
            return "File format is not valid"
    except GithubException, exception:
        if(exception.status == 404): #handling for unknown file error
            return 'Unknown Object Exception .... File Not found under user : {}\'s Github Repository : {}.'.format(user_name,repository)
        else: #else for any other unhandeled error
            return "Unhandled Exception occurred"
    except IndexError: #index error handling
        return "File extention is not given in the URL"    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
