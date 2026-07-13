from flask import Flask, request, jsonify
from database import db
from models import Course

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///courses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.post("/api/courses")
def create_course():

    data = request.json

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "id": course.id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits
    }), 201


@app.get("/api/courses/<int:id>")
def get_course(id):

    course = Course.query.get(id)

    if course is None:
        return jsonify({"error":"Course not found"}),404

    return jsonify({
        "id":course.id,
        "name":course.name,
        "code":course.code,
        "credits":course.credits
    })


if __name__=="__main__":
    app.run(port=5001,debug=True)