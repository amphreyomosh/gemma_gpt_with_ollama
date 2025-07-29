from flask import Flask, render_template, request, jsonify
import subprocess
import time
import logging
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

def clean_text(text):
    """Clean up the text by removing markdown formatting and ensuring proper line breaks."""
    if not text:
        return text
    
    # Remove markdown headers (lines starting with #)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    
    # Replace markdown bold/italic with plain text
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    
    # Replace markdown lists with new lines
    text = re.sub(r'^\s*[-*]\s+', '• ', text, flags=re.MULTILINE)
    
    # Ensure consistent line breaks
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
    
    # Replace multiple newlines with a single one
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

# Function to run the gemma3 model and get output
def run_gemma3(input_text):
    try:
        start_time = time.time()
        # Run the model using subprocess
        result = subprocess.run(
            ['ollama', 'run', 'gemma3:1b'],
            input=input_text,
            capture_output=True,
            text=True,
            encoding='utf-8',  # Specify utf-8 encoding
            check=True  # Raise CalledProcessError if command fails
        )
        end_time = time.time()
        logging.debug(f"Model execution time: {end_time - start_time} seconds")
        
        # Clean the output before returning
        return clean_text(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e.stderr}")
        return f"Subprocess error: {e.stderr}"
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def home():
    output = None
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        output = run_gemma3(input_text)
    return render_template('index.html', output=output)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    input_text = data.get('message', '')
    try:
        output = run_gemma3(input_text)
        response_time = 0.5  # Placeholder for actual response time
        return jsonify({'success': True, 'response': output, 'response_time': response_time})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/clear', methods=['GET'])
def clear():
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
