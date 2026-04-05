import tensorflow as tf
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'student_perf_model.keras')

def build_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def get_model():
    if os.path.exists(MODEL_PATH):
        return tf.keras.models.load_model(MODEL_PATH)
    else:
        return build_model()

def predict_performance(attendance, assignment, test, fuzzy_score):
    model = get_model()
    # Normalize inputs
    input_data = np.array([[attendance, assignment, test, fuzzy_score]], dtype=np.float32)
    input_data = input_data / 100.0
    
    prediction = model.predict(input_data)
    class_idx = np.argmax(prediction[0])
    confidence = float(np.max(prediction[0]))
    
    classes = ['Poor', 'Average', 'Good']
    return classes[class_idx], confidence
