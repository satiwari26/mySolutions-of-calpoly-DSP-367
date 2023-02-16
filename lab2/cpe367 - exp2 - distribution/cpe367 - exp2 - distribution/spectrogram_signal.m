function spectrogram_signal(wav_fname)

% usage: spectrogram_signal 'file_name.wav'

% load WAV file and generate spectrogram
% feel free to use this version of the spectrogram script to modify
%  as needed on projects - the other two have specific parameters 
%  that are needed for demos

% load WAV file
% wav_fname = 'signals/joy_fs_16khz.wav';
% wav_fname = 'signals/music.wav';
[x,fs] = audioread(wav_fname);

% set length of DFT and overlap 
Ndft = 2048;    % 2048  256 128
overlap = floor(0.9 * Ndft);

% win = hamming(Ndft);
win = rectwin(Ndft);


spectrogram(x,win,overlap,Ndft,fs,'yaxis')
title('Spectrogram')
