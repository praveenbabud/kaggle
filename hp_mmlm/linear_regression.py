import numpy as np
from numpy import linalg

def compute_cost_multi(X, y, theta):
    m = y.shape[0]
    return (1.0/2.0 * 1.0/m * sum((np.dot(X,theta) - y) ** 2))

def feature_normalize(X):
    X_norm = X.copy() 
    X_norm = (X - X.mean(axis=0)) /X.std(axis=0)
    mu = X.mean(axis=0)
    sigma = X.std(axis=0)
    return(X_norm, mu, sigma)

def gradient_descent_multi(X, y, theta, alpha, num_iters):
    m = y.shape[0]
    J_history = np.zeros((num_iters, 1), dtype=np.float64)
    for iter in range(num_iters):
        theta = theta - alpha * 1/m * (np.dot((np.dot(X, theta) - y).T, X)).T
        J_history[iter] = compute_cost_multi(X, y, theta)
    return (theta, J_history)


def normal_eqn(X, y):
    theta = np.zeros((X.shape[1], 1), dtype=np.float64)
    theta = np.dot(linalg.pinv(np.dot(X.T, X)), np.dot(X.T, y))
    return theta

def linear_regression_solve_matrix(X,y):
    x = np.zeros((X.shape[0], (X.shape[1] + 1)),dtype=X.dtype)
    x[:,1:] = X
    x[:,0] = 1
    return normal_eqn(x,y)

def linear_regression_compute_cost(X, y, theta):
    x = np.zeros((X.shape[0], (X.shape[1] + 1)),dtype=X.dtype)
    x[:,1:] = X
    x[:,0] = 1
    return compute_cost_multi(x,y,theta)

def linear_regression_predict(X,theta):
    x = np.zeros((X.shape[0], (X.shape[1] + 1)),dtype=X.dtype)
    x[:,1:] = X
    x[:,0] = 1
    return np.dot(x,theta)



       
