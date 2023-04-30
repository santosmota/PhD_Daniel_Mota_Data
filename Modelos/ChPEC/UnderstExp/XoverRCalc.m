clear;
home;
cd 'C:\Users\daniemot\OneDrive - NTNU\Publications\2021_PosNegSequences\matlab\Basics'

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculation of the total impedance seen from the LSC
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fn = 60;
wn = 2*pi*fn;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% At the base of 2 * Generators
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Sb_gen = 88e6;                      %VA of 2 generators
Ub_gen = 11e3;                      %V of the main busbar
Ib_gen = Sb_gen / Ub_gen / 3^0.5;   %Base current at 2*Gen base
Zb_gen = Ub_gen^2 / Sb_gen;         %Zb at the 2*Gen base

xd_gen = 0.299;
rs_gen = 0.0242;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Breakers at the 11kV
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Rbr = 0.01;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Load at the 11kV
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Pload = 0.64 * 70e6;                 %W load
Rload = Ub_gen^2 / Pload;            %Ohm
rload_gen = Rload / Zb_gen;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Converter bases
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Sb_con = 9.65e6;                            %VA of LSC
Ub_con_hv = 11e3;                            %V of the main busbar
Ib_con_hv = Sb_con / Ub_con_hv / 3^0.5;     %Base current at Conv HV base
Zb_con_hv = Ub_con_hv^2 / Sb_con;           %Zb at the Conv HV base

Ub_con_lv = 690;                            %V of the main busbar
Ib_con_lv = Sb_con / Ub_con_lv / 3^0.5;     %Base current at 2*Gen base
Zb_con_lv = Ub_con_lv^2 / Sb_con;           %Zb at the 2*Gen base

Lb_con_lv = Zb_con_lv / wn;           %Zb at the 2*Gen base
Cb_con_lv = 1 / Zb_con_lv / wn;           %Zb at the 2*Gen base

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Converter DC voltage
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Udc = 1200;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Transfomer
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xt_con = 0.06;
rt_con = 0.005;

Lt_con_lv = xt_con * Lb_con_lv; 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Resistance of main reactor
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
rr_con = 0.01;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Shunt capacitor
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
c_con = 0.05;
xc_con = 1 / c_con; 

C_con_lv = c_con * Cb_con_lv;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Moving what is not at to the conveter base
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xd_con = xd_gen * Sb_con / Sb_gen;
rs_con = rs_gen * Sb_con / Sb_gen;
rbr_con = Rbr / Zb_con_hv; 
rload_con = rload_gen * Sb_con / Sb_gen;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculating Lr and xr for a series of switching frequencies
% Lr = Udc / (8 * fsw * 0.1 * 2^0.5 * Ib) - Brantsæater 2015
% lr = xr = Lr / Lb;
N = 151;
fswmin = 2500;
fswmax = 4000;

fsw = linspace(fswmin,fswmax,N);
Lr = zeros(1,N);
xr = zeros(1,N);

for col = 1:N
    Lr(col) = Udc / (8 * fsw(col) * 0.1 * 2^0.5 * Ib_con_lv);
end
xr = (1/Lb_con_lv) * Lr;

figure(1)
plot(fsw,xr);
xlabel('Switching frequency (Hz)') 
ylabel('Main reactance (pu)') 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculating resonance frequency and Rc
% fres = 1 / (2 * pi) * sqrt((Lr + Lt_con_lv)/(Lr * Lt_con_lv * C_con_lv)) - Brantsæater 2015
% Rc   = 1 / 3 * 1 / (2 * pi * fres * C_con_lv);

fres = zeros(1,N);
Rc = zeros(1,N);
rc = zeros(1,N);

for col = 1:N
    fres(col) = 1 / (2 * pi) * sqrt((Lr(col) + Lt_con_lv)/(Lr(col) * Lt_con_lv * C_con_lv));
    Rc(col) = 1 / 3 * 1 / (2 * pi * fres(col) * C_con_lv);
    rc(col) = Rc(col) / Zb_con_lv;
end
xr = (1/Lb_con_lv) * Lr;

figure(2)
plot(fsw,fres);
xlabel('Switching frequency (Hz)') 
ylabel('LCL resonance frequency (Hz)') 

figure(3)
plot(fsw,rc);
xlabel('Switching frequency (Hz)') 
ylabel('Damping resistor (pu)') 


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculating the total impedance
zgen_con = rs_con + 1i * xd_con;
zpcc_con = (zgen_con + rbr_con)*rload_con / (zgen_con + rbr_con + rload_con); 
ztrlv_con = zpcc_con + rbr_con + rt_con + 1i*xt_con;

ztot_con = zeros(1,N);
xoverr = zeros(1,N);

for col = 1:N
    zc_con = rc(col) - 1i * xc_con; 
    ztot_con(col) = rr_con + 1i*xr(col) + zc_con*ztrlv_con/(zc_con+ztrlv_con);
    xoverr(col) = imag(ztot_con(col))/real(ztot_con(col));
end
figure(4)
plot(fsw,xoverr);
xlabel('Switching frequency (Hz)') 
ylabel('X/R (pu)') 


disp('Start saving text file with X over R data')
% fsw fres rc xr xoverr 
arquivo = fopen('XoverRCalculation.txt','w');
for col = 1:N
    fprintf(arquivo,'%f, %f, %f, %f, %f\n',fsw(col),fres(col),rc(col),xr(col),xoverr(col));
end
fclose(arquivo);



