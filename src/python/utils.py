##This file contains utilities function fused for the estimator and predictor part


##Kafka
import json
from json import loads, dumps
from kafka import KafkaConsumer, KafkaProducer
import ast

from fixed_params import *


def msg_deserializer(message) :
    ## this function a custom to deserialize
    ## the kafka message comming from the cascade topic
    ## message = key, value

    key = loads(message.key.decode('utf-8'))
    value = ast.literal_eval(message.value.decode("UTF-8"))
    #value = loads(message.value.decode('utf-8').replace('\'', '\"'))
    return (key, value)



def msg_serializer(message):
    ## this function a custom to deserialize
    ## the kafka message going to the cascade topic
    ## message = key, value
    messageJSON = dumps(message)
    messageBytes = messageJSON.encode('utf-8')
    return messageBytes



##Estimator
import numpy as np
import scipy.optimize as optim


def loglikelihood(params, history, t=None):
    """
    Returns the loglikelihood of a Hawkes process with exponential kernel
    computed with a linear time complexity

    params   -- parameter tuple (p,beta) of the Hawkes process
    history  -- (n,2) numpy array containing marked time points (t_i,m_i)
    t        -- current time (i.e end of observation window)
    """

    p,beta = params

    if p <= 0 or p >= 1 or beta <= 0.: return -np.inf

    if t is None:
        t = history[-1, 0]

    history_at_t = history[history[:, 0] <= t]

    n = len(history_at_t)
    tis = history_at_t[:,0]
    mis = history_at_t[:,1]

    loglikelihood = (n-1)*np.log(p*beta)

    #A1
    previous_ai = np.exp(-beta*(tis[1]-tis[0]))*(mis[0])
    for i in range(1,n):
        if(mis[i-1] + previous_ai <= 0):
            print("Bad value",mis[i-1]  + previous_ai)
        previous_ai = np.exp(-beta*(tis[i]-tis[i-1]))*(mis[i-1]+previous_ai)
        loglikelihood += np.log(previous_ai)

    loglikelihood -= p*(np.sum(mis) - np.exp(-beta*(t-tis[n-1]))*(mis[n-1]+previous_ai))

    return loglikelihood



def compute_MAP(history, alpha=alpha, mu=mu,
                prior_params = prior_params,
                max_n_star = max_n_star, display=False, t=None):
    """
    Returns the pair of the estimated logdensity of a posteriori and parameters (as a numpy array)

    history      -- (n,2) numpy array containing marked time points (t_i,m_i)
    t            -- current time (i.e end of observation window)
    alpha        -- power parameter of the power-law mark distribution
    mu           -- min value parameter of the power-law mark distribution
    prior_params -- list (mu_p, mu_beta, sig_p, sig_beta, corr) of hyper parameters of the prior
                 -- where:
                 --   mu_p:     is the prior mean value of p
                 --   mu_beta:  is the prior mean value of beta
                 --   sig_p:    is the prior standard deviation of p
                 --   sig_beta: is the prior standard deviation of beta
                 --   corr:     is the correlation coefficient between p and beta
    max_n_star   -- maximum authorized value of the branching factor (defines the upper bound of p)
    display      -- verbose flag to display optimization iterations (see 'disp' options of optim.optimize)
    """

    # Compute prior moments
    mu_p, mu_beta, sig_p, sig_beta, corr = prior_params

    mu_sample = np.array([mu_p, mu_beta])
    cov_p_beta = corr*sig_p*sig_beta

    Q = [[sig_p**2, cov_p_beta],
         [cov_p_beta, sig_beta**2]]

    # Apply method of moments

    sigma_prior = np.log(Q / mu_sample / mu_sample.reshape((-1, 1)) + 1)
    mu_prior = np.log(mu_sample) - np.diag(sigma_prior) / 2.

    # Compute the covariance inverse (precision matrix) once for all
    inv_cov_prior = np.asmatrix(sigma_prior).I

    # Define the target function to minimize as minus the log of the a posteriori density
    def target(params):
        ## a is added in case params equals to 0
        log_params = np.log(1+params)

        if np.any(np.isnan(log_params)):
            return np.inf
        else:
            dparams = np.asmatrix(log_params - mu_prior)
            prior_term = float(- 1/2 * dparams * inv_cov_prior * dparams.T)
            logLL = loglikelihood(params, history, t)
            return - (prior_term + logLL)


    # Run the optimization
    EM = mu * (alpha - 1) / (alpha - 2)
    eps = 1.E-8

    # Set realistic bounds on p and beta
    p_min, p_max       = eps, max_n_star/EM - eps
    beta_min, beta_max = 1/(3600. * 24 * 10), 1/(60. * 1)

    # Define the bounds on p (first column) and beta (second column)
    bounds = optim.Bounds(
        np.array([p_min, beta_min]),
        np.array([p_max, beta_max])
    )

    # Run the optimization
    res = optim.minimize(
        target, mu_sample,
        method='Powell',
        bounds=bounds,
        options={'xtol': 1e-8, 'disp': display}
    )
    # Returns the loglikelihood and found parameters
    return(-res.fun, res.x)


