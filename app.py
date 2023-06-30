from flask import Flask, render_template
import database
import functionalties


app = Flask (__name__)

courses = database.load_courses()

@app.route("/")
def hello_world():
    random_courses = functionalties.generate_courses(courses)
    return render_template("index.html",
                           courses=random_courses)


if __name__ == "__main__":
    app.run(debug=True)
