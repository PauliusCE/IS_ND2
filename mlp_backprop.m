%close all
clear

%% Duomenys
% x - ivesties signalas, d1,d2,d3 - norimi atsakai (3 isejimai)
% Isejimo sluoksnio aktyvacija - sigmoide, todel d turi buti intervale (0,1)
n = 1:200;
x = sin(0.05*n) + 0.3*sin(0.2*n);

% Pavyzdiniai norimi atsakai (pakeisti savo uzduoties duomenimis)
d1 = 1./(1 + exp(-(sin(0.05*n))));
d2 = 1./(1 + exp(-(cos(0.05*n))));
d3 = 1./(1 + exp(-(sin(0.1*n))));

%% 1 sluoksnis (3 neuronai, tanh) - ivestys x(n) ir x(n-1)
w11_1 = rand(1); w12_1 = rand(1);
w21_1 = rand(1); w22_1 = rand(1);
w31_1 = rand(1); w32_1 = rand(1);
b1_1 = rand(1);
b2_1 = rand(1);
b3_1 = rand(1);

%% 2 sluoksnis (2 neuronai, tiesine funkcija)
w11_2 = rand(1); w12_2 = rand(1); w13_2 = rand(1);
w21_2 = rand(1); w22_2 = rand(1); w23_2 = rand(1);
b1_2 = rand(1);
b2_2 = rand(1);

%% 3 sluoksnis (3 neuronai, sigmoide)
w11_3 = rand(1); w12_3 = rand(1);
w21_3 = rand(1); w22_3 = rand(1);
w31_3 = rand(1); w32_3 = rand(1);
b1_3 = rand(1);
b2_3 = rand(1);
b3_3 = rand(1);

eta = 0.01;

%% Mokymas
for epocha = 1:50000
    for i = 2:length(x)          % nuo 2, nes reikia x(i-1)
        xn  = x(i);
        xn1 = x(i-1);

        %% --- Pirmyn eiga ---
        % 1 sluoksnio pasvertos sumos
        v1_1 = xn * w11_1 + xn1 * w12_1 + b1_1;
        v2_1 = xn * w21_1 + xn1 * w22_1 + b2_1;
        v3_1 = xn * w31_1 + xn1 * w32_1 + b3_1;
        % 1 sluoksnio aktyvacijos funkcija (tanh)
        y1_1 = tanh(v1_1);
        y2_1 = tanh(v2_1);
        y3_1 = tanh(v3_1);

        % 2 sluoksnio pasvertos sumos
        v1_2 = y1_1 * w11_2 + y2_1 * w12_2 + y3_1 * w13_2 + b1_2;
        v2_2 = y1_1 * w21_2 + y2_1 * w22_2 + y3_1 * w23_2 + b2_2;
        % 2 sluoksnio aktyvacijos funkcija (tiesine)
        y1_2 = v1_2;
        y2_2 = v2_2;

        % 3 sluoksnio pasvertos sumos
        v1_3 = y1_2 * w11_3 + y2_2 * w12_3 + b1_3;
        v2_3 = y1_2 * w21_3 + y2_2 * w22_3 + b2_3;
        v3_3 = y1_2 * w31_3 + y2_2 * w32_3 + b3_3;
        % 3 sluoksnio aktyvacijos funkcija (sigmoide)
        y1_3 = 1/(1 + exp(-v1_3));
        y2_3 = 1/(1 + exp(-v2_3));
        y3_3 = 1/(1 + exp(-v3_3));

        % Tinklo isejimai
        y1 = y1_3;
        y2 = y2_3;
        y3 = y3_3;

        %% --- Klaidos ---
        e1 = d1(i) - y1;
        e2 = d2(i) - y2;
        e3 = d3(i) - y3;

        %% --- Atgalinis klaidos sklidimas ---
        % Isejimo sluoksnis: fi3'(v) = y*(1-y)
        delta1_3 = y1_3 * (1 - y1_3) * e1;
        delta2_3 = y2_3 * (1 - y2_3) * e2;
        delta3_3 = y3_3 * (1 - y3_3) * e3;

        % 2 sluoksnis: fi2'(v) = 1 (tiesine)
        delta1_2 = 1 * (delta1_3 * w11_3 + delta2_3 * w21_3 + delta3_3 * w31_3);
        delta2_2 = 1 * (delta1_3 * w12_3 + delta2_3 * w22_3 + delta3_3 * w32_3);

        % 1 sluoksnis: fi1'(v) = 1 - tanh(v)^2 = 1 - y^2
        delta1_1 = (1 - y1_1^2) * (delta1_2 * w11_2 + delta2_2 * w21_2);
        delta2_1 = (1 - y2_1^2) * (delta1_2 * w12_2 + delta2_2 * w22_2);
        delta3_1 = (1 - y3_1^2) * (delta1_2 * w13_2 + delta2_2 * w23_2);

        %% --- Svoriu atnaujinimas ---
        % 3 sluoksnis
        w11_3 = w11_3 + eta * delta1_3 * y1_2;
        w12_3 = w12_3 + eta * delta1_3 * y2_2;
        w21_3 = w21_3 + eta * delta2_3 * y1_2;
        w22_3 = w22_3 + eta * delta2_3 * y2_2;
        w31_3 = w31_3 + eta * delta3_3 * y1_2;
        w32_3 = w32_3 + eta * delta3_3 * y2_2;
        b1_3 = b1_3 + eta * delta1_3;
        b2_3 = b2_3 + eta * delta2_3;
        b3_3 = b3_3 + eta * delta3_3;

        % 2 sluoksnis
        w11_2 = w11_2 + eta * delta1_2 * y1_1;
        w12_2 = w12_2 + eta * delta1_2 * y2_1;
        w13_2 = w13_2 + eta * delta1_2 * y3_1;
        w21_2 = w21_2 + eta * delta2_2 * y1_1;
        w22_2 = w22_2 + eta * delta2_2 * y2_1;
        w23_2 = w23_2 + eta * delta2_2 * y3_1;
        b1_2 = b1_2 + eta * delta1_2;
        b2_2 = b2_2 + eta * delta2_2;

        % 1 sluoksnis
        w11_1 = w11_1 + eta * delta1_1 * xn;
        w21_1 = w21_1 + eta * delta2_1 * xn;
        w31_1 = w31_1 + eta * delta3_1 * xn;
        w12_1 = w12_1 + eta * delta1_1 * xn1;
        w22_1 = w22_1 + eta * delta2_1 * xn1;
        w32_1 = w32_1 + eta * delta3_1 * xn1;
        b1_1 = b1_1 + eta * delta1_1;
        b2_1 = b2_1 + eta * delta2_1;
        b3_1 = b3_1 + eta * delta3_1;
    end
