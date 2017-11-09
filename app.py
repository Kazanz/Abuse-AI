import pickle
import re

from apispec import APISpec
from flask import Flask, render_template, send_from_directory, jsonify
from flask_apispec import use_kwargs, marshal_with, annotations
from flask_apispec.extension import FlaskApiSpec
from marshmallow import fields, Schema



app = Flask(__name__,  static_url_path='/static')
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Abuse AI',
        version='v1',
        plugins=['apispec.ext.marshmallow'],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})




class EmailClassification():
    def __init__(self, subject='', body=''):
        self.ips = []
        self.extract_ips(subject)
        self.extract_ips(body)
        self.predict(body)

    def extract_ips(self, text):
        ips = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)
        self.ips += ips

    def predict(self, body):
        with open('model.pickle', 'rb') as f:
          vectorizer, model = pickle.load(f)

        X_new = vectorizer.transform([body])
        classes, pred = model.classes_.tolist(), model.predict_proba(X_new).tolist()[0]
        self.confidence = dict(zip(classes, pred))
        self.predicted = classes[pred.index(max(pred))]


class ClassificationSchema(Schema):
    ips = fields.List(fields.Str())
    type = fields.Dict()

    class Meta:
        fields = ('ips', 'confidence', 'predicted')


class ValidationError(Exception):
    status_code = 400

    def __init__(self, errors, status_code=None, payload=None):
        Exception.__init__(self)
        self.errors = errors
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['errors'] = self.errors
        return rv


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def validate(kwargs):
    errors = {}
    if not kwargs.get('subject'):
        errors['subject'] = 'This field is required'
    if not kwargs.get('body'):
        errors['body'] = 'This field is required'
    if errors:
        raise ValidationError(errors)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/api/email', methods=['POST'])
@use_kwargs({'subject': fields.Str(), 'body': fields.Str()})
@marshal_with(ClassificationSchema())
@annotations.doc(tags=['Email Classification'], description="""
    For more info visit the repo on Github: https://github.com/Kazanz/Abuse-AI
""")
def classify_email(**kwargs):
    validate(kwargs)
    return EmailClassification(**kwargs) 


docs = FlaskApiSpec(app)
docs.register(classify_email)
