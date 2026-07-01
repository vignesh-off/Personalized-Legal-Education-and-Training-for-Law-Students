import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import os

def generate_mock_dataset(filename="student_data.csv"):
    """Generates a synthetic dataset for the legal tutor ML model."""
    print("Generating mock dataset...")
    np.random.seed(42)
    n_samples = 1000
    
    # Features
    time_spent_modules = np.random.normal(loc=50, scale=15, size=n_samples) # hours
    practice_problems_completed = np.random.randint(10, 100, size=n_samples)
    previous_quiz_scores = np.random.normal(loc=70, scale=10, size=n_samples)
    days_since_last_login = np.random.randint(0, 30, size=n_samples)
    
    # Target variable: Concept Mastery (1 = Yes, 0 = No)
    # Higher study time, practice, and previous scores increase chance of mastery
    mastery_prob = (time_spent_modules * 0.3 + practice_problems_completed * 0.4 + previous_quiz_scores * 0.3 - days_since_last_login * 0.5) / 100
    mastery_prob = np.clip(mastery_prob, 0, 1) # Ensure probabilities are between 0 and 1
    concept_mastery = np.random.binomial(1, mastery_prob)
    
    # Create DataFrame
    df = pd.DataFrame({
        'time_spent_modules': time_spent_modules,
        'practice_problems_completed': practice_problems_completed,
        'previous_quiz_scores': previous_quiz_scores,
        'days_since_last_login': days_since_last_login,
        'concept_mastery': concept_mastery
    })
    
    # Introduce some missing values to demonstrate preprocessing
    df.loc[np.random.choice(df.index, size=50, replace=False), 'previous_quiz_scores'] = np.nan
    
    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename}\n")
    return filename

def run_ml_pipeline():
    dataset_path = "student_data.csv"
    if not os.path.exists(dataset_path):
        generate_mock_dataset(dataset_path)
        
    print("--- 1. Loading Data ---")
    df = pd.read_csv(dataset_path)
    print(df.head(), "\n")
    
    print("--- 2. Data Preprocessing ---")
    # Handling missing values (imputing with mean)
    print(f"Missing values before preprocessing:\n{df.isnull().sum()}\n")
    df['previous_quiz_scores'] = df['previous_quiz_scores'].fillna(df['previous_quiz_scores'].mean())
    print("Missing values handled (mean imputation applied).\n")
    
    # Separating features (X) and target (y)
    X = df.drop('concept_mastery', axis=1)
    y = df['concept_mastery']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("Data features scaled using StandardScaler.\n")
    
    print("--- 3. Model Training ---")
    # Using Random Forest as the baseline model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    print("Random Forest Classifier model trained successfully.\n")
    
    print("--- 4. Evaluation Metrics ---")
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1-Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC:   {roc_auc_score(y_test, y_prob):.4f}\n")
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\n--- 5. Feature Importance ---")
    feature_importances = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    print(feature_importances)

if __name__ == "__main__":
    run_ml_pipeline()
