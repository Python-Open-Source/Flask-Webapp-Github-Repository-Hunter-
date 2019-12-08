try:

    from flask import Flask, request, render_template
    from package import GithubHunter
except Exception as e:
    print("Some Modules are Missing {}".format(e))

app = Flask(__name__)


@app.route("/")
def home():

    hunter = GithubHunter(username = "soumilshah1995", pages=2)
    df = hunter.run()
    data = list(zip(df["Repo Name"].to_list(), df["url"].to_list()))

    return render_template('home.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)