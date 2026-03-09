import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load .env file

MODEL_DIR = Path(__file__).parent / "model" / "final_sinhala_mood_model"

# Check if ML model loading should be skipped
SKIP_ML_MODEL = os.getenv("SKIP_ML_MODEL", "false").lower() == "true"

tokenizer = None
model = None
device = None
id2label = {0: "Bad", 1: "Normal", 2: "Happy"}

if not SKIP_ML_MODEL:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    
    # device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # load
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model = model.to(device)
    model.eval()
    
    # labels
    raw_id2label = model.config.id2label
    id2label = {int(k): v for k, v in raw_id2label.items()} if isinstance(list(raw_id2label.keys())[0], str) else raw_id2label
    
    fallback = {0: "Bad", 1: "Normal", 2: "Happy"}
    if any(str(v).startswith("LABEL_") for v in id2label.values()):
        id2label = fallback


def predict_with_probs(text: str):
    text = text.strip()
    if not text:
        return {
            "mood": "Unknown",
            "confidence": 0.0,
            "probs": {}
        }
    
    # Return placeholder when model is not loaded
    if SKIP_ML_MODEL or model is None:
        return {
            "mood": "Normal",
            "confidence": 0.0,
            "probs": {"Bad": 0.0, "Normal": 0.0, "Happy": 0.0},
            "warning": "ML model not loaded"
        }

    import torch
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1).squeeze(0)

    pred_id = int(torch.argmax(probs).item())
    confidence = float(probs[pred_id].item())
    probs_dict = {id2label[i]: float(probs[i].item()) for i in range(probs.shape[0])}

    return {
        "mood": id2label.get(pred_id, str(pred_id)),
        "confidence": confidence,
        "probs": probs_dict
    }
