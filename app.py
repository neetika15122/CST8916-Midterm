# Import necessary modules from Flask
# Flask: the core framework for the web app
# jsonify: to convert Python dictionaries to JSON responses
# request: to access incoming request data (e.g., POST data)
# abort: to handle errors and send error status codes
from flask import Flask, jsonify, request, abort

# Initialize the Flask app
app = Flask(__name__)

# In-memory "database" of students
# This list holds a set of user dictionaries. 
# In a real-world application, this would be replaced by a database such as MySQL, PostgreSQL, or MongoDB.
students = [
    {"id": 1, "name": "Neetika", "grade": "A", "email": "Neetika@example.com"},
    {"id": 2, "name": "Parth", "grade": "B", "email": "Parth@example.com"},
]

# Define route to handle requests to the root URL ('/')
@app.route('/')
def index():
    return "Welcome to Flask REST API Demo! Try accessing /students to see all students."

# Health check route (GET)
# This endpoint returns a 200 OK status and a JSON response to confirm that the service is running.
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200  # Return HTTP status 200 OK

# Route to retrieve all students (GET request)
# When the client sends a GET request to /students, this function will return a JSON list of all students.
# The @ symbol in Python represents a decorator. 
# In this case, @app.route is a Flask route decorator.
# It is used to map a specific URL (route) to a function in your Flask application.
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200  # 200 is the HTTP status code for 'OK'

# Route to retrieve a single user by their ID (GET request)
# When the client sends a GET request to /students/<id>, this function will return the user with the specified ID.
@app.route('/students/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Using a list comprehension to find the user by ID
    user = next((user for user in students if user['id'] == user_id), None)
    if user is None:
        abort(404)  # If the user is not found, return a 404 error (Not Found)
    return jsonify(user), 200  # Return the user as a JSON object with a 200 status code (OK)

# Route to create a new user (POST request)
# When the client sends a POST request to /students with user data, this function will add the new user to the list.
@app.route('/students', methods=['POST'])
def create_user():
    # If the request body is not in JSON format or if the 'name' field is missing, return a 400 error (Bad Request)
    if not request.json or not 'name' in request.json:
        abort(400)
    
    # Create a new user dictionary. Assign the next available ID by incrementing the highest current ID.
    # If no students exist, the new ID will be 1.
    new_user = {
        'id': students[-1]['id'] + 1 if students else 1,
       'name': request.json['name'],
        'grade': request.json.get('grade', 'Not Assigned'),
        'email': request.json['email']
    }
    # Add the new user to the students list
    students.append(new_user)
    return jsonify(new_user), 201  # 201 is the HTTP status code for 'Created'

# Route to update an existing user (PUT request)
# When the client sends a PUT request to /students/<id> with updated user data, this function will update the user.
@app.route('/students/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Find the user by their ID
    user = next((user for user in students if user['id'] == user_id), None)
    if user is None:
        abort(404)  # If the user is not found, return a 404 error (Not Found)
    
    # If the request body is missing or not in JSON format, return a 400 error (Bad Request)
    if not request.json:
        abort(400)
    
    # Update the user's data based on the request body
    # If a field is not provided in the request, keep the existing value
    user['name'] = request.json.get('name', user['name'])
    user['grade'] = request.json.get('grade', user['grade'])
    user['email'] = request.json.get('email', user['email'])
    return jsonify(user), 200  # Return the updated user data with a 200 status code (OK)

# Route to delete a user (DELETE request)
# When the client sends a DELETE request to /students/<id>, this function will remove the user with that ID.
@app.route('/students/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global students  # Reference the global students list
    # Rebuild the students list, excluding the user with the specified ID
    students = [user for user in students if user['id'] != user_id]
    return '', 204  # 204 is the HTTP status code for 'No Content', indicating the deletion was successful

# Entry point for running the Flask app
# The app will run on host 0.0.0.0 (accessible on all network interfaces) and port 8000.
# Debug mode is disabled (set to False).
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)