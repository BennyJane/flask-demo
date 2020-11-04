from flask import Flask, views, request

app = Flask(__name__)
app.config['FLASK_ENV'] = "development"


class baseView(views.MethodView):

    def get(self, age):
        return "base view"

    def post(self):
        res = request.form
        return "base view post"


app.add_url_rule('/base/<int:age>', view_func=baseView.as_view("base"))
if __name__ == '__main__':
    # app.run(debug=True)
    b = views.MethodView()
    print(b.__class__)
    print(type(b))
    print(b.__class__.__class__)
    print(b.__class__.__class__.__class__)
