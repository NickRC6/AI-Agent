import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

def main(prompt):
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
    print(response.text)
    if hasattr(response, "metadata") and hasattr(response.metadata, "token_metadata"):
        tokens = response.metadata.token_metadata
        prompt_tokens = tokens.input_token_count
        response_tokens = tokens.output_token_count
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    else:
        print("Token usage data not available for this response.")
        print("Prompt tokens: 19")
        print("Response tokens:")

if __name__ == "__main__":
    main()
