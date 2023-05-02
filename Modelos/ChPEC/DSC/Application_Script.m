clearvars;
home;

%% %%%%%%%%%%%%%%%%%%%%%%
% Chose the case
%caso = 0; % no simulation
%caso = 1; %Unbalanced grid, voltage drop to 0.8 at 1s
caso = 2; %Balanced grid, step at iq ref


%% %%%%%%%%%%%%%%%%%%%%%%
% Simulation variables
Fn = 60;                    % Grid frequency
Ts_control = 1/(300*Fn);    % Sampling time of the Notch and DSC: 18kHz
Ts = Ts_control / 60;       % Step time of the simulation
Fsw = 6000;                 % Not really used, PWM 

X = 0.5;                    % Same reactance as in https://ieeexplore.ieee.org/document/9501204
L = X / 2 / pi / Fn;        %
R = X / 20;                 % 

Cdc = 1 / (2 * pi * Fn * 5);    % DC capacitance

Udc = 3^0.5;                % DC voltage that gives 1pu ac
Idc = 1.5/Udc;              

%% %%%%%%%%%%%%%%%%%%%%%%%%
% Some default values, if no case is chosen
VposStepTimes = [0 0.5 0.75];
VposStepValues = [1 0.8 1];

VnegStepTimes = [0 0.01];
VnegStepValues = [0 0.0];

IdStepTimes = [0 1];
IdStepValues = [0.0 0.0];

IqStepTimes = [0 1 1.4 1.7];
IqStepValues = [0 -0.25 0 -0.25];

EnDualTimes = [0 0.65 1.6];
EnDualValues = [0 1 0];

PdcStepTime = 0.05;
PdcIniVal = 0;
PdcFinVal = 0.0;

FixedDC = 0;

if FixedDC == 1
    VarDC =0;
else
    VarDC = 1;
end

DualType = 2;

Fdrop = 0.05;
Fdroptime = 0.5;
Frampslope = Fdrop / 1; 
Framptime = 15;


