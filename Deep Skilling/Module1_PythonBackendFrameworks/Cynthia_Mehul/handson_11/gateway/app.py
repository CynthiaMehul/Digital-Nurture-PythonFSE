from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/courses", methods=["GET", "POST"])
@app.route("/api/courses/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def course_proxy(path=""):
    url = f"http://localhost:5001/api/courses/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        json=request.get_json(silent=True)
    )
    return (
        response.content,
        response.status_code,
        response.headers.items())

@app.route("/api/students", methods=["GET", "POST"])
@app.route("/api/students/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def student_proxy(path=""):
    url = f"http://localhost:5002/api/students/{path}"
    response = requests.request(
        method=request.method,
        url=url,
        json=request.get_json(silent=True)
    )
    return (
        response.content,
        response.status_code,
        response.headers.items()
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)