from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the pretrained emotion model and tokenizer
def load_emotion_model():
    model_name = "joeddav/distilbert-base-uncased-go-emotions-student"
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

# Emotion classification map
emotion_map = {0: "admiration", 1: "amusement", 2: "anger", 3: "annoyance", 4: "approval", 5: "caring", 
               6: "confusion", 7: "curiosity", 8: "desire", 9: "disappointment", 10: "disgust", 11: "embarrassment", 
               12: "excitement", 13: "fear", 14: "gratitude", 15: "grief", 16: "joy", 17: "love", 18: "nervousness", 
               19: "optimism", 20: "pride", 21: "relief", 22: "remorse", 23: "sadness", 24: "surprise", 
               25: "sympathy", 26: "thankfulness", 27: "neutral"}

# Predict emotion based on the user input
def predict_emotion(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return emotion_map.get(predicted_class, "unknown")

