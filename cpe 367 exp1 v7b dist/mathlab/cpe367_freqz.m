% find the frequency response for a system using freqz()

b = [ 1/3, 1/3, 1/3 ];
a = 1;

N = 512;
fs = 16000;

[h,f] = freqz(b,a,N,fs);

mag = abs(h);
ph = angle(h);

subplot(2,1,1)
plot(f,mag)
title('Magnitude of Frequency Response')
xlabel('Frequency (Hz)')

subplot(2,1,2)
plot(f,ph*180/pi)
title('Phase of Frequency Response')
xlabel('Frequency (Hz)')

