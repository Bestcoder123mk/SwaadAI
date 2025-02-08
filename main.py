from boltiotai import openai
import os
from flask import Flask, request, render_template_string

# Get API key from environment variables
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("ERROR: Missing OpenAI API Key. Set OPENAI_API_KEY in your environment variables.")

openai.api_key = api_key

def generate_tutorial(components):
    if not components:
        return "Error: No ingredients provided."

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Suggest a recipe using {components}. Include step-by-step instructions, ingredient quantities, and a recipe name."}]
        )

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error in OpenAI API call: {str(e)}"




app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    output = ""
    if request.method == 'POST':
        components = request.form.get('components', '')
        output = generate_tutorial(components)

    return render_template_string(''' 
    <!DOCTYPE html>
    <html>
    <head>
        <title>Recipe Generator</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1 class="my-4">Custom Recipe Generator</h1>
            <form id="tutorial-form" onsubmit="event.preventDefault(); generateTutorial();" class="mb-3">
                <div class="mb-3">
                    <label for="components" class="form-label">Type the ingredients or any recipe name:</label>
                    <input type="text" class="form-control" id="components" name="components" placeholder="Enter the ingredients or a recipe name..." required>
                </div>
                <button type="submit" class="btn btn-primary">Send to SwaadAI</button>
            </form>
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    Output:
                    <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy</button>
                </div>

                <div class="card-body">
                    <p id="output" style="white-space: pre-wrap;">{{ output }}</p>
                </div>
             <footer>
             <hr></hr>
             <h6>Made by Anirudh Melkaveri</h6>
             </footer>
            </div>
        </div>
       
        <script>
        async function generateTutorial() {
            const components = document.querySelector('#components').value;
            const output = document.querySelector('#output');
            output.textContent = 'Generating a recipe for you...';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: new FormData(document.querySelector('#tutorial-form'))
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch');
                }

                const recipe = await response.text();
                output.textContent = recipe;
            } catch (error) {
                output.textContent = 'Error generating recipe: ' + error.message;
            }
        }

        function copyToClipboard() {
            const recipeText = document.getElementById('output').textContent;
            const textarea = document.createElement('textarea');
            textarea.value = recipeText;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('Copied to clipboard');
        }
        </script>
    </body>
    </html>
    ''', output=output)

@app.route('/generate', methods=['POST'])
def generate():
    components = request.form.get('components', '')
    return generate_tutorial(components)


if __name__ == '__main__':            
    app.run(host='0.0.0.0', port=8080, debug=True)


