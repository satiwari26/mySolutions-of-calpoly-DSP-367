function fresp_system_welch(in_fname,out_fname)

% find the frequency response by taking the ratio of the input & output noise 
%  power at each frequency. use the welch method of averaging with 50%
%  overlap. Take square root to display magnitude (rather than power)

% load input and output
% [y,fs] = audioread ('out_noise.wav');
% [x,fs] = audioread ('in_noise.wav');
[y,fs] = audioread (out_fname);
[x,fs] = audioread (in_fname);

N = length(x) / 200;
N = floor(N);

% duration of signal used for each DFT transform
segment_length = N;

% use a hamming window with each segment
segment_window = hamming(segment_length);
% segment_window = rectwin(segment_length);

% 50% overlap
overlap = N/2;

% length of each DFT
nfft = N;

[pxx,f] = pwelch(x,segment_window,overlap,nfft,fs,'power');
[pyy,f] = pwelch(y,segment_window,overlap,nfft,fs,'power');

% divide output power by input power
%  dividing sequences element by element
phh = pyy ./ pxx;

% display magnitude instead of power
phh = sqrt(phh);

% plot(f,20*log10(pxx))
plot(f,phh)

title('My Digital Filter')
grid on
grid minor
xlabel('Frequency (Hz)')
ylabel('Magnitude of Frequency Response')

