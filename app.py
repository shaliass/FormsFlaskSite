from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for('form'))

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        num = request.form.get('num', '').strip()
        cvv = request.form.get('cvv', '').strip()
        expDate = request.form.get('expDate', '').strip()
        mName = request.form.get('mName', '').strip()
        con = request.form.get('con', '').strip()
        ungaBunga = request.form.get('ungaBunga') == "yes"  # true if checked

        # validation
        if not name or not num or not cvv or not expDate or not mName or not con:
            error = "please fill in all required fields"
            return render_template('defaultForm.html', error=error)

        return render_template(
            'formSuccess.html',
            name=name,
            num=num,
            cvv=cvv,
            expDate=expDate,
            mName=mName,
            con=con,
            ungaBunga=ungaBunga
        )
    return render_template('defaultForm.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')