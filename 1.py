try:

    from flask import Flask, request,\
        render_template,\
        redirect, url_for, session, send_file
    from package import GithubHunter
    from flask_wtf import FlaskForm

    from wtforms import StringField, SubmitField
    from io import BytesIO
    import io
    from flask_wtf.file import FileField
    from wtforms.validators import DataRequired

except Exception as e:

    print("Some Modules are Missing {}".format(e))

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"


class MyForm(FlaskForm):

    name = StringField(label='Github username')
    button = SubmitField(label="Submit")



class FormDownload(FlaskForm):
    download =SubmitField(label = 'download')


@app.route("/", methods=("GET", "POST"))
def home():


    form = MyForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            session["username"] = form.name.data
            return redirect(url_for('result'))

    if request.method == 'GET':
        return render_template('home.html', form=form)


@app.route("/result", methods=("GET", "POST"))

def result():

    form = FormDownload()
    hunter = GithubHunter(username = session["username"], pages=2)
    df = hunter.run()
    data = list(zip(df["Repo Name"].to_list(), df["url"].to_list()))

    if request.method == 'POST':
        towrite = io.BytesIO()
        df.to_excel(towrite)
        towrite.seek(0)
        return send_file(BytesIO(towrite.getvalue()), attachment_filename="repo.xlsx", as_attachment=True)

    return render_template('result.html', data=data, form=form)


if __name__ == "__main__":
    app.run(debug=True)