import pickle
import re
from pathlib import Path

__version__ = "0.1.0"

# base directory: current file's parent = 'model'
# remove symlink through resolve()
BASE_DIR = Path(__file__).resolve(strict=True).parent

with open(f"{BASE_DIR}/trained_pipeline-{__version__}.pkl", "rb") as f:
    model = pickle.load(f)

# classes to return using predicted category index
classes = [
    "Arabic",
    "Danish",
    "Dutch",
    "English",
    "French",
    "German",
    "Greek",
    "Hindi",
    "Italian",
    "Kannada",
    "Malayalam",
    "Portugeese",
    "Russian",
    "Spanish",
    "Sweedish",
    "Tamil",
    "Turkish",
]


def preprocess_text(text: str) -> str:
    """
    preprocess text by removing special characters or numbers
    and lowering letters
    """
    text = re.sub(r'[!@#$(),\n"%^*?\:;~`0-9]', " ", text)
    text = re.sub(r"[[]]", " ", text)
    text = text.lower()
    return text


def predict_pipeline(text: str) -> str:
    """
    Predict the language for the given text
    """
    text = preprocess_text(text)
    pred = model.predict([text])
    return classes[pred[0]]
