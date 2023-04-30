clear vars;
%home;
cd 'C:\Users\daniemot\OneDrive - NTNU\Publications\2021_PosNegSequences\matlab\Basics' 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simplest RL between two voltages
% Grid voltage 
%   Positive sequence in series with negative sequence
% 
% 2021-06-15 Made for estimating frequency responses in the abc
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

nomemodelo = 'PostSubmission_FreqResp_00';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simulation cases
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
caso = 1; %1 nao funciona, copie o codigo de salvar na linha de comando                              
            
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Common variables
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Ttot = 0.04;%10.0;
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

% Impulse for FFT calculations
ImpulseTime = 1 / (10*fn);
ImpulseAmp = 1;

% Impulse for FFT calculations
Pos_1_Neg_minus1 = 1;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Simulation cases
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
switch caso
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Caso 1 - Transducer comparison
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case 1
        disp('Simulation case: 01 - Impulse - zeta 1')
        Ttot = 1;
        
        simulacao = sim(nomemodelo, 'SimulationMode', 'accelerator');
        %simulacao = sim(nomemodelo, 'SimulationMode');
        aux = simulacao.get('PostSubmFreqResp');

        
        %aux = PostSubmFreqResp;
        TotalSamplesSim = round(Ttot / Ts_control + 1);
        
        disp('Start saving text files:');
        fComparison = fopen('PostSubmFreqResp.txt','w');
        for c = 1:TotalSamplesSim
            fprintf(fComparison,'%e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e, %e\n',aux(c,:));
        end
        fclose(fComparison);
                
        
        return


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% No case
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
    otherwise
        disp('No simulation case chosen')      
       
end







