import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=5000):
    np.random.seed(42)
    
    data = {
        'borrower_id': range(1, num_samples + 1),
        'age': np.random.randint(21, 70, num_samples),
        'gender': np.random.choice(['Male', 'Female'], num_samples),
        'income': np.random.normal(50000, 20000, num_samples).clip(15000, 200000),
        'employment_duration': np.random.randint(0, 480, num_samples),
        'housing_status': np.random.choice(['Own', 'Rent', 'Mortgage'], num_samples),
        'loan_amount': np.random.normal(15000, 10000, num_samples).clip(1000, 100000),
        'tenure': np.random.choice([12, 24, 36, 48, 60], num_samples),
        'credit_score': np.random.randint(300, 850, num_samples),
        'previous_defaults': np.random.choice([0, 1, 2, 3], num_samples, p=[0.8, 0.1, 0.07, 0.03]),
        'debt_to_income_ratio': np.random.uniform(0.1, 0.6, num_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Logic to create realistic default labels
    # Default risk increases with lower credit score, higher debt-to-income, and previous defaults
    risk_score = (
        (850 - df['credit_score']) / 550 * 0.4 +
        df['debt_to_income_ratio'] * 0.3 +
        df['previous_defaults'] * 0.2 +
        (df['loan_amount'] / df['income']) * 0.1
    )
    
    # Base probability + some noise
    prob = risk_score + np.random.normal(0, 0.05, num_samples)
    df['default'] = (prob > 0.5).astype(int)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/synthetic_loan_data.csv', index=False)
    print(f"Generated {num_samples} samples and saved to data/synthetic_loan_data.csv")
    print(f"Default rate: {df['default'].mean():.2%}")
    return df

if __name__ == "__main__":
    generate_synthetic_data()
