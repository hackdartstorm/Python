def linear_regression(x_values, y_values, learning_rate=0.01, epochs=1000):
    """
    Implements Simple Linear Regression using Gradient Descent.
    This is the foundation of Supervised Learning.
    """
    # Initializing weight (m) and bias (b)
    m, b = 0.0, 0.0
    n = len(x_values)
    
    for _ in range(epochs):
        # Calculating predictions
        y_pred = [m * x + b for x in x_values]
        
        # Calculating Gradients
        dm = (-2/n) * sum(x * (y - yp) for x, y, yp in zip(x_values, y_values, y_pred))
        db = (-2/n) * sum(y - yp for y, yp in zip(y_values, y_pred))
        
        # Updating parameters (Gradient Descent)
        m -= learning_rate * dm
        b -= learning_rate * db
        
    return m, b

# Simple Test Case
# x = [1, 2, 3], y = [2, 4, 6] -> Expected m=2, b=0