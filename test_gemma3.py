import subprocess

# Function to run the gemma3 model and get output

def run_gemma3(input_text):
    try:
        # Run the model using subprocess
        result = subprocess.run(
            ['ollama', 'run', 'gemma3:1b'],
            input=input_text,
            capture_output=True,
            text=True,
            encoding='utf-8'  # Specify utf-8 encoding
        )
        
        # Return the output from the model
        return result.stdout
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Test the model with dynamic input
def main():
    while True:
        input_text = input("Enter your message for Gemma (or type 'exit' to quit): ")
        if input_text.lower() == 'exit':
            break
        output = run_gemma3(input_text)
        print("Model Output:", output)

if __name__ == "__main__":
    main()
