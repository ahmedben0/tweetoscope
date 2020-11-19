## This is a first simple predictor that takes the parameters of the generating process (p, beta)

def prediction(params, history, alpha=2.4, mu=10, t=None):
    """
    Returns the expected total numbers of points for a set of time points
    
    params   -- parameter tuple (p,beta) of the Hawkes process
    history  -- (n,2) numpy array containing marked time points (t_i,m_i)  
    alpha    -- power parameter of the power-law mark distribution
    mu       -- min value parameter of the power-law mark distribution
    t        -- current time (i.e end of observation window)
    """

    p,beta = params
    
    n_star = p*mu*(alpha-1)/(alpha-2)
    
    if t is None:
        t = history[-1, 0] 
    
    history_at_t = history[history[:, 0] <= t]
    
    n = len(history_at_t)
    
    G1=0
    for t_i, m_i in history_at_t:
        G1 += m_i*(np.exp(-beta*(t-t_i)))
    G1*=p
    
    N_infini = n + G1/(1-n_star)
    
    return N_infini
    