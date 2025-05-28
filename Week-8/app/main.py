from flask import Flask, request, jsonify
from auth import verify_token
app = Flask(__name__)

@app.route('/')
def public():
    return jsonify({"msg": "This is a public endpoint."})

@app.route('/protected')
def protected():
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.replace("Bearer ", "")
    user = verify_token(token)
    if not user:
        return jsonify({"msg": "Unauthorized"}), 401
    return jsonify({"msg": "Protected resource accessed!", "user": user})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
