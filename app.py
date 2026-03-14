from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define the root route
@app.route("/")
def home():
    return "<h1>Hello, World!</h1><p>This is my first DevOps-powered Flask app.</p>"

if __name__ == "__main__":
    # Run the application in debug mode
    app.run(debug=True)
