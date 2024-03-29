clearvars;
close all;

Sn = 88;            % MW
Tgov1 = 0.1;        % s
Tgov2 = 0.4;
Tess = 0.05;        % s
H = 2.5;            % s
Fn = 50;            % Hz

Pessmax = 3.0;
StepMW = 6.0;       % MW

Kgt = [12 10  8  6  4  2 0];    % MW/Hz
Kess = [0  2  4  6  8 10 12];   % MW/Hz

KGT =  Kgt(1);
KESS = Kess(1);
open_system('PrimRes_sharing');

for i = 1:length(Kgt)
    KGT =  Kgt(i);
    KESS = Kess(i);
    
    simulacao = sim('PrimRes_sharing', 'SimulationMode', 'accelerator');
    aux = simulacao.get('raw_data');
    
    Nsamp = length(aux); 
    disp(strcat('Start saving text files: matstep_1_2MW_run_',int2str(i),'.csv'));
    
    fstep = fopen(strcat('matstep_6MW_run_',int2str(i),'.csv'),'w');
    for c = 1:Nsamp
        % time, F, deltaP, PfcrGT1, PfcrGT2, PfcrESS  
        fprintf(fstep,'%f, %f, %f, %f, %f, %f\n',aux(c,:));
    end
    fclose(fstep);
end






