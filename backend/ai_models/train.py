import numpy as np
import tensorflow as tf
import os
import sys

# Ensure backend root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fuzzy_logic.fuzzy_system import compute_fuzzy_score
from ai_models.nn_model import build_model, MODEL_PATH

def generate_synthetic_data(num_samples=2000):
    np.random.seed(42)
    attendance = np.random.randint(0, 101, num_samples)
    assignment = np.random.randint(0, 101, num_samples)
    test = np.random.randint(0, 101, num_samples)
    
    X = []
    y = []
    
    for i in range(num_samples):
        att = attendance[i]
        assgn = assignment[i]
        tst = test[i]
        fuzz_score = compute_fuzzy_score(att, assgn, tst)
        
        # Determine the label combining factors
        combined = (att + assgn + tst + fuzz_score) / 4.0
        
        # Add slight noise
        noise = np.random.normal(0, 5)
        combined += noise
        
        if combined < 40:
            label = 0 # Poor
        elif combined < 70:
            label = 1 # Average
        else:
            label = 2 # Good
            
        X.append([att, assgn, tst, fuzz_score])
        y.append(label)
        
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)

def train_and_save():
    print("Generating synthetic data for hybrid training...")
    X, y = generate_synthetic_data(3000)
    
    X = X / 100.0
    
    model = build_model()
    print("Training neural network...")
    # Validation split shows accuracy
    history = model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2, verbose=1)
    
    model.save(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save()
