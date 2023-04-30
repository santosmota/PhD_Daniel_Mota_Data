clearvars;
%home;
cd 'C:\Users\daniemot\OneDrive - NTNU\Publications\2021_PosNegSequences\matlab\Basics' 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simplest RL between two voltages
% Grid voltage 
%   Positive sequence in series with negative sequence
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

nomemodelo = 'Basics_01';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simulation cases
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%caso = 1;  % Comparing the transducers
            % Harsh connection at time zero 
            % 0.1V positive sequence voltage
            % no negative sequence
            % zeta = 1 
            
%caso = 2;   % DDLPF vs Notch vs AMA
            % Harsh connection at time zero with Vpos = 1 
            % zeta = 1
            NegativePositive = 0; %if 1: negative step at pos seq.,
                              %else: positive step at neg. seq.

%caso = 3;   % DDLPF vs Notch vs AMA
            % Harsh connection at time zero with Vpos = 1 
            % step at Iq at t=0.5
            % zeta = 1
                              
caso = 0;                              
            
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Common variables
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Ttot = 1.0;
% Sampling time, system frequency, switching frequency
Ts_control = 1/20000;   % for measuremetn control
Ts_PWM = 1/200000;      % for the PWM block
fsw = 2500;             % necessary for inner workuing of PWM block
fn = 60;                % easier to deal with 20ms period than 16,6667
                        % não agradou a todos, tem que atar as simulacoes
                        % à plataforma.
% Voltage bases
Uanp = 1;               % peak phase to neutral voltage
Uabp = Uanp * 3^0.5;    % peak line voltage
Udc = Uanp * 3^0.5;     % dc voltage - set to no gain - as dc is constant in this sim.
% Load / impedance between voltage sources
X = 0.5;                % reactance in Ohm
L = X / 2 / pi / fn;    % inductance in H
R = X/20;               % resistance in Ohm
Z = (X^2 + R^2)^0.5;    % absolute value of the total impedance
Phi = atan (X/R);       % power angle of the impedance
Tau = L / R;            % time constant
% PI regulator
Ti = Tau;               % Main pole cancelling
Kp = 4;%2;%0.5;                 % A guess, values on the range of 5 make LPF based unstable

% Some default choices
% also usefull when no simulation is run from this script
% Default choices fot the filters in the Notch based transducer
f_LPF_noise = 1000;
%zeta = 2^0.5/2;
zeta = 1; %for "fairness" with the slow LPF based
% Default choices fot references and setpoint
idref = 0;
iqref_StepTime = 10000.5;
iqref_InitialLevel = 0.0;
iqref_FinalLevel = 0.0;
% mode defaul choices
EnableInverter = 1;     % 1 = power converter, 0 transducer bench marking
DDLPF_Notch = -1;       % -1=DDLPF , 1=Notch based
Select_AMA = 0;         % AMA not selected, has precedence over DDLPF and Notch
                        % AMA is not stable with Kp = 2, with 0.5 it was
                        % but it performs worse, very much worse than the
                        % DDLPF
