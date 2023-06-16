function dydt = vanderpoldyn(t, y, K)
    dydt = [y(2); -y(1) + K*(1-y(1)^2)*y(2)];
end