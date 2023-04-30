%clear;
%home;
cd 'C:\Users\daniemot\OneDrive - NTNU\Publications\2021_PosNegSequences\matlab\Basics' 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simplest RL between two voltages
% Grid voltage 
%   Positive sequence in series with negative sequence
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

nomemodelo = 'Basics_00';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simulation cases
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%caso = 1;   % Comparing the transducers
            % Harsh connection at time zero 
            % 0.1V positive sequence voltage
            % no negative sequence
            % zeta = 2^0.5/2 of all fitter in the notch based transducer

%caso = 2;   % Comparing quality of filters for the Notch Based transducer
            % Harsh connection at time zero 
            % 0.1V positive sequence voltage
            % no negative sequence
            % zeta = 2^0.5/2: zeta/1 zeta/5 zeta/10
            
caso = 3;   % Brogan vs Rodriguez
            % Harsh connection at time zero with Vpos = 1 
            % Step at Vpos from 1 to 0.8 at time 0.5
            % no negative sequence
            % zeta = 2^0.5 / 2
            PositiveDrop = 0; %if 1 then a negative step at the pos seq.,
                               %else NegativeStep at neg. seq. performed
            
            
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Common variables
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Sampling time, system frequency, switching frequency
Ts_control = 1/20000;   % for measuremetn control
Ts_PWM = 1/200000;      % for the PWM block
fsw = 2500;             % necessary for inner workuing of PWM block
fn = 50;                % easier to deal with 20ms period than 16,6667
% Voltage bases
Uanp = 1;
Uabp = Uanp * 3^0.5; 
Udc = Uanp * 3^0.5; 
% Load / impedance between voltage sources
X = 0.5;                % reactance in Ohm
L = X / 2 / pi / fn;    % inductance in H
R = X/20;               % resistance in Ohm
Z = (X^2 + R^2)^0.5;    % absolute value of the total impedance
Phi = atan (X/R);       % power angle of the impedance
Tau = L / R;            % time constant
% PI regulator
Ti = Tau;               % Main pole cancelling
Kp = 2;                 % A guess, values on the range of 5 make LPF based unstable
% Default choices fot the filters in the Notch based transducer
f_LPF_noise = 1000;
zeta = 2^0.5/2;
% Default choices fot references and setpoint
idref = 0;
iqref_StepTime = 10000.0;
iqref_InitialLevel = 0.0;
iqref_FinalLevel = 0.0;
%%%%%%%%
optionssim=simset('SrcWorkspace','base','DstWorkspace','base');

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
                                
        Rodriguez_Brogan = -1 ; % 1 for Brogan, -1 for Rodriguez
                                % actually irrelevant for this case
               
        V_PosSeq_StepTime = 10000;
        V_PosSeq_InitialValue = 0.1;
        V_PosSeq_FinalValue = 0.1;
        
        V_NegSeq_StepTime = 1000;
        V_NegSeq_InitialValue = 0;
        V_NegSeq_FinalValue = 0;
        
        
        aux = sim(nomemodelo, 'SimulationMode', 'accelerator');
        aux = aux.get('TransducerComp');
        assignin('base','TransducerComp',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV files
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text files');
        % Comparison file
        % time id-wtan iq-wtan id-wtmeas iq -wtmeas id-an iq-an id-meas iq-meas
        fComparison = fopen('Comparison.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%f, %f, %f, %f, %f, %f, %f, %f, %f\n',TransducerComp(c,:));
        end
        fclose(fComparison);
        disp('End of Script');
        return

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Caso 2 - Notch quality
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case 2
        disp('Simulation case: 02 - Quality of the notch filters - zeta 0.707 /1 /5 /10')
        Ttot = 0.260;
        
        EnableInverter = 0;    %short circuits inverter voltage
                                %inverts the igrid measurement direction
                                
        Rodriguez_Brogan = -1 ; % 1 for Brogan, -1 for Rodriguez
                                % actually irrelevant for this case
               
        V_PosSeq_StepTime = 10000;
        V_PosSeq_InitialValue = 0.1;
        V_PosSeq_FinalValue = 0.1;
        
        V_NegSeq_StepTime = 1000;
        V_NegSeq_InitialValue = 0;
        V_NegSeq_FinalValue = 0;
        
        zeta = 2^0.5/2;
        sim(nomemodelo, Ttot);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV file first simulation
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text file first simulation');
        % Comparison file
        % time id+an iq+an id+meas iq+meas id-wtan iq-wtan id-meas iq-meas 
        fComparison = fopen('Quality_01.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%f, %f, %f, %f, %f, %f, %f, %f, %f\n',QualityEval(c,:));
        end
        fclose(fComparison);
        
        zeta = 2^0.5/2/5;
        
        aux = sim(nomemodelo, 'SimulationMode', 'accelerator');
        aux = aux.get('QualityEval');
        assignin('base','QualityEval',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV file first simulation
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text file second simulation');
        % Comparison file
        % time id+an iq+an id+meas iq+meas id-wtan iq-wtan id-meas iq-meas 
        fComparison = fopen('Quality_05.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%f, %f, %f, %f, %f, %f, %f, %f, %f\n',QualityEval(c,:));
        end
        fclose(fComparison);
        
        zeta = 2^0.5/2/10;
        sim(nomemodelo, Ttot);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV file first simulation
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text file second simulation');
        % Comparison file
        % time id+an iq+an id+meas iq+meas id-wtan iq-wtan id-meas iq-meas 
        fComparison = fopen('Quality_10.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%f, %f, %f, %f, %f, %f, %f, %f, %f\n',QualityEval(c,:));
        end
        fclose(fComparison);
                
        disp('End of Script');
        return    

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% No case
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
    case 3
        disp('Simulation case 3: Rodriguez and Brogan, Pos step 1->0.8 at t=0.5')
        Ttot = 1;
        idref = 0.0;
        
        EnableInverter = 1;    %short circuits inverter voltage
                                %inverts the igrid measurement direction
        zeta = 2^0.5/2;
        
        if PositiveDrop == 1
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
        Rodriguez_Brogan = -1 ; % 1 for Brogan, -1 for Rodriguez
        aux = sim(nomemodelo, 'SimulationMode', 'accelerator');
        aux = aux.get('GridVoltDrop');
        assignin('base','GridVoltDrop',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV file first simulation
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text file grid voltage drop - Rodriguez');
        % time vga vgb vgc vca vcb vcc ia ib ic p q u i
        auxfile = fopen('GridVoltDrop_Rodriguez.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(auxfile,'%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n',GridVoltDrop(c,:));
        end
        fclose(auxfile);
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        Rodriguez_Brogan = 1 ; % 1 for Brogan, -1 for Rodriguez
        aux = sim(nomemodelo, 'SimulationMode', 'accelerator');
        aux = aux.get('GridVoltDrop');
        assignin('base','GridVoltDrop',aux);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Saving CSV file first simulation
        % This is hardcoded with the Simulink File
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        disp('Start saving text file grid voltage drop - Brogan');
        % time vga vgb vgc vca vcb vcc ia ib ic p q u i
        auxfile = fopen('GridVoltDrop_Brogan.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(auxfile,'%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n',GridVoltDrop(c,:));
        end
        fclose(auxfile);
        
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% No case
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
    otherwise
        disp('No simulation case chosen')
        Ttot = 0.5;
        
        EnableInverter = 1;    %short circuits inverter voltage
                                %inverts the igrid measurement direction
                                
        Rodriguez_Brogan = 1 ; % 1 for Brogan, -1 for Rodriguez
                                % actually irrelevant for this case
              
        V_PosSeq_StepTime = 10000;
        V_PosSeq_InitialValue = 1;
        V_PosSeq_FinalValue = 1;
        
        V_NegSeq_StepTime = 10000.25;
        V_NegSeq_InitialValue = 0.0;
        V_NegSeq_FinalValue = 0;
        
end







