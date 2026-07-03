import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    
    # Generate features
    # scores from 0 to 100
    scores = np.random.randint(0, 101, num_samples)
    # time spent in minutes from 5 to 120
    time_spent = np.random.randint(5, 121, num_samples)
    # attempts from 1 to 10
    attempts = np.random.randint(1, 11, num_samples)
    # difficulty level from 1 to 5
    difficulty = np.random.randint(1, 6, num_samples)
    
    # Generate labels based on a heuristic
    # High score, low attempts -> Expert
    # Low score, high attempts -> Beginner
    mastery_levels = []
    for s, t, a, d in zip(scores, time_spent, attempts, difficulty):
        # A simple score to define mastery
        mastery_score = s - (a * 2) + (d * 5)
        
        if mastery_score >= 70:
            mastery_levels.append('Expert')
        elif mastery_score >= 40:
            mastery_levels.append('Intermediate')
        else:
            mastery_levels.append('Beginner')
            
    df = pd.DataFrame({
        'score': scores,
        'time_spent': time_spent,
        'attempts': attempts,
        'difficulty_level': difficulty,
        'mastery_level': mastery_levels
    })
    
    return df

def main():
    print("Generating synthetic data...")
    df = generate_synthetic_data(num_samples=2000)
    
    X = df[['score', 'time_spent', 'attempts', 'difficulty_level']]
    y = df['mastery_level']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    print(classification_report(y_test, y_pred))
    
    # Create ml/models directory if it doesn't exist
    os.makedirs('ml/models', exist_ok=True)
    
    print("Saving model and scaler to ml/models/...")
    joblib.dump(model, 'ml/models/model.joblib')
    joblib.dump(scaler, 'ml/models/scaler.joblib')
    print("Done.")

if __name__ == '__main__':
    main()