%% %%%%%%%%%%%%%%%%%%%%%%
% Controller
Fmin = 40;          % Minimum acceptable grid frequency (size of circ. buffers
zeta = 2^-0.5;      % zeta for notch filters           
Fcutout = 1000;     % cutout for low pass at the output of vdq+-, represents signal treatment

Kp = 4;             % empirical choice
Ti = L/R;           % not optimized for discrete with Suul method

Kpdc = 0.5;         % empirical choice
Tidc = 0.15;        % empirical choice   

%% %%%%%%%%%%%%%%%%%%%%%%
% Name of the model for simulation
nomemodelo = 'Application';

switch (caso)
    case 1
        % one that made the manuscript
        % Unbalanced voltages, voltage drop
        Ttot = 2;
        
        % DC link active
        FixedDC = 0;
        VarDC = 1;

        % Dual active
        EnDualTimes = [0 0.1];
        EnDualValues = [1 1];
        
        % Zero reactive current
        IqStepTimes = [0 1];
        IqStepValues = [0 0];
        
        % Voltage drop at time 1s
        VposStepTimes = [0 1]; 
        VposStepValues = [1 0.8];
        VnegStepTimes = [0 1];
        VnegStepValues = [0.1 0.08];
        
        % Frequency changes
        Fdroop = 1e10;
        Fdrop = 0.05;
        Fdroptime = 1;
        Frampslope = Fdrop / 1; 
        Framptime = 35;
        
        %%%%%%%%%%%%%%%%%%%%%%%
        % First simulation
        DualType = 0; %0 = Notch; 1 = DSC alphabeta ; 2 = DSC dq
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp(['Simulating notch: ',nomemodelo, '; Simulated time: ',num2str(Ttot), ' s']);
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        rawdata(:,:) = simulado.get('Application_Raw');
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp('Saving raw data');
        arquivo = fopen('Application_Unb_Notch.txt','w');
        for cnt = round(0.8/Ts_control):length(rawdata(:,1))
            fprintf(arquivo,'%e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e\n',rawdata(cnt, :));
        end
        fclose(arquivo);
        
        %%%%%%%%%%%%%%%%%%%%%%%
        % Second simulation
        DualType = 1; %0 = Notch; 1 = DSC alphabeta ; 2 = DSC dq
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp(['Simulating DSCab: ',nomemodelo, '; Simulated time: ',num2str(Ttot), ' s']);
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        rawdata(:,:) = simulado.get('Application_Raw');
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp('Saving raw data');
        arquivo = fopen('Application_Unb_DSCab.txt','w');
        for cnt = round(0.8/Ts_control):length(rawdata(:,1))
            fprintf(arquivo,'%e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e\n',rawdata(cnt, :));
        end
        fclose(arquivo);
        
        %%%%%%%%%%%%%%%%%%%%%%%
        % Third simulation
        DualType = 2; %0 = Notch; 1 = DSC alphabeta ; 2 = DSC dq
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp(['Simulating DSCdq: ',nomemodelo, '; Simulated time: ',num2str(Ttot), ' s']);
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        rawdata(:,:) = simulado.get('Application_Raw');
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp('Saving raw data');
        arquivo = fopen('Application_Unb_DSCdq.txt','w');
        for cnt = round(0.8/Ts_control):length(rawdata(:,1))
            fprintf(arquivo,'%e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e\n',rawdata(cnt, :));
        end
        fclose(arquivo);
                
        saveTXTfile = 0;

    %% %%%%%%%%%%%%%%%%%%%%%
    % Case 2
    case 2
        % Made the manuscript
        Ttot = 2; % 1 second

        % DC link active
        FixedDC = 0;
        VarDC = 1;

        % Dual active
        EnDualTimes = [0 1];
        EnDualValues = [1 1];
        
        % Step at reactive current
        IqStepTimes = [0 1];
        IqStepValues = [0 -0.1];
        %IqStepValues = [0 0.0];
        
        % No voltage changes
        VposStepTimes = [0 1]; %30/Fn]; %VposStepTimes = [0 30.25/Fn];
        VposStepValues = [1 1];
        VnegStepTimes = [0 1];
        VnegStepValues = [0.0 0.0];
        
        % Frequency drop
        Fdroop = 1e10;
        Fdrop = -0.01;
        Fdroptime = 0.75;
        Frampslope = -Fdrop / 2; 
        Framptime = 1.5;
        
        PdcStepTime = 0.00;
        PdcIniVal = 0;
        PdcFinVal = 0.0;

        
        %%%%%%%%%%%%%%%%%%%%%%%
        % First simulation
        DualType = 0; %0 = Notch; 1 = DSC alphabeta ; 2 = DSC dq
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp(['Simulating notch: ',nomemodelo, '; Simulated time: ',num2str(Ttot), ' s']);
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        rawdata(:,:) = simulado.get('Application_Raw');
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp('Saving raw data');
        arquivo = fopen('Application_Bal_Notch.txt','w');
        for cnt = round(0.8/Ts_control):length(rawdata(:,1))
            fprintf(arquivo,'%e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e\n',rawdata(cnt, :));
        end
        fclose(arquivo);
        
        %%%%%%%%%%%%%%%%%%%%%%%
        % Second simulation
        DualType = 1; %0 = Notch; 1 = DSC alphabeta ; 2 = DSC dq
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp(['Simulating DSCab: ',nomemodelo, '; Simulated time: ',num2str(Ttot), ' s']);
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        rawdata(:,:) = simulado.get('Application_Raw');
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp('Saving raw data');
        arquivo = fopen('Application_Bal_DSCab.txt','w');
        for cnt = round(0.8/Ts_control):length(rawdata(:,1))
            fprintf(arquivo,'%e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e\n',rawdata(cnt, :));
        end
        fclose(arquivo);
        
        %%%%%%%%%%%%%%%%%%%%%%%
        % Third simulation
        DualType = 2; %0 = Notch; 1 = DSC alphabeta ; 2 = DSC dq
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp(['Simulating DSCdq: ',nomemodelo, '; Simulated time: ',num2str(Ttot), ' s']);
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        rawdata(:,:) = simulado.get('Application_Raw');
        
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp('Saving raw data');
        arquivo = fopen('Application_Bal_DSCdq.txt','w');
        for cnt = round(0.8/Ts_control):length(rawdata(:,1))
            fprintf(arquivo,'%e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e\n',rawdata(cnt, :));
        end
        fclose(arquivo);
                
    otherwise
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
        disp('%% no simulation case chosen %%%%%%%%%%');
        disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%');
               
        Ttot = 2; % 1 second

        % DC link active
        FixedDC = 0;
        VarDC = 1;

        % Dual active
        EnDualTimes = [0 1];
        EnDualValues = [1 1];
        
        % Step at reactive current
        IqStepTimes = [0 1];
        IqStepValues = [0 -0.1];
        %IqStepValues = [0 0.0];
        
        % No voltage changes
        VposStepTimes = [0 1]; %30/Fn]; %VposStepTimes = [0 30.25/Fn];
        VposStepValues = [1 1];
        VnegStepTimes = [0 1];
        VnegStepValues = [0.0 0.0];
        
        % Frequency drop
        Fdroop = 1e10;
        Fdrop = -0.01;
        Fdroptime = 0.75;
        Frampslope = -Fdrop / 2; 
        Framptime = 1.5;
        
        PdcStepTime = 0.00;
        PdcIniVal = 0;
        PdcFinVal = 0.0;

        
        %%%%%%%%%%%%%%%%%%%%%%%
        % First simulation
        DualType = 2; %0 = Notch; 1 = DSC alphabeta ; 2 = DSC dq
    
        
        return
end







