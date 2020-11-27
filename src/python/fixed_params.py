##These are fixed parameter sused throughout the process

    
##Hawkes process
alpha=2.4  #power parameter of the power-law mark distribution
mu=10  #min value parameter of the power-law mark distribution
#for computong MAP
prior_params = [ 0.02, 0.0002, 0.01, 0.001, -0.1] #list (mu_p, mu_beta, sig_p, sig_beta, corr) of hyper parameters of the prior
max_n_star = 1 #maximum authorized value of the branching factor (defines the upper bound of p)

##Random forests
max_depth = 2
random_state = 0


#observation windows
obs = [600, 1200, 1800]