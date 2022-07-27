from plotCDF.discrete import discrete_rv

support_X = list(range(100, 600, 100))
probs_X = [.2, .4, .2, .1, .1]
support_N = list(range(5))
probs_N = [.9934, .004, .002, .0004, .0002]


rv_X = discrete_rv.PMF(support_X, probs_X)
rv_N = discrete_rv.PMF(support_N, probs_N)

print('E(X)=', discrete_rv.expected_value_x_power_k(rv_X))
print('V(X)=', discrete_rv.variance_x(rv_X))

print('E(N)=', discrete_rv.expected_value_x_power_k(rv_N))
print('V(N)=', discrete_rv.variance_x(rv_N))

print('E(P)=', discrete_rv.expected_value_x_power_k(rv_X)*discrete_rv.expected_value_x_power_k(rv_N))
print('V(N)=', discrete_rv.expected_value_x_power_k(rv_N)*discrete_rv.variance_x(rv_X)+
      discrete_rv.expected_value_x_power_k(rv_X)**2*discrete_rv.variance_x(rv_N))