end

%% Tinklo atsakas po mokymo
Y1 = zeros(1,length(x));
Y2 = zeros(1,length(x));
Y3 = zeros(1,length(x));

for i = 2:length(x)
    xn  = x(i);
    xn1 = x(i-1);

    v1_1 = xn * w11_1 + xn1 * w12_1 + b1_1;
    v2_1 = xn * w21_1 + xn1 * w22_1 + b2_1;
    v3_1 = xn * w31_1 + xn1 * w32_1 + b3_1;
    y1_1 = tanh(v1_1);
    y2_1 = tanh(v2_1);
    y3_1 = tanh(v3_1);

    v1_2 = y1_1 * w11_2 + y2_1 * w12_2 + y3_1 * w13_2 + b1_2;
    v2_2 = y1_1 * w21_2 + y2_1 * w22_2 + y3_1 * w23_2 + b2_2;
    y1_2 = v1_2;
    y2_2 = v2_2;

    v1_3 = y1_2 * w11_3 + y2_2 * w12_3 + b1_3;
    v2_3 = y1_2 * w21_3 + y2_2 * w22_3 + b2_3;
    v3_3 = y1_2 * w31_3 + y2_2 * w32_3 + b3_3;

    Y1(i) = 1/(1 + exp(-v1_3));
    Y2(i) = 1/(1 + exp(-v2_3));
    Y3(i) = 1/(1 + exp(-v3_3));
end

figure
subplot(3,1,1); plot(n,d1,'b',n,Y1,'r'); legend('d1','y1'); title('1 isejimas')
subplot(3,1,2); plot(n,d2,'b',n,Y2,'r'); legend('d2','y2'); title('2 isejimas')
subplot(3,1,3); plot(n,d3,'b',n,Y3,'r'); legend('d3','y3'); title('3 isejimas')
