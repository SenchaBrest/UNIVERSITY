function I = integrate(method)
    % Функция для вычисления интеграла

    % Определяем переменные
    a = 0; b = 5; I = 0; dx = 0.1;

    % Вычисляем интеграл
    if method == 1
        % Метод трапеций
        while dx >= 0.00001
            % Определяем вектор значений аргумента и функции
            x = a:dx:b;
            y = sin(x).*exp(-x);
            % Суммируем площади трапеций
            I_prev = I;
            I = trapz(x,y);
            % Проверяем достижение точности
            if abs(I - I_prev) < 1e-8
                break
            end
            % Уменьшаем шаг интегрирования в 10 раз
            dx = dx/10;
        end
        I = trapz(x,y);
    elseif method == 2
        % Определяем вектор значений аргумента и функции
        y = @(x) sin(x).*exp(-x);
        % Метод Симпсона
        I = simpson(y, a, b);
    else
        error('Некорректный метод интегрирования')
    end

    % Выводим результат
    disp(['Значение интеграла: ', num2str(I)])
end