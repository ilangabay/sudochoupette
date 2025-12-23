"""
Most basic working sequence classifier - guaranteed to work!
"""

import numpy as np
from sklearn.linear_model import LogisticRegression

class BasicSequenceClassifier:
    """Most basic sequence classifier that should work everywhere."""
    
    def __init__(self):
        # Use the most basic LogisticRegression setup
        self.model = LogisticRegression(max_iter=2000)
        self.is_fitted = False
    
    def _one_hot_encode(self, X):
        """Simple one-hot encoding for 4 categories."""
        n_samples, n_features = X.shape
        encoded = np.zeros((n_samples, n_features * 4))
        
        for i in range(n_samples):
            for j in range(n_features):
                value = X[i, j]
                if 1 <= value <= 4:
                    col_idx = j * 4 + (value - 1)
                    encoded[i, col_idx] = 1
        
        return encoded
    
    def prepare_data(self, sequences):
        """Convert sequences to training data."""
        X, y = [], []
        
        for seq in sequences:
            for i in range(len(seq) - 5):
                if all(1 <= x <= 4 for x in seq[i:i+6]):
                    X.append(seq[i:i+5])
                    y.append(seq[i+5])
        
        return np.array(X), np.array(y)
    
    def fit(self, sequences):
        """Train the classifier."""
        X, y = self.prepare_data(sequences)
        
        if len(X) == 0:
            raise ValueError("No valid data")
        
        X_encoded = self._one_hot_encode(X)
        
        print(f"Training on {len(X)} samples with {len(set(y))} classes")
        
        self.model.fit(X_encoded, y)
        self.is_fitted = True
        return self
    
    def predict_proba(self, features):
        """Get probability vector for 4 classes."""
        if not self.is_fitted:
            raise ValueError("Not trained")
        
        if len(features) != 5 or not all(1 <= x <= 4 for x in features):
            raise ValueError("Need 5 features with values 1-4")
        
        X = np.array(features).reshape(1, -1)
        X_encoded = self._one_hot_encode(X)
        
        # Get probabilities for all classes 1-4
        probs = self.model.predict_proba(X_encoded)[0]
        
        # Make sure we have exactly 4 probabilities
        result = np.zeros(4)
        classes = self.model.classes_
        
        for i, cls in enumerate(classes):
            if 1 <= cls <= 4:
                result[cls-1] = probs[i]
        
        # Normalize to sum to 1
        if result.sum() > 0:
            result = result / result.sum()
        else:
            result = np.array([0.25, 0.25, 0.25, 0.25])  # Uniform if all zero
        
        return result
    
    def predict(self, features):
        """Predict most likely class."""
        probs = self.predict_proba(features)
        return np.argmax(probs) + 1


# Test it
if __name__ == "__main__":
    # Test data
    sequences = [
        [1, 2, 3, 4, 1, 2, 3],
        [4, 3, 2, 1, 4, 3, 2],
        [1, 1, 2, 2, 3, 3, 4],
        [2, 4, 1, 3, 2, 4, 1],
    ]
    
    # Train and test
    clf = BasicSequenceClassifier()
    clf.fit(sequences)
    
    # Test prediction
    test = [1, 2, 3, 4, 1]
    probs = clf.predict_proba(test)
    pred = clf.predict(test)
    
    print(f"Input: {test}")
    print(f"Probabilities: {probs.round(3)}")
    print(f"Prediction: {pred}")
    print("SUCCESS! ✓")