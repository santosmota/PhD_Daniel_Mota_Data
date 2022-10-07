% Date: 2022-10-07
% What: runs the SimpleMass.slx and stores the data in a text file (CSV)
% Who: Daniel Mota
% Disclaimer: no guarantees given, use at your own risk

clearvars;

%%
%caso = 0; % no storage of files 
caso = 1; % store text file

%%
%saveTextFile = 0; %DO NOT save files
if caso > 0
    saveTextFile = 1; %save files
else
    saveTextFile = 0;
end

%total simulation time
Ttot = 80;

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
kgov_WHz = 8.8e6;  % will use step of 4.4MW, 5% of the installed MVA 88MWVA
kgov = kgov_WHz / Sn * Fn; % for 13.2MW/Hz, means 7.5 gain, 

%RateSec = 1/1; %maximum rate of secondary control
Tsec = 4; %integrator time of secondary control
Kpsec = 0; %proportional gain of secondary control

Tsec_on_delay = 25; %on-delay to show difference between primary and secondary control 

%First and second time constants of the governor
Tgt1 = 0.1; %representing a fuel system
Tgt2 = 0.4; %the larger time constant
%Dead time for the gas valve
DeadTimeValve = 0.1;


%Initial power level
Peini = 44e6/Sn;

%Power step - a large motor start (5% of the nominal power)
Pestep = 4.4e6/Sn;
StepTime = 10;

%%
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
disp(['Simulating for a total time:',num2str(Ttot), ' s']);
simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
rawdata(:,:) = simulado.get('rawdata');

%%
if saveTextFile == 1 % saving text files
    %Indices %not really necessary, made only for code checking
    Ind = [];
    Ind.time = 1;
    Ind.f = 2;
    Ind.e = 3;
    Ind.pload = 4;
    Ind.pmec = 5;
    Ind.pinert = 6;
    Ind.pprim = 7;
    Ind.psec = 8; 
 
    disp('%%%%%%%%%%%%%%%%%%%%%%%%%');
    disp('Saving raw data');
    if caso == 1
        arquivo = fopen('SimpleMass_RawData.csv','w');
        fprintf(arquivo, 'time,f,e,pload,pmec,pinert,pprim,psec\n');
    %elseif caso == 2 
    %    arquivo = fopen('SimpleMass_One_Raw.txt','w');
    %elseif caso == 3 
    %   arquivo = fopen('SimpleMass_One_SlowerSec_Raw.txt','w');
    end
    
    for cnt = 1:length(rawdata(:,Ind.time))
        fprintf(arquivo, '%e,%e,%e,%e,%e,%e,%e,%e\n',rawdata(cnt, :));
        disp(['Sample: ',num2str(cnt)]);
    end
    fclose(arquivo);
end    
