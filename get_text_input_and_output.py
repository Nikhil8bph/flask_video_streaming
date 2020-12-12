from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('myform.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return myform_thanks()

@app.route('/thank_you')
def myform_thanks():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)