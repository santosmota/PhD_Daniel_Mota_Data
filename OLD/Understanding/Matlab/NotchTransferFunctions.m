clear;
home;
cd 'C:\Users\daniemot\OneDrive - NTNU\Publications\2021_PosNegSequences\matlab\Basics'

aux = 2^-0.5;

wn = 2 * pi * 100;

zetarange = [0.3:0.2:1.1];
Nz = 5;
Nw = 1001;

w = 2*pi*linspace(25,175,Nw);
mag = zeros(Nw,Nz);
phase = zeros(Nw,Nz);

figure(1)
for count = 1:Nz
    zeta = zetarange(count);
    sys = tf ([1 0 wn^2],[1 2*zeta*wn wn^2]);
    [magaux, phaseaux, woutaux] = bode(sys,w);
    mag(:,count) = squeeze(magaux);
    phase(:,count) = squeeze(phaseaux);
    hold on
end
hold off

t = linspace(0,0.03,1001);
degrau = zeros(1001,Nz);
figure(2)
for count = 1:Nz
    zeta = zetarange(count);
    sys = tf ([1 0 wn^2],[1 2*zeta*wn wn^2]);
    degrau(:,count) = step(sys,t);
    hold on
end
hold off

figure(3)
for zeta = zetarange
    sys = tf ([1 0 wn^2],[1 2*zeta*wn wn^2]);
    rlocus(sys);
    hold on
end
hold off

arquivo = fopen('QualityFreqResp.txt','w');
for linha = 1:Nw
    fprintf(arquivo,'%f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n',w(linha)/2/pi,mag(linha,:),phase(linha,:));
end
fclose(arquivo);

arquivo = fopen('QualitySteps.txt','w');
for linha = 1:Nw
    fprintf(arquivo,'%f, %f, %f, %f, %f, %f\n',t(linha),degrau(linha,:));
end
fclose(arquivo);

