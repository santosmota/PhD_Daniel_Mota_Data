%%%% SINTEF - BEGIN %%%%

Ts_phy = 1/10000;
Ts_sim = Ts_phy;


%% System
systemBase = {};

% System baseValues
%systemBase.Sn = 60e3; % VA
systemBase.Sn = 2*44e6; % VA
systemBase.cosphi = 0.8; % 
systemBase.Pn = systemBase.cosphi * systemBase.Sn; % 
%systemBase.Vn = 400;  % V rms phase to phase
systemBase.Vn = 11000;  % V rms phase to phase
systemBase.fn = 50; % Hz
%systemBase.fn = 60; % Hz

systemBase.Vn_phase = systemBase.Vn/sqrt(3); % V
systemBase.Vn_phase_peak = systemBase.Vn_phase*sqrt(2); % V
systemBase.In   = systemBase.Sn/(systemBase.Vn*sqrt(3)) ; % A
systemBase.Zn   = systemBase.Vn*systemBase.Vn/systemBase.Sn ; % Ohm
systemBase.Rn   = systemBase.Zn; % Ohm
systemBase.Wn   = 2*pi()*systemBase.fn ; % rad/s
systemBase.Ln   = systemBase.Zn/systemBase.Wn ; % H
systemBase.Cn   = 1/(systemBase.Zn*systemBase.Wn) ; % F


%% SM

% Change to pu- input 
sm.fn=systemBase.fn; % [Hz] Rated electric frequency 
sm.Vn=systemBase.Vn; % [Vrms] Rated line voltage 
sm.Sn=systemBase.Sn; % [VA] Rated VA
sm.Vn_phase = sm.Vn/sqrt(3); % V
sm.Vn_phase_peak = sm.Vn_phase * sqrt(2);
sm.In   = sm.Sn/(sm.Vn*sqrt(3)) ; % A
sm.Zn   = sm.Vn*sm.Vn/sm.Sn ; % Ohm
sm.Rn   = sm.Zn; % Ohm
sm.Wn   = 2*pi()*sm.fn ; % rad/s
sm.Ln   = sm.Zn/sm.Wn ; % H
sm.Cn   = 1/(sm.Zn*sm.Wn) ; % F

sm.phaseInitial=0; %[rad] Initial phase angle of phase 1 (electric)
sm.initialSpeed=1 ;        % [pu] Initial turbine speed

%% Measurements
sm.V_measure_T=0.005; % [s] LP filter time constant for SM volatge measurement
sm.I_measure_T=0.005; % [s] LP filter time constant for SM current measurement
sm.P_measure=0.04; % LP filter time constant for SM power measurement
sm.Q_measure=0.04; % LP filter time constant for SM reactive power measurement


%% Wind farm - Collector system
col = {};
col.Un = 33000;                     % [Vrms] Line voltage
col.Uanp = col.Un*sqrt(2/3);        % [Vpeak] Phase to ground voltage 
col.cosphi = 0.8;                   % [-] Power factor
col.Sn = 12e6/col.cosphi;           % [VA] Wind farm power: 13.33MVA for cosphi=0.9
col.Iap = col.Sn/col.Un*sqrt(2/3);  % [Vpeak] phase to ground voltage 
col.Trafo.xsc = 0.12;               % [pu] Transformer short circuit reactance 
col.Trafo.rsc = 0.005;              % [pu] Transformer short circuit resistance

%95 mm2
%17MVA at 33kV
% DIGISILENT POWER FACTORY - 30kV Paper	NEKBA 3x95rm 18/30kV
% VERY SIMILAR TO OTHER CABLES 20kV and 30kV cables
% but not the most capacitive of them
col.Cable.Rpos = 194.800E-3;        % [Ohm/km] Resistance positive sequence
col.Cable.Lpos = 379.998E-6;        % [H/km] Inductance positive sequence
col.Cable.Cpos = 250.000E-9;        % [F/km] Capacitance positive sequence
col.Cable.Rzero = 779.200E-3;       % [Ohm/km] Resistance zero sequence
col.Cable.Lzero = 1.520E-3;         % [H/km] Inductance zero sequence
col.Cable.Czero = 246.900E-9;       % [F/km] Capacitance positive sequence

col.Cable.Limport = 4;              % [km] Import lenght
col.Cable.LinterWT = 2;             % [km] Inter WT lenght


