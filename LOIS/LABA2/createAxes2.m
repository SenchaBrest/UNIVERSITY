function createAxes2()
    % Создаем графическое окно с объектом axes
    fig = figure();
    ax = axes('Parent', fig, 'Position', [0.1 0.3 0.8 0.6]);
    
    % Создаем редактируемые поля и текстовые поля
    uicontrol('Style', 'text', 'String', 'b1:', 'Position', [50 270 30 20]);
    b1_edit = uicontrol('Style', 'edit', 'Position', [80 270 100 20], 'String', '0');
    
    uicontrol('Style', 'text', 'String', 'b2:', 'Position', [50 240 30 20]);
    b2_edit = uicontrol('Style', 'edit', 'Position', [80 240 100 20], 'String', '10');

    uicontrol('Style', 'text', 'String', 'y1:', 'Position', [50 210 30 20]);
    y1_edit = uicontrol('Style', 'edit', 'Position', [80 210 100 20], 'String', '0.1');
    
    uicontrol('Style', 'text', 'String', 'y2:', 'Position', [50 180 30 20]);
    y2_edit = uicontrol('Style', 'edit', 'Position', [80 180 100 20], 'String', '0.1');
    
    % Создаем командную кнопку для построения графика
    uicontrol('Style', 'pushbutton', 'String', 'Построить', ...
              'Position', [50 130 130 30], 'Callback', @plotFunction);
          
    % Создаем командную кнопку для сброса графика и элементов управления
    reset_button = uicontrol('Style', 'pushbutton', 'String', 'Сброс', ...
              'Position', [50 80 130 30], 'Callback', @resetFunction, 'Visible', 'off');
          
    % Функция для построения графика
    function plotFunction(~, ~)
        % Получаем значения из редактируемых полей
        b1 = str2double(get(b1_edit, 'String'));
        b2 = str2double(get(b2_edit, 'String'));
        y1 = str2double(get(y1_edit, 'String'));
        y2 = str2double(get(y2_edit, 'String'));

        % Список доступных функций
        functions = {'1', '2', '3'};
        
        % Диалог выбора функции
        indx = listdlg('ListString', functions, 'Name', 'Выберите функцию');

        switch indx
            case 1
                f = @(x, y) [y(2); -y(1) + 0.01*(1-y(1)^2)*y(2)];
            case 2
                f = @(x, y) [y(2); -y(1) + 0.1*(1-y(1)^2)*y(2)];
            case 3
                f = @(x, y) [y(2); -y(1) + 1*(1-y(1)^2)*y(2)];
        end
        [t, y] = ode15s(f, [b1, b2], [y1, y2]);

        % Визуализируем решение
        plot(t, y(:,1));
        xlabel('t');
        ylabel('y1');
        
        % Расширяем объект axes, чтобы он перекрывал элементы управления
        ax.Position = [0.1 0.1 0.8 0.8];
        
        % Скрываем элементы управления
        set(b1_edit, 'Visible', 'off');
        set(b2_edit, 'Visible', 'off');
        set(y1_edit, 'Visible', 'off');
        set(y2_edit, 'Visible', 'off');
        set(reset_button, 'Visible', 'on');
    end

    % Функция для сброса графика и элементов управления
    function resetFunction(~, ~)
        % Очищаем график
        cla(ax);
    
        % Возвращаем объект axes в исходное положение
        ax.Position = [0.1 0.3 0.8 0.6];
    
        % Показываем элементы управления
        set(b1_edit, 'Visible', 'on');
        set(b2_edit, 'Visible', 'on');
        set(y1_edit, 'Visible', 'on');
        set(y2_edit, 'Visible', 'on');
        set(gcbo, 'Visible', 'on'); % gcbo - объект, инициировавший вызов функции
        set(reset_button, 'Visible', 'off'); 
    end
end