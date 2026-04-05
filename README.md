# Hybrid Intelligent System for Student Performance Prediction

This project combines Fuzzy Logic (rule-based reasoning) and Artificial Neural Networks (learning-based prediction) to create a robust student performance evaluation system.

##  Why a Hybrid System?
Fuzzy logic is excellent at modeling human-like reasoning and subjective concepts (e.g., "High Attendance"). Conversely, Neural Networks are powerful pattern recognizers that learn from unstructured data. 

**Our Architecture (Option A):**
We extract structured knowledge from the user’s inputs using Fuzzy Rules. This fuzzy output score is then used alongside the raw inputs (Attendance, Assignment, Test) as features for a Keras Sequential Neural Network model. This combination significantly increases context awareness and prediction confidence compared to standalone NN models!

##  Features
- Fuzzy rule-based reasoning
- Neural network learning
- Hybrid AI integration
- Interactive frontend
  
##  Project Structure
```text
/backend
 ├── ai_models
 │    ├── nn_model.py (Tensorflow keras NN)
 │    └── train.py (Trains and creates .keras model)
 ├── data
 │    ├── database.py (SQLite setup)
 │    └── models.py (SQLAlchemy schema)
 ├── fuzzy_logic
 │    └── fuzzy_system.py (scikit-fuzzy logic and 9 strict rules)
 ├── main.py (FastAPI application)
 └── requirements.txt

/frontend
 ├── src
 │    ├── App.jsx (React UI)
 │    ├── index.css (Premium animated UI styles)
 ├── package.json
```

## Setup Instructions

### 1. Backend Setup
1. Navigate to the `backend` folder.
2. Install Python requirements: `pip install -r requirements.txt`
3. The Neural Network must be trained first. Run `python ai_models/train.py`.
   - This will generate a synthetic dataset governed by the fuzzy rules, train the neural network, and save `student_perf_model.keras`.
4. Start the FastAPI server: `python -m uvicorn main:app --reload`
   - Test endpoints at `http://localhost:8000/docs`

### 2. Frontend Setup
1. Navigate to the `frontend` folder.
2. Install NodeJS dependencies: `npm install`
3. Run the Vite development server: `npm run dev`
4. Visit `http://localhost:5173` to interact with the premium predictive UI!
