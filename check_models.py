import google.generativeai as genai

# Replace with your actual API key
genai.configure(api_key="AIzaSyDryuKNhPACwrNApTGCr_fLHxXceKROTHQ")

try:
    models = genai.list_models()
    print("✅ Available Models:")
    for model in models:
        print(f"- {model.name}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
