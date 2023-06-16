using Plots
using LinearAlgebra

K = 0.0001
T = 100
T_D = 100
T_0 = 1

q_0 = K * (1 + T_D/T_0)
q_1 = -K * (1 + 2 * T_D / T_0 - T_0 / T)
q_2 = K * T_D / T_0


q = [q_0, q_1, q_2]
e = [0.0, 0.0, 0.0]
y = [0.0, 0.0, 0.0]
u = [1.0, 1.0]

function nonlinear_model(time, a = 0.5, b = 0.3, c = 0.9, d = 0.7)
    i = 0
    while i < time
        e[1] = w - y[length(y)]
        e[2] = w - y[length(y) - 1]
        e[3] = w - y[length(y) - 2]
        u[1] = u[2] + dot(q, e)
        push!(y, (a*y[length(y)] - b*y[length(y) - 1]^2 + c*u[1] + d*sin(u[2])))
        u[2] = u[1]
        
        i += 1
    end
end

function main()
    global w = parse(Int64, readline())
    nonlinear_model(100)
    
    for el in y
        println(el * w / y[length(y)])  
    end
    
    plot(1:length(y), y * w / y[length(y)], label="nonlinear_model")
end

main()