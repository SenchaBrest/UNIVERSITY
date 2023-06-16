timeSvetofor = randi([10,35]);
statusTimeSvetofor = 0;
countNS = 0; countWE = 0;
coefNS = []; coefWE = [];
statusNS = 0; statusWE = 0;
svetoforStatus = 0;

for i=1:100
    disp(i)
    disp(["Время зеленого светофора на СЮ: ", timeSvetofor])
    disp(["Время зеленого светофора на ЗВ: ", (60 - timeSvetofor)])
    statusWE = 0; statusNS = 0;
    statusTimeSvetofor = 0;
    countNS = max([countNS + randi([4,15],1,1) - round(timeSvetofor/3),0]);
    countWE = max([countWE + randi([4,15],1,1) - round((60-timeSvetofor)/3),0]);
    disp([ ...
        "countNS: ",countNS, ...
        "countWS: ",countWE])
    % малое (10-25сек.) = 1 
    % среднее(20-40сек.) = 2 
    % большое(35-50сек.) = 3
    [~,statusTimeSvetofor] = max([ ...
        gaussmf([0,10,20,25],timeSvetofor), ...
        gaussmf([20,25,35,40],timeSvetofor), ...
        gaussmf([35,40,50,60],timeSvetofor)]);
    % очень малое (0-18) = 1
    % малое (16-36) = 2 
    % среднее (34-56)= 3 
    % большое (54-76) = 4
    % очень большое (72-90)= 5
    [~,statusNS] = max([ ...
        gaussmf([-100,0,12,18],countNS), ...
        gaussmf([16,22,32,36],countNS), ...    
        gaussmf([34,40,50,56],countNS), ...
        gaussmf([54,60,70,76],countNS), ...
        gaussmf([72,78,90,1000],countNS)]);
    [~,statusWE] = max([ ...
        gaussmf([-100,0,12,18],countWE), ...
        gaussmf([16,22,32,36],countWE), ...
        gaussmf([34,40,50,56],countWE), ...
        gaussmf([54,60,70,76],countWE), ...
        gaussmf([72,78,90,1000],countWE)]);   

    svetoforStatus = WhatToDo(statusTimeSvetofor,statusNS,statusWE);
    disp(["states: ", statusTimeSvetofor, statusNS, statusWE, svetoforStatus])

    % увеличить (0-20сек.) = 1 
    % не изменять (-15-15сек.) = 2
    % уменьшить (-20-0сек.) = 3
    switch svetoforStatus
        case 1
            disp('увеличить (0-20сек.)')
            timeSvetofor = min([timeSvetofor + randi([0,20],1,1),50]);
        case 2
            disp('не изменять (-15-15сек.)')
            timeSvetofor = max([10,min([timeSvetofor+randi([-15,15],1,1),50])]);
        case 3
            disp('уменьшить (-20-0сек.)')
            timeSvetofor = max([timeSvetofor+randi([-20,0],1,1);10]);
        otherwise
            disp('Anomaly')
    end
end
