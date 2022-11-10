% Date: 2022-10-07
% What: runs the SimpleMass.slx and stores the data in a text file (CSV)
% Who: Daniel Mota
% Disclaimer: no guarantees given, use at your own risk

clearvars;

%%
% caso = -1; % no storage of files, no simulatation
% caso = 0; % no storage of files, still simulates
caso = 1; % 3MW step, store text file
% caso = 2; % 5MW step, store text file
% caso = 3; % WF 12MW out, store text file

%%
%saveTextFile = 0; %DO NOT save files
if caso > 0
    saveTextFile = 1; %save files
else
    saveTextFile = 0;
end

%total simulation time
Ttot = 200;
Ts = 0.005;

%name of the simulink model
nomemodelo = 'SimpleMass'; 

%Total apparent power
Sn = 2*44e6;
np = 1; %numper of pair of poles, same mechanical and electrical frequencies
Fn = 50; %Hz

%angular frequency
omegan = 2 * pi * Fn / np;

%nominal torque would produce P = Sn
Tn = Sn / omegan;

H = 2.5; 
J = 2 * H * Sn / omegan^2;


%Governor
gov = [];
gov.FD = 1;                 % Hz
gov.fD = gov.FD / Fn;       % pu of frequency
gov.KD = 6e6;               % W/Hz
gov.kD = gov.KD / Sn * Fn;  % per unit of power / per unit of frequency
gov.PDmax = 20e6;           % W
gov.pDmax = gov.PDmax / Sn; % pu of power
%First and second time constants of the governor
gov.Tgt1 = 0.1; %representing a fuel system
gov.Tgt2 = 0.4; %the larger time constant
%Dead time for the gas valve
gov.DeadTimeValve = 0.1;

%Battery
bat = [];
bat.Pn = 3e6;
bat.FN = 0.0;
bat.fN = bat.FN / Fn;
bat.KN = 3e6;               
bat.kN = bat.KN / bat.Pn * Fn; 
bat.PNmax = bat.Pn;
bat.pNmax = bat.PNmax / bat.Pn;
bat.T1 = 0.05;
bat.SOCmaxcut = 75e3; 
bat.SOCmaxrest = 0.9*bat.SOCmaxcut;              % Wh max, after that stops charging
bat.SOCini = 0.6*bat.SOCmaxcut;                  % Wh initial
bat.SOCminrest = 0.1*bat.SOCmaxcut;                
bat.SOCmincut = 0.05*bat.SOCmaxcut;                

%Fuel cell
fc = [];
fc.Pmax = 6e6;
fc.T1 = 0.5;
fc.DeadTime = 0.25;

%Wind farm
wf = [];
wf.StepTime = 1010;
wf.Pini = 12e6;
wf.Pstep = -12.e6;

%secondary
sec.Ti = 15;  % 4; %integrator time of secondary control
sec.Rate = 0.005; %maximum rate of secondary control
sec.Kp = 0.25; %proportional gain of secondary control
sec.T_on_delay = 25; %on-delay 

%Load
load = [];
load.Pini = 44e6;
load.Pstep = 3e6;
load.StepTime = 10;

% governor initial power
gov.Pini = load.Pini - wf.Pini;


% cases for transients 
switch caso
    case 1
        load.Pstep = 3e6;
        load.StepTime = 10;
        wf.StepTime = 1010;
        filename = 'RawData_Case1.csv';
    case 2
        load.Pstep = 5e6;
        load.StepTime = 10;
        wf.StepTime = 1010;
        filename = 'RawData_Case2.csv';
    case 3
        load.StepTime = 1010;
        wf.StepTime = 10;
        filename = 'RawData_Case3.csv';
end


if caso >= 0
    %%
    disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
    disp(['Simulating for a total time:',num2str(Ttot), ' s']);
    simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
    rawdata(:,:) = simulado.get('rawdata');
end

%%
if saveTextFile == 1 % saving text files
    %Indices %not really necessary, made only for code checking
    Ind = [];
    Ind.time = 1;
    Ind.F = 2;
    Ind.Pload = 3;
    Ind.Pinert = 4;
    Ind.Pgov = 5;
    Ind.Pbat = 6;
    Ind.Pfc = 7;
    Ind.Pwf = 8; 
    Ind.SOC = 9; 
 
    disp('%%%%%%%%%%%%%%%%%%%%%%%%%');
    disp('Saving raw data');
    arquivo = fopen(filename,'w');
    fprintf(arquivo, 'time,F,Pload,Pinert,Pgov,Pbat,Pfc,Pwf,SOC\n');
    
    for cnt = 1:length(rawdata(:,Ind.time))
        fprintf(arquivo, '%e,%e,%e,%e,%e,%e,%e,%e,%e\n',rawdata(cnt, :));
        disp(['Sample: ',num2str(cnt)]);
    end
    fclose(arquivo);
end    
