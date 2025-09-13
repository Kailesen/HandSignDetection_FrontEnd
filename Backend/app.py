from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import pickle
import os

MODEL_PATH = os.path.join("Backend", "artifacts", "best_gesture_model.h5")
LABEL_ENCODER_PATH = os.path.join("Backend", "artifacts", "label_encoder.pkl")

app = Flask(__name__)
CORS(app)  # Allow requests from the browser (localhost)

# Load model + label encoder at startup (only once)
print("[INFO] Loading model and label encoder...")
model = tf.keras.models.load_model(MODEL_PATH)
with open(LABEL_ENCODER_PATH, "rb") as f:
    le = pickle.load(f)
print("[INFO] Model loaded.")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Expect JSON body: { "features": [[f1,...,f126], [f1,...,f126], ...] }
    Where the outer array length == SEQ_LEN (e.g., 30).
    """
    data = request.get_json()
    seq = data.get("features") or data.get("sequence")
    if seq is None:
        return jsonify({"error": "No 'features' provided"}), 400

    arr = np.array(seq, dtype=np.float32)
    if arr.ndim != 2:
        return jsonify({"error": "features must be 2D array [frames, features]"}), 400

    # Add batch axis and predict
    input_data = np.expand_dims(arr, axis=0)  # shape (1, seq_len, 126)
    preds = model.predict(input_data)[0]
    idx = int(np.argmax(preds))
    try:
        label = le.inverse_transform([idx])[0]
    except Exception:
        label = str(idx)
    confidence = float(preds[idx]) * 100.0

    return jsonify({"label": label, "confidence": confidence})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Run on port 5000; use 0.0.0.0 to be reachable from other devices if needed
    app.run(host="0.0.0.0", port=5000, debug=True)