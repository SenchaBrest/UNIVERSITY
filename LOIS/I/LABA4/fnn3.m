% Задаем параметры нечеткой нейронной сети
a1 = 40; a2 = -40; a3 = 20;
b1 = 0.07; b2 = 0.08; b3 = 0.09;
c1 = 0.05; c2 = -0.03; c3 = -0.04;
k1 = -0.9; k2 = 1.5; k3 = -1.3;

% Генерируем обучающую выборку
P_train = 1000;
X_train = linspace(-100, 100, P_train);
Z_train = zeros(1, P_train);

for i = 1:P_train
    alpha1 = sigmFunc(a1, b1, X_train(i));
    alpha2 = sigmFunc(a2, b2, X_train(i));
    alpha3 = sigmFunc(a3, b3, X_train(i));
    zet1 = linFuncRevers(c1, k1, alpha1);
    zet2 = linFuncRevers(c2, k2, alpha2);
    zet3 = linFuncRevers(c3, k3, alpha3);
    z0 = (alpha1 * zet1 + alpha2 * zet2 + alpha3 * zet3) / (alpha1 + alpha2 + alpha3);
    Z_train(i) = z0;
end

% Генерируем тестовую выборку
P_test = 200;
X_test = linspace(-100, 100, P_test);
Z_test = zeros(1, P_test);

for i = 1:P_test
    alpha1 = sigmFunc(a1, b1, X_test(i));
    alpha2 = sigmFunc(a2, b2, X_test(i));
    alpha3 = sigmFunc(a3, b3, X_test(i));
    zet1 = linFuncRevers(c1, k1, alpha1);
    zet2 = linFuncRevers(c2, k2, alpha2);
    zet3 = linFuncRevers(c3, k3, alpha3);
    z0 = (alpha1 * zet1 + alpha2 * zet2 + alpha3 * zet3) / (alpha1 + alpha2 + alpha3);
    Z_test(i) = z0;
end

% Строим нечеткую нейронную сеть и обучаем ее
trn_data = [X_train', Z_train'];
val_data = [X_test', Z_test'];
in_fis = genfis1(trn_data, 3, 'gbellmf');
% backpropagation
opt_backprop = anfisOptions('InitialFis', in_fis, ...
    'EpochNumber', 100, ...
    'DisplayANFISInformation', 0, ...
    'ValidationData', val_data, ...
    'DisplayErrorValues', 0, ...
    'OptimizationMethod', 0);
out_fis_backprop = anfis(trn_data, opt_backprop);
% hybrid
opt_hybrid = anfisOptions('InitialFis', in_fis, ...
    'EpochNumber', 100, ...
    'DisplayANFISInformation', 0, ...
    'ValidationData', val_data, ...
    'DisplayErrorValues', 0, ...
    'OptimizationMethod', 1);
out_fis_hybrid = anfis(trn_data, opt_hybrid);

writeFIS(out_fis_backprop, 'out_fis_backprop.fis');
writeFIS(out_fis_hybrid, 'out_fis_hybrid.fis');

in_fis_backprop = readfis('out_fis_backprop.fis');
ruleedit(in_fis_backprop);

in_fis_hybrid = readfis('out_fis_hybrid.fis');
ruleedit(in_fis_hybrid);
