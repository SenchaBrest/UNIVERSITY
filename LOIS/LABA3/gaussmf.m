function [mu] = gaussmf(params, x)
    % Функция гаусса принадлежности для нечетких множеств
    % params - вектор параметров
    % x - входной скаляр или массив
    mu = exp(-(x - params(1)).^2 / (2*params(2)^2));
end