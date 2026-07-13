from flask import Flask, request, jsonify
from database import db
from models import Student, Enrollment
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.post("/api/students")
def create_student():

    data=request.json

    student=Student(
        name=data["name"],
        email=data["email"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "id":student.id,
        "name":student.name,
        "email":student.email
    }),201


@app.get("/api/students/<int:id>")
def get_student(id):

    student=Student.query.get(id)

    if student is None:
        return jsonify({"error":"Student not found"}),404

    return jsonify({
        "id":student.id,
        "name":student.name,
        "email":student.email
    })

@app.post("/api/students/<int:id>/enroll")
def enroll(id):
    student = Student.query.get(id)

    if student is None:
        return jsonify({
            "error":"Student not found"
        }),404
    
    data = request.json
    course_id = data["course_id"]
    try:
        response = requests.get(f"http://localhost:5001/api/courses/{course_id}")

        if response.status_code == 404:
            return jsonify({
        "error":"Course not found"}),404

        enrollment = Enrollment(student_id=id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({"message":"Enrollment successful"})
    except requests.exceptions.ConnectionError:
        return jsonify({"error":"Course Service is unavailable"}),503


if __name__=="__main__":
    app.run(port=5002,debug=True)
