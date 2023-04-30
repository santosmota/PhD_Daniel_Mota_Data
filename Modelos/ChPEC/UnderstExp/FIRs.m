clear variable;
home;
cd 'C:\Users\daniemot\OneDrive - NTNU\Publications\2021_PosNegSequences\matlab\Basics'

Ts = 1/2000;

fn = 50;
Tn = 1/fn;

n = 10;
%wnotch = 4*Ts/Tn; % 1 is equal to Nyquist frequency
wnotch = 200/1000;
b = fir1(n,[0.9*wnotch 1.1*wnotch],'bandpass');
%b = fir1(n,wnotch,'low');
%simulado = sim('FiltrosDigitais', 'SimulationMode', 'accelerator');

%for aux = length(b):-1:2
%    disp(aux)
%end

%N = length(b);
%ent = zeros(1,N);
%ent(N) = 1;
%y = dot(b, ent);