## Predictor

##This is the function for computing the estimated size of the cascade
## For simple estimator (direct computation without radnom forest) use w_obs=1
# def estimated_size(params, history, alpha=alpha, mu=mu, t=None, w_obs=1):
#     """
#     Returns the expected total numbers of points for a set of time points
    
#     params   -- parameter tuple (p,beta) of the Hawkes process
#     history  -- (n,2) numpy array containing marked time points (t_i,m_i)  
#     alpha    -- power parameter of the power-law mark distribution
#     mu       -- min value parameter of the power-law mark distribution
#     t        -- current time (i.e end of observation window)
#     """

#     p,beta = params
    
#     n_star = p*mu*(alpha-1)/(alpha-2)
    
#     if t is None:
#         t = history[-1, 0] 
    
#     history_at_t = history[history[:, 0] <= t]
    
#     n = len(history_at_t)
<<<<<<< HEAD
    
=======
>>>>>>> 34309cc0e77002abf8bb78f573ac607c691ac054
#     G1=0
#     for t_i, m_i in history_at_t:
#         G1 += m_i*(np.exp(-beta*(t-t_i)))
#     G1*=p
    
#     N_infini = n + w_obs*(G1/(1-n_star))
    
#     return N_infini


##Function for computing G1 parameter
def compute_G1(params, cascade):
    """
    Returns G1

    params -- parameter tuple (p,beta) of the Hawkes process
    cascade -- (n,2) numpy array containing marked time points (t_i,m_i) 
    """
    p, beta = params
    G1=0
    t = cascade[-1, 0]
    for t_i, m_i in cascade:
        G1 += m_i*(np.exp(-beta*(t-t_i)))
    G1*=p

    return G1



##This is the function for computing the estimated size of the cascade
## For simple estimator (direct computation without radnom forest) use w_obs=1
def estimated_size(n_obs, params, w_obs=1, alpha=alpha, mu=mu):
    """
    Returns the expected total numbers of points for a set of time points
    
    n_obs -- int, the size of the observed window
    params -- parameter tuple (p,beta, G1) of the Hawkes process sent by the estimator
    w_obs -- the w computed by the model associated to the obs window, default 1 (if no trained model)
    alpha    -- power parameter of the power-law mark distribution
    mu       -- min value parameter of the power-law mark distribution
    
    """

    p, beta, G1 = params
    n_star = p*mu*(alpha-1)/(alpha-2)
    n_pred = n_obs + w_obs*(G1/(1-n_star))

    return n_pred



def compute_true_omega(n_obs, n_true, params,  alpha=alpha, mu=mu):
    """
    compute the true W used for random forest training.
    We use the true value of the size of the cascade to compute the value of the W we want to find
    
    n_obs -- int, the size of the observed window
    n_true -- the final size of the cascade, once the cascade is considered idle and over
    params -- parameter tuple (p,beta, G1) of the Hawkes process sent by the estimator
    alpha    -- power parameter of the power-law mark distribution
    mu       -- min value parameter of the power-law mark distribution
    """

    p, beta, G1 = params
    n_star = p*mu*(alpha-1)/(alpha-2)
    W = (n_true - n_obs)*(1-n_star)/G1

    return W




def compute_are(n_tot, n_true):
    """
    Return the Absolute Relative Error

    n_tot -- int, predicted size of the cascade
    n_true -- int, real size of the  cascade
    """

    return abs(n_tot - n_true)/n_true
