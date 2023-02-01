% The values in volts, amps, ohms are purposefully chosen
%   as 1V phase to neutral amplitude and 1A line amplitude
%   this means that the Sn = 1.5 VA

clearvars;


Ts = 1e-6;
Ts_cont = 1/10000; 
Ts_pwm = 1/200000;
Fsw = 1/0.0004;         % Hz, to make it multiple of Ts

Vanp = 1;
Iap = 1;
Sn = 1.5;               % VA
Fn = 50;                % Hz
wn = 2*pi*Fn;           % rad/s
Vrms = (3/2)^0.5;       % V phase to phase rms

Vdc = 2 ; % 1.2*3^0.5;                % 2 would be a rounded value for 1.2*3^0.5... 
Idc = Sn / Vdc;         % A

Vamppos = 1;            % V
Vampline = 3^0.5;       % V
Vampneg = 0.1;          % V

% Trafo
Rt = 0.005;             % pu
Xt = 0.05;              % pu
Lt = Xt / wn;           % H

% Main reactor
Lr = Vdc / (0.8 * 2^0.5 * ( Sn / 3^0.5 / Vrms) * Fsw);
Xr = Lr * wn; 
disp('Current controller PI transfer function = kp (1 + 1/(sTi))');
disp(['    Reactor impedance Xr = ',num2str(Xr),' s']);

Rr = 0.005;             % Ohms
%Xr = 0.35;             % Ohms
%Lr = Xr / wn;          % Henry

% Capacitance branch
Xf = 20;                % Ohm  Xc = 1/(wC)  =>  C = 1 / (w Xc)
Cf= 1 / (wn * Xf);      % F
fres = 1 / (2 * pi) * sqrt((Lt + Lr )/(Lt * Lr * Cf)); % Hz
Rf = 1 / ( 3 * 2 * pi * fres * Cf); % Ohm
disp(['    Resonance frequency fres = ',num2str(fres),' s']);

% DC link
H = 0.0025;
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




%% GRID CONVERTER - 5MVA
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% GRID CONVERTER / MAYBE FROM A WIND TURBINE');
gc = {};

gc.Sn = 5e6; % 1.5; %
gc.Fn = 50;
gc.Ts_control = 1/10000;            % [s] Sampling time
gc.Fs_control = 10000;              % [Hz] Sampling frequency controller
gc.Fsw = 5000; % 1/0.0003;                  % [Hz] Sampling frequency PWM
gc.Ts_pwm = 1/200000;

gc.TenDCLinkExch = 0.00;

% Grid-side converter
gc.cosphi = 0.8;                    % [-] Power factor
gc.Pn = gc.cosphi * gc.Sn;          % [W] Active power
gc.Un = 690; % (3/2)^0.5; %                        % [Vrms] Line voltage (at LV side of trafo)
gc.Uanp = gc.Un*sqrt(2/3);          % [Vpeak] Phase to ground voltage (at LV side of trafo)
gc.Uabp = gc.Un*sqrt(2);            % [Vpeak] Line voltage (at LV side of trafo)
gc.Iap = gc.Sn/gc.Un*sqrt(2/3);     % [Apeak] Line current (at LV side of trafo)
gc.Udc = 1.2*gc.Un*2^0.5;           % [Vdc] Rated dc voltage
gc.Idc = gc.Sn/gc.Udc;              % [Adc] Rated dc current
gc.H = 0.5; % 0.0025;                      % [s] 
% gc.Cdc = 2 * gc.Sn * gc.H / gc.Udc^2; % [F] DC link capacitor
gc.Cdc = gc.Idc/(2*gc.Fn*gc.Udc);
gc.LCL.l2 = 0.05;                   % [pu] Short circuit reactance of trafo
gc.LCL.r2 = 0.005;                  % [pu] Short circuit resistance of trafo
gc.LCL.r1 = 0.01;                  % [pu] LCL main reactance resistance
gc.dampDC = 0.8; sqrt(2)/2;              % [-] damping Udc controller 

%% Wind turbine 1 - Grid-converter design
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% DESIGN LCL');
[designOk, gc.LCL] = GC_LCLdesign_202301(gc);
if designOk == 1 
    [gc.CurrContSingle, gc.DCVContSingle] = GC_PItuning_202301(gc,0);
    [gc.CurrContDual, gc.DCVContDual] = GC_PItuning_202301(gc,1);
end


