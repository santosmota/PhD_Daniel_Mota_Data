clearvars;
close all;

Sn = 88;            % MW
Tgov1 = 0.1;        % s
Tgov2 = 0.4;
Tess = 0.05;        % s
H = 2.5;            % s
Fn = 50;            % Hz

Kgt = [12 10  8  6  4  2 0];    % MW/Hz
Kess = [0  2  4  6  8 10 12];   % MW/Hz

Pessmax = 3;

KGT =  Kgt(7);
KESS = Kess(7);


StepMW = 6;

