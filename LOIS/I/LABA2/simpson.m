function I = simpson(y, a, b)
    % Функция для вычисления интеграла методом Симпсона
    I = quad(y, a, b,'simpson');
end
