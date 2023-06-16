using PyPlot

y_lin = [] # empty list to store the y values for the linear model
y_nonlin = [] # empty list to store the y values for the nonlinear model

function linear_model(a, b, y, u, i, t)
    # if you want to make the noise, pass the (u) parameter as (u + rand(-1:1) / 100)
    if i <= t
        println(y)
        push!(y_lin, y)
        linear_model(a, b, a*y + b*u, u, i + 1, t) 
    else
        println("OFF")
    end
end

function nonlinear_model(a, b, c, d, y, y_prev, u, u_prev, i, t)
    # if you want to make the noise, pass the (u) parameter as (u + rand(-1:1) / 100)
    if i == 1
        println(y)
        push!(y_nonlin, y)
        nonlinear_model(a, b, c, d, 
                        a*y - b*y_prev^2 + c*0 + d*sin(0), y, 
                        u, u,
                        i + 1, t)
    elseif i <= t
        println(y)
        push!(y_nonlin, y)
        nonlinear_model(a, b, c, d,
                        a*y - b*y_prev^2 + c*u + d*sin(u_prev), y,
                        u, u, 
                        i + 1, t)
    else
        println("OFF")
    end
end

function main()
    i = 1 # initial time; can not be changed
    y = 0.0 # initial temperature; can be changed
    u = 1.0 # input warm; can be changed
    t = 100 # final time; can be changed
    a = 0.5 # linear and nonlinear model parameter; can be changed
    b = 0.5 # linear and nonlinear model parameter; can be changed
    c = 0.5 # nonlinear model parameter; can be changed
    d = 0.5 # nonlinear model parameter; can be changed

    println("Linear Model:")
    linear_model(a, b, y, u, i, t)
    println("Nonlinear Model:")
    nonlinear_model(a, b, c, d, y, y, u, u, i, t)
    
    x = 1:t; y = y_lin; y2 = y_nonlin
    plot(x, y, label="linear_model")
    plot(x, y2, label="nonlinear_model")
    plot(x, y, "b.") 
    plot(x, y2, "r.")
    legend()
end

main()