%% Wind turbine 1 - Specification
wt1 = {};

% Sampling time, system frequency, switching frequency
wt1.Fn = systemBase.fn;
wt1.Fs_control = 1/Ts_phy;          % [Hz] Sampling frequency controller
wt1.Fsw = 5e3;                      % [Hz] Sampling frequency PWM
wt1.Ts_control = 1/wt1.Fs_control;  % [s] Sampling time controller A/D converter

% Grid-side converter
wt1.Pn = 4e6;                       % [W] Active power
wt1.cosphi = 0.8;                   % [-] Power factor
wt1.Sn = wt1.Pn/wt1.cosphi;         % [VA] Apparent power
wt1.Un = 690;                       % [Vrms] Line voltage (at LV side of trafo)
wt1.Uanp = wt1.Un*sqrt(2/3);        % [Vpeak] Phase to ground voltage (at LV side of trafo)
wt1.Uabp = wt1.Un*sqrt(2);          % [Vpeak] Line voltage (at LV side of trafo)
wt1.Iap = wt1.Sn/wt1.Un*sqrt(2/3);  % [Apeak] Line current (at LV side of trafo)
wt1.Udc = 1200;                     % [Vdc] Rated dc voltage
wt1.Idc = wt1.Sn/wt1.Udc;           % [Adc] Rated dc current
wt1.Cdc = wt1.Idc/(2*wt1.Fn*wt1.Udc); % [F] DC link capacitor
wt1.LCL.l2 = 0.08;                  % [pu] Short circuit reactance of trafo
wt1.LCL.r2 = 0.005;                 % [pu] Short circuit resistance of trafo
wt1.LCL.r1 = 0.01;                  % [pu] LCL main reactance resistance
wt1.dampDC = 0.8; %sqrt(2)/2;             % [-] damping Udc controller 

%% Wind turbine 1 - Grid-converter design
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp('% WIND TURBINES');
[designOk, wt1.LCL] = GC_LCLdesign(wt1);
if designOk == 1 
    [wt1.CurrContSingle, wt1.DCVContSingle] = GC_PItuning(wt1,0);
    [wt1.CurrContDual, wt1.DCVContDual] = GC_PItuning(wt1,1);
end

%% Wind turbine 1 - Controllers
% Current 
wt1.CurrCont.PImax = 1.5;           % [pu] max value of PI output
wt1.CurrCont.PImin = -1.5;          % [pu] min value of PI output
wt1.CurrCont.x = wt1.LCL.l1;        % [pu] reactance for dq decoupling
wt1.CurrCont.f_LPF_noise = wt1.LCL.fres;    % [Hz] low pass cutout filter
wt1.CurrCont.zeta = sqrt(2)/2;      % [pu] damping coefficient for notch filters
wt1.filtertype = 1;                 % None = 0; Notch = 1; DSC = 2

%DC link voltage
wt1.DCVCont.PImax = 1.5;            % [pu] Max value of PI output
wt1.DCVCont.PImin = -1.5;           % [pu] Min value of PI output
wt1.DCVCont.Start = 0.2;

%AC voltage controller
wt1.ACVCont.PImax = 1.5;            % [pu] Max value of PI output
wt1.ACVCont.PImin = -1.5;           % [pu] Min value of PI output
wt1.ACVCont.kg = 1;                 % [pu/pu] Loop gain kg(kp + 1/sTi)
wt1.ACVCont.kp = 0.00;              % [pu/pu] Proportional gain kg(kp + 1/sTi)
wt1.ACVCont.Ti = 0.15;               % [s] Integral time
wt1.ACVCont.kiq_droop = 0.00;

%Q consensus controller
wt1.Qctrl.Umax = 1.05;
wt1.Qctrl.Umin = 0.95;
wt1.Qctrl.deltaUmaxPos = (wt1.Qctrl.Umax - wt1.Qctrl.Umin);
wt1.Qctrl.deltaUmaxNeg = -wt1.Qctrl.deltaUmaxPos; 
wt1.Qctrl.Ti = 5;
wt1.Qctrl.Kg = 1;
wt1.Qctrl.Kp = 0.05;


% comment under the FLEX
% Daniel used Ti = 10x the calculated value

%% Initial conditions

sm.Vt0 = 1;             % [pu] SM stator voltage
wt1.Vac0 = sm.Vt0;      % [pu] WT1 AC voltage

