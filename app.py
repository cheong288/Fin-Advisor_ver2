from flask import Flask, request, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

#load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not found in .env file.")

app = Flask(__name__)

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Get the text prompt from the form
        user_input = request.form["prompt"]
        
        # Get the file from the form (if any)
        uploaded_file = request.files.get("file")

        # Process the file (example: read text content if it's a text file)
        if uploaded_file:
            file_content = uploaded_file.read().decode("utf-8")  # Assuming it's a text file
            user_input += "\n" + file_content  # Append the file content to the prompt
        
        # Send the combined prompt (user input + file content) to the model
        response = model.generate_content(user_input)
        result = response.text

    return render_template("index.html", result=result)

def format_output(text):
    # Example: Convert newlines into HTML <br> for line breaks
    formatted_text = text.replace("\n", "<br>")

    # Example: Add basic HTML tags (if you want to create paragraphs, list items, etc.)
    formatted_text = "<p>" + formatted_text + "</p>"
    
    # You could also format the text into bullet points, numbered lists, etc.
    # Example: Convert '*' into list items:
    formatted_text = re.sub(r"\* (.*)", r"<ul><li>\1</li></ul>", formatted_text)
    
    return formatted_text

if __name__ == "__main__":
    app.run(debug=True)