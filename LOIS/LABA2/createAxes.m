function createAxes()
    % Создаем графическое окно с объектом axes
    fig = figure();
    ax = axes('Parent', fig, 'Position', [0.1 0.3 0.8 0.6]);
    
    % Создаем редактируемые поля и текстовые поля
    uicontrol('Style', 'text', 'String', 'x0:', 'Position', [50 240 30 20]);
    x0_edit = uicontrol('Style', 'edit', 'Position', [80 240 100 20], 'String', '0');
    
    uicontrol('Style', 'text', 'String', 'dx:', 'Position', [50 210 30 20]);
    dx_edit = uicontrol('Style', 'edit', 'Position', [80 210 100 20], 'String', '0.1');
    
    uicontrol('Style', 'text', 'String', 'xn:', 'Position', [50 180 30 20]);
    xn_edit = uicontrol('Style', 'edit', 'Position', [80 180 100 20], 'String', '10');
    
    % Создаем командную кнопку
    uicontrol('Style', 'pushbutton', 'String', 'Построить', ...
              'Position', [50 130 130 30], 'Callback', @plotFunction);
    
    % Функция для построения графика
    function plotFunction(~, ~)
        % Получаем значения из редактируемых полей
        x0 = str2double(get(x0_edit, 'String'));
        dx = str2double(get(dx_edit, 'String'));
        xn = str2double(get(xn_edit, 'String'));
        
        % Создаем массив x
        x = x0:dx:xn;
        
        % Список доступных функций
        functions = {'sin', 'cos', 'tan', 'exp', 'myFunction'};
        
        % Диалог выбора функции
        [indx,tf] = listdlg('ListString',functions,'Name','Выберите функцию');
        if tf == 1
            % Выбрана одна из стандартных функций
            func_name = functions{indx};
            y = feval(func_name, x);
            plot(ax, x, y);
        elseif indx == 5
            % Выбрана пользовательская функция
            y = myFunction(x);
            plot(ax, x, y);
        end
    end
end

function y = myFunction(x)
    % Замените содержимое этой функции на свою собственную функцию
    y = x.^2;
end