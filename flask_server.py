from flask import Flask, jsonify, request
from flask_cors import CORS #CORS gives permission for website to access when running server on local (for testing)
from db import get_db

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

#endpoint to edit cms community page text in the database
@app.route('/edit_community_page_text', methods=['POST'])
def edit_community_page_text():
    db = get_db()
    cursor = db.cursor()

    number = request.json.get('number')
    content = request.json.get('content')

    if number is not None and content is not None:
        # Update statement
        update_query = "UPDATE cmsCommunityPage SET content = %s WHERE number = %s"

        # Execute the update query
        cursor.execute(update_query, (content, number))
        db.commit()

        cursor.close()
        return jsonify({"message": "Data updated successfully"})
    else:
        cursor.close()
        return jsonify({"error": "Invalid request data"})

#endpoint to get cms community page text from database
@app.route('/get_community_page_text', methods=['GET'])
def get_community_page_text():
    db = get_db()  # Use the function from database.py to connect to the database
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM cmsCommunityPage")
        data = cursor.fetchall()
        return jsonify({'data': data})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        #db.close()

if __name__ == '__main__':
    app.run(debug=True, port = 5000)  # Run the Flask app with debug mode enabled
