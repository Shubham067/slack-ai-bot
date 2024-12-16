import helpers
import google.generativeai as genai

def load_gemini_model(model):
    genai.configure(api_key=helpers.config("GOOGLE_GEMINI_API_KEY", default = None))
    
    gemini_model = genai.GenerativeModel(model, system_instruction="You are a coding expert who specializes in writing code for various kinds of applications i.e. web, mobile etc.")

    return gemini_model

def chat_with_gemini(message, model="gemini-1.5-flash"):
    gemini_model = load_gemini_model(model)
    response = gemini_model.generate_content(message).text
    
    return response