function alpha = sigmFunc(a,b,x)
    alpha = 1/(1 + exp(1).^(b.*(x-a)));
end