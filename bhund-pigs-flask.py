from flask import Flask, request, abort
from bhund_backend_pigs import authorise_with_email, authorise_with_session_id, get_pig_by_id, getall_pigs, modify, delete_pig, insert_pig
from bhund_backend_class import user, sessions, credentials, populate_credential_with_json, populate_pigs_with_json, populate_session_with_json, populate_user_with_json

app = Flask(__name__)


def auth():
    header = request.headers
    session_id = header.get('session_id')
    return authorise_with_session_id(session_id)

@app.route('/pigs')
def get_all_pigs():
    if auth():
        return getall_pigs()
    else:
        abort(401)

@app.route('/pigs/<id>')
def get_pig(id):
    if auth():
        return get_pig_by_id(id)
    else:
        abort(401)

@app.route('/pigs/<id>', methods= ['DELETE'])
def delete(id):
    if auth():
        return delete_pig(id)
    else:
        abort(401)

@app.route('/pigs/<id>', methods= ['PATCH'])
def modify_pig(id):
    if auth():
        incoming_json = request.json
        pig = populate_pigs_with_json(incoming_json)
        pig.id = id
        return modify(pig)
    else:
        abort(401)


@app.route('/pigs', methods= ['POST'])
def add_pig():
    if auth():
        incoming_json = request.json
        pig = populate_pigs_with_json(incoming_json)
        return insert_pig(pig)
    else:
        abort(401)



@app.route('/fetch')
def authorise_user():
    auth = request.authorization
    credential = credentials(auth.username, auth.password)
    if(authorise_with_email(credential)):
        return {"Status" : "Authorised User"}
    else:
        abort(401)


if __name__ == "__main__":
    app.run()