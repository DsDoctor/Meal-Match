from SourceCode import init_app
from flask import jsonify
from flask import request
from random import randint
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer


app = init_app()
mail = Mail(app)


# /index can find all route of app
@app.route('/index')
def index():
    return jsonify({rule.endpoint: rule.rule for rule in app.url_map.iter_rules()})


@app.route('/email', methods=['POST'])
def send_code():
    to_mail = request.form.get('email')
    if not to_mail:
        return {'res': False}, 400
    url = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    url = url.dumps(to_mail, salt=app.config['SECURITY_PASSWORD_SALT'])
    for s in ['.', '_', '-']:
        url = url.replace(s, '')
    start = randint(0, 30)
    v_code = url[start:start+6]
    html = f"""
    <p>Welcome Meal Match! Please use this CODE to validate your email:</p>
    <p>{v_code}</p>
    <br>
    <p>Cheers!</p>"""
    msg = Message("Meal Match - Email verification", sender=app.config["MAIL_USERNAME"],
                  # recipients=list(to_mail.email),
                  recipients=[to_mail],
                  html=html)
    mail.send(msg)
    return jsonify({'res': True})


@app.route('/verify', methods=['POST'])
def valid():
    code = request.form.get('code')
    email = request.form.get('email')
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email_code = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
    if code in email_code:
        return {'res': True}
    return {'res': False}


if __name__ == '__main__':
    app.run()
