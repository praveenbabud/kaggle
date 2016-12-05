import numpy as np
import scipy.optimize as op
## should always pass np.array to sigmoid function
def sigmoid(z):
    r = np.e ** (-1 * z)
    r = r + 1
    r = 1 / r 
    return r


def cost_function_reg(theta, X, y, lam):
    m,n = X.shape
    theta = theta.reshape((n,1))
    y = y.reshape((m,1))
    total_cost = 0.0
    #total_cost =  1.0/m * sum(((-1 * y) * np.log(sigmoid(np.dot(X, theta))))  - ((1-y) * np.log(1 - sigmoid(np.dot(X, theta)))))
    #total_cost =  1.0/m * sum(((-1 * y) * np.log(sigmoid(np.dot(X, theta)))))
    total_cost =  1.0/m * sum(((-1 * 32.1 * y) * np.log(sigmoid(np.dot(X, theta))))  - ((1-y) * np.log(1 - sigmoid(np.dot(X, theta)))))
    total_cost = total_cost + (lam/(2 * m)) * sum(theta[1:] ** 2)
    return total_cost


def cost_function_reg_der(theta, X, y, lam):
    m,n = X.shape
    theta = theta.reshape((n,1))
    y = y.reshape((m,1))
    grad = np.zeros((theta.shape[0],1), dtype=np.float32)
    gradt = np.zeros((theta.shape[0],1), dtype=np.float32)
    #grad = 1.0/m * (np.dot(((sigmoid(np.dot(X, theta)) - y).T), X).T)
    for i in range(m):
        thetax = np.dot(X[i],theta)
        grad = grad + (sigmoid(thetax) * (32.1 * y[i][0] * (np.e ** (-1 * thetax)) + y[i][0] - 1)) * (((X[i]).T).reshape((n,1)))
        #grad = grad + (sigmoid(-thetax) * (y[i][0])) * (((X[i]).T).reshape((n,1)))
    grad = 1.0/m * grad
    gradt = (lam/m) * theta
    gradt[0] = 0.0
    grad = grad + gradt;
    return grad.flatten()

def solve_lr(X,y,lam):
    m,n = X.shape
    x = np.zeros((m,n+1), dtype=np.float32)
    x[:,1:] = X
    x[:,0] = 1
    initial_theta = np.zeros(((n+1)), dtype=np.float32)
    od = {'maxiter':10000 }
    Result = op.minimize(fun=cost_function_reg, x0=initial_theta,args=(x,y,lam), method = 'TNC', jac = cost_function_reg_der, options=od)
    optimal_theta = Result.x
    return optimal_theta.T


def predict_lr(X,y,theta):
    m,n = X.shape
    x = np.zeros((m,n+1), dtype=np.float32)
    x[:,1:] = X
    x[:,0] = 1
    co = cost_function_reg(theta,x,y,0)
    return (sigmoid(np.dot(x, theta)), co)
   

 
def predict_nlr(X,theta):
    m,n = X.shape
    x = np.zeros((m,n+1), dtype=np.float32)
    x[:,1:] = X
    x[:,0] = 1
    return sigmoid(np.dot(x, theta))
    
