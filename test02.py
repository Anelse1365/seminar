from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html',title='home')
@app.route('/hello/<name>')
def hello_name(name):
    name = "fk"
    return render_template('hello.html',title='hello_name',name=name)
if __name__ == '__main__':
    app.run(debug=True)