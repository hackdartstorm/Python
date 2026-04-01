import numpy as np

def multiple_linear_regression(X, y, lr=0.01, epochs=1000):
    """
    Implements Multiple Linear Regression using Vectorized Operations.
    X: Matrix of features (samples, features)
    y: Target values
    """
    # Adding a column of ones for the intercept (bias term)
    X = np.c_[np.ones(X.shape[0]), X]
    
    # Initializing weights with zeros
    weights = np.zeros(X.shape[1])
    n = len(y)
    
    for _ in range(epochs):
        # Predicting values
        y_pred = np.dot(X, weights)
        
        # Calculating Gradients
        error = y_pred - y
        gradient = (2/n) * np.dot(X.T, error)
        
        # Updating weights (Gradient Descent)
        weights -= lr * gradient
        
    return weights

# Example Use: Predicting house price based on (Area, Rooms)
# X = np.array([[1500, 3], [2000, 4], [1200, 2]])
# y = np.array([300000, 400000, 240000])