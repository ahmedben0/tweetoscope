## This funiton estimates the parameters (p, beta) of the generating process for the cascade.
## We use the MAP estimator.



import numpy as np

import scipy.optimize as optim


##Simulate cascade
# #%%

# def neg_power_law(alpha, mu, size=1):
#     """
#     Returns a 1D-array of samples drawn from a negative power law distribution
    
#     alpha -- power parameter of the power-law mark distribution
#     mu    -- min value parameter of the power-law mark distribution
#     size  -- number of samples
#     """
    
#     u = np.random.uniform(size=size)
#     return mu * np.exp(np.log(u) / (1. - alpha))    


# def simulate_marked_exp_hawkes_process(params, m0, alpha, mu, max_size=10000):
#     """
#     Returns a 2D-array whose rows contain marked time points simulated from an exponential Hawkes process
    
#     params   -- parameter tuple (p,beta) of the generating process
#     m0       -- magnitude of the initial tweet at t = 0.
#     alpha    -- power parameter of the power-law mark distribution
#     mu       -- min value parameter of the power-law mark distribution
#     max_size -- maximal authorized size of the cascade
#     """
    
#     p,beta = params
    
    
#     # Create an unitialized array for optimization purpose (only memory allocation)
#     T = np.empty((max_size,2))
    
#     intensity = beta * p * m0
#     t, m = 0., m0
    
#     samples = neg_power_law(alpha, mu, size=max_size)
    
#     # Main loop
#     for i in range(max_size):
#         # Save the current point before generating the next one.
#         T[i] = (t, m)
        
#         # 
#         u = np.random.uniform()
#         v = -np.log(u)
#         w = 1. - beta / intensity * v
#         # Tests if process stops generating points.
#         if w <= 0.:
#             # Shrink T to remove unused rows
#             T = T[:i,:]
#             break
            
#         # Otherwise computes the time jump dt and new time point t
#         dt = - np.log(w) / beta
#         t += dt
        
#         # And update intensity accordingly
#         m = neg_power_law(alpha, mu)
#         intensity = intensity * np.exp(-beta * dt) + beta * p * m  
#     return T

# #%%
# beta = 1/3600
# p = 0.05
# params = (p, beta)
# m0 = 1000
# alpha = 2.4
# mu = 10

# n = p*mu*(alpha-1)/(alpha-2)
# print("n*: ", n)

# cascade = simulate_marked_exp_hawkes_process(params, m0, alpha, mu, max_size=10000)



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



def compute_MAP(history, alpha=2.4, mu=10,
                prior_params = [ 0.02, 0.0002, 0.01, 0.001, -0.1],
                max_n_star = 1, display=False, t=None):
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
        log_params = np.log(params)
        
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


estimated_params = compute_MAP(cascade)[1]

