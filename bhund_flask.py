from flask import Flask, request, abort, send_from_directory, render_template
from bhund_backend_class import user, credentials, populate_credential_with_json, populate_session_with_json, populate_user_with_json
from bhund_backend_sql import login, getall_users, get_user_by_email, set_user, delete_user, patch_user, logout_user

app = Flask(__name__, static_folder='', template_folder='', static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def get_all():
    return getall_users()


@app.route('/users/<email>')
def get_user(email):
    return get_user_by_email(email)


@app.route('/users/signup', methods= ['POST'])
def signup_user():
    request_data = request.json
    user1 = populate_user_with_json(request_data)
    return set_user(user1)


@app.route('/users/logout/<session_id>', methods= ['DELETE'])
def logout(session_id):
    return logout_user(session_id)


@app.route('/users/<email>', methods= ['DELETE'])
def delete(email):
    return delete_user(email)


@app.route('/users/<email>', methods= ['PATCH'])
def modify(email):
    request_data = request.json
    user1=populate_user_with_json(request_data)
    user1.email_id = email
    return patch_user(user1)


@app.route('/users/login', methods=['POST'])
def user_login():
    request_credentials = request.json
    credential1 = populate_credential_with_json(request_credentials)
    return login(credential1)


if __name__ == "__main__":
    app.run()
