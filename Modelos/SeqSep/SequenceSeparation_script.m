% The values in volts, amps, ohms are purposefully chosen
%   as 1V phase to neutral amplitude and 1A line amplitude
%   this means that the Sn = 1.5 VA

clearvars;

Ts = 1e-6;
Ts_cont = 1/10000; 
Ts_pwm = 1/200000;
Fsw = 1/0.0003;      % Hz, to make it multiple of Ts

Sn = 1.5;  		% VA
Fn = 50;		% Hz
wn = 2*pi*Fn;           % rad/s
Vrms = (3/2)^0.5;	% V phase to phase rms

Vdc = 2;		% rounded value for 1.2*3^0.5

Vamppos = 1;
Vampline = 3^0.5; 
Vampneg = 0.1;

% Trafo
Rt = 0.005;  		% pu
Xt = 0.08;  		% pu
Lt = Xt / wn;       % Henry

% Main reactor
Lr = Vdc / (0.8 * 2^0.5 * ( Sn / 3^0.5 / Vrms) * Fsw);
Xr = Lr * wn; 

Rr = 0.005;         % Ohms
%Xr = 0.35;          % Ohms
%Lr = Xr / wn;       % Henry

% Capacitance branch
Xf = 20;                % Ohm  Xc = 1/(wC)  =>  C = 1 / (w Xc)
Cf= 1 / (wn * Xf);
fres = 1 / (2 * pi) * sqrt((Lt + Lr )/(Lt * Lr * Cf));
Rf = 1 / ( 3 * 2 * pi * fres * Cf);

% DC link
H = 0.025;
Cdc = 2 * Sn * H / Vdc^2;


%
Tsum = 2 / (2 * pi * fres) + 0.5 / Fsw;

% Equation (13)
% PI controller parameters
halfTs = 0.5*Ts_cont;
Ti_current = (Lr/Rr) + halfTs;
disp('Current controller PI transfer function = kp (1 + 1/(sTi))');
disp(['    Sum of small time constants Tsum = ',num2str(Tsum),' s']);
disp(['    Ti = ',num2str(Ti_current),' s']);
%Kp_current = 0.5* Rr * (Ti_current - halfTs)/(Tsum + halfTs);
Kp_current = Rr * (Ti_current - halfTs)/(Tsum + halfTs);
disp(['    kp = ',num2str(Kp_current),' pu/pu']);
disp('    Current feedback from converter before capacitance!');
