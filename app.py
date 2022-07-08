from flask import Flask, render_template, url_for, redirect
import requests
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)

app.config["SECRET_KEY"] = "THISISASECRET"
app.config["GITHUB_CLIENT_ID"] = "ac7b086b464a5226a3c7"
app.config["GITHUB_CLIENT_SECRET"] = "23ec00aabcf7e9acf3fda497c930f2263cb40dcb"

github = oauth.register(
    name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,    
    api_base_url = 'https://api.github.com',    
    client_kwargs = {'scope': '(no scope)'},
)

@app.route('/')
def index():    
    return render_template('info.html')

@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()

    url = "https://api.miro.com/v2/boards/uXjVOHHq3zg%3D/images"

    payload = {
        "data": {
            "url": resp.get('avatar_url'),
            "title": "Sample image"
        },
        "position": {
            "origin": "center",
            "x": 0,
            "y": 0
        },
        "geometry": {"height": 200}
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_JasvcxOKWa_9CPQrdug0NRqI0CI"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(f"\n{response.text}\n")
    
    return "You are successfully logged in using github"


if __name__ == '__main__':
    app.run(debug=True)
