% load WAV file and plot in time domain

clear

% load WAV file
wav_fname = 'reverb_hn.wav';
[xn,fs] = audioread(wav_fname);

% create a sequence of time-domain values
N = length(xn);
n = (0:N-1);
t = n * (1/fs);

td_plot_mode = 'line';

figure
if td_plot_mode == 'stem'
    stem(t,xn)
else
    plot(t,xn)
end
grid on
title('Reverb h[n]')
xlabel('Time (Sec)')