%%%%%%%%
V_PosSeq_StepTime = 0.5;
V_PosSeq_InitialValue = 1;
V_PosSeq_FinalValue = 0.8;
%%%%%%%%        
V_NegSeq_StepTime = 1000.1;
V_NegSeq_InitialValue = 0;
V_NegSeq_FinalValue = +0.2;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simulation cases
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
switch caso
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Caso 1 - Transducer comparison
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case 1
        disp('Simulation case: 01 - Comparing transducers - zeta 0.707')
        Ttot = 0.260;
        
        EnableInverter = 0;    %short circuits inverter voltage
                                %inverts the igrid measurement direction
                                
        Rodriguez_Brogan = -1 ; % 1 for Notch, -1 for DDLPF
                                % actually irrelevant for this case
               
        V_PosSeq_StepTime = 10000;
        V_PosSeq_InitialValue = 0.1;
        V_PosSeq_FinalValue = 0.1;
        
        V_NegSeq_StepTime = 1000;
        V_NegSeq_InitialValue = 0;
        V_NegSeq_FinalValue = 0;
        
        %zeta = 2^0.5/2;
        zeta = 1;
        
        simulacao = sim(nomemodelo, 'SimulationMode', 'accelerator');
        
        aux = simulacao.get('BenchPositive');
        %assignin('base','BenchPositive',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving txt files, lot of hardcoded things
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text files: BenchPositive');
        % time id iq idnotch iqnotch idlpf iqlpf idama iqama
        fComparison = fopen('BenchPositive.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%f, %f, %f, %f, %f, %f, %f, %f, %f\n',aux(c,:));
        end
        fclose(fComparison);
                
        aux = simulacao.get('BenchNegative');
        %assignin('base','BenchNegative',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving txt files, lot of hardcoded things
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text files: BenchNegative');
        % time id iq idnotch iqnotch idlpf iqlpf idama iqama
        fComparison = fopen('BenchNegative.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%f, %f, %f, %f, %f, %f, %f, %f, %f\n',aux(c,:));
        end
        fclose(fComparison);
        disp('End of Script');
        
        
        aux = simulacao.get('BenchVoltPos');
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving txt files, lot of hardcoded things
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text files: BenchVoltPos');
        % time id iq idnotch iqnotch idlpf iqlpf idama iqama
        fComparison = fopen('BenchVoltPos.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%f, %f, %f, %f, %f, %f, %f, %f, %f\n',aux(c,:));
        end
        fclose(fComparison);
                
        aux = simulacao.get('BenchVoltNeg');
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving txt files, lot of hardcoded things
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text files: BenchVoltNeg');
        % time id iq idnotch iqnotch idlpf iqlpf idama iqama
        fComparison = fopen('BenchVoltNeg.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%f, %f, %f, %f, %f, %f, %f, %f, %f\n',aux(c,:));
        end
        fclose(fComparison);
        disp('End of Script');
        
        
        aux = simulacao.get('viabcpqui');
        %assignin('base','viabcpqui',aux); Do not need that if I can use aux directly
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving txt files, lot of hardcoded things
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text files: viabcpqui');
        % time id iq idnotch iqnotch idlpf iqlpf idama iqama
        fComparison = fopen('viabcpqui.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n',aux(c,:));
        end
        fclose(fComparison);
        disp('End of Script');
        
        return

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Case 2 - Comparing regulators
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
    case 2
        disp('Simulation case 3: Rodriguez and Brogan, Pos step 1->0.8 at t=0.5')
        Ttot = 1;
        idref = 0.0;
        
        EnableInverter = 1;    %short circuits inverter voltage
                                %inverts the igrid measurement direction
        
        %DDLPF_Notch = -1;       % -1=DDLPF , 1=Notch based
        Select_AMA = 0;         % AMA not selected, has precedence over DDLPF and Notch                
        zeta = 1;
        
        if NegativePositive == 1
            V_PosSeq_StepTime = 0.5;
            V_PosSeq_InitialValue = 1;
            V_PosSeq_FinalValue = 0.8;
        
            V_NegSeq_StepTime = 10000.25;
            V_NegSeq_InitialValue = 0.0;
            V_NegSeq_FinalValue = 0;
        else
            V_PosSeq_StepTime = 10000.5;
            V_PosSeq_InitialValue = 1;
            V_PosSeq_FinalValue = 0.8;
        
            V_NegSeq_StepTime = 0.5;
            V_NegSeq_InitialValue = 0.0;
            V_NegSeq_FinalValue = 0.2;
        end
            
        iqref_StepTime = 10000.760;
        iqref_InitialLevel = 0.0;
        iqref_FinalLevel = -0.2;
                                        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        DDLPF_Notch = -1 ; % 1 for Brogan, -1 for Rodriguez
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        aux = simulado.get('viabcpqui');
        %assignin('base','GridVoltDrop',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV file first simulation
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text file grid voltage change - Rodriguez');
        % time vga vgb vgc vca vcb vcc ia ib ic p q u i
        if NegativePositive == 1
            auxfile = fopen('viabcpqui_Pos_lpf.txt','w');
        else
            auxfile = fopen('viabcpqui_Neg_lpf.txt','w');
        end
        for c = 1:TotalSamplesSim
            fprintf(auxfile,'%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n',aux(c,:));
        end
        fclose(auxfile);
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        DDLPF_Notch = +1 ; % 1 for Brogan, -1 for Rodriguez
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        aux = simulado.get('viabcpqui');
        %assignin('base','GridVoltDrop',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV file first simulation
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text file grid voltage change - Brogan');
        % time vga vgb vgc vca vcb vcc ia ib ic p q u i
        if NegativePositive == 1
            auxfile = fopen('viabcpqui_Pos_notch.txt','w');
        else
            auxfile = fopen('viabcpqui_Neg_notch.txt','w');
        end
                
        for c = 1:TotalSamplesSim
            fprintf(auxfile,'%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n',aux(c,:));
        end
        fclose(auxfile);
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Case 3 - Positive step at iq ref
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
    case 3
        disp('Simulation case 3: Rodriguez and Brogan, Pos step iq reference at t=0.5')
        Ttot = 1;
        idref = 0.0;
        
        EnableInverter = 1;    %short circuits inverter voltage
                                %inverts the igrid measurement direction
        
        %DDLPF_Notch = -1;       % -1=DDLPF , 1=Notch based
        Select_AMA = 0;         % AMA not selected, has precedence over DDLPF and Notch                
        zeta = 1;
        
        V_PosSeq_StepTime = 10000.5;
        V_PosSeq_InitialValue = 1;
        V_PosSeq_FinalValue = 0.8;
        
        V_NegSeq_StepTime = 10000.5;
        V_NegSeq_InitialValue = 0.0;
        V_NegSeq_FinalValue = 0.2;
            
        iqref_StepTime = 0.5;
        iqref_InitialLevel = 0.0;
        iqref_FinalLevel = -0.2;
                                        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        DDLPF_Notch = -1 ; % 1 for Brogan, -1 for Rodriguez
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        aux = simulado.get('viabcpqui');
        %assignin('base','GridVoltDrop',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV file first simulation
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text file step Iq - Rodriguez');
        % time vga vgb vgc vca vcb vcc ia ib ic p q u i
        auxfile = fopen('StepIq_lpf.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(auxfile,'%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n',aux(c,:));
        end
        fclose(auxfile);
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        DDLPF_Notch = +1 ; % 1 for Brogan, -1 for Rodriguez
        simulado = sim(nomemodelo, 'SimulationMode', 'accelerator');
        aux = simulado.get('viabcpqui');
        %assignin('base','GridVoltDrop',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV file first simulation
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text file step Iq - Brogan');
        % time vga vgb vgc vca vcb vcc ia ib ic p q u i
        auxfile = fopen('StepIq_notch.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(auxfile,'%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n',aux(c,:));
        end
        fclose(auxfile);
        
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% No case
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
    otherwise
        disp('No simulation case chosen')      
       
end







