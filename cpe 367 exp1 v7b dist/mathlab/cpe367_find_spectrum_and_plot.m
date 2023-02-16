function cpe367_find_spectrum_and_plot(xn,fs,td_plot_mode,fd_plot_mode, ...
            two_sided_flag,include_phase_flag,td_units,fd_units)
% Given a time-domain function, x[n], compute spectrum by DFT/FFT and plot
%   

% set length of DFT equal to length of signal
N = length(xn);

Nfft = N;
Nffto2 = floor(N/2);

% take FFT transform
%  Note if N is not a power of 2 then DFT is automatically used instead
Xf_og = fft(xn,Nfft);

% limit to only the positive frequencies
if two_sided_flag == false
    Xf = Xf_og(1:Nffto2);
    f = (0:length(Xf)-1)*(fs/2)/length(Xf);
else
    Xf = zeros(Nfft,1);
    f  = ones(Nfft,1);
    f_og = (0:Nfft-1)*(fs)/Nfft;
    
    % copy and shift
    for i = 0:Nfft-1
        iii = i + 1;
        
        if f_og(iii) > (fs/2)
            f(iii - Nffto2) = f_og(iii) - fs;
            Xf(iii - Nffto2) = Xf_og(iii);
        else
            f(iii + Nffto2) = f_og(iii);
            Xf(iii + Nffto2) = Xf_og(iii);
        end
    end
    
    f(1) = -fs/2;
    Xf(1) = 0;
    
end

% get magnitude of transform
Xf_mag = abs(Xf);
Xf_mag = Xf_mag / length(xn);

% get phase angle and convert to degrees
Xf_ph = angle(Xf);
Xf_ph = Xf_ph*180/pi;

% set angle to zero for tiny mags!
% Xf_ph_rounded = Xf_ph;
for i = 1:length(Xf_mag)
    if Xf_mag(i) > 0.00001
        Xf_ph_rounded(i) = round(Xf_ph(i),4);
    else
        Xf_ph_rounded(i) = 0;
    end
end

% generate vector with time-domain values
n = (0:length(xn)-1);
t = n * (1/fs);

% plot(f,20*log10(phh))
% plot(f,phh)

% set number of plots
if include_phase_flag == true
    num_plots = 3;
else
    num_plots = 2;
end

subplot(num_plots,1,1)
if td_plot_mode == 'stem'
    stem(t,xn)
else
    plot(t,xn)
end
grid on
title('Signal x[t]')
lstr = strcat('Time (',td_units,')');
xlabel(lstr)


subplot(num_plots,1,2)
if fd_plot_mode == 'stem'
    stem(f,Xf_mag)
else
    plot(f,Xf_mag)
end
grid on
title('Magnitude of X(f)')
lstr = strcat('Frequency (',fd_units,')');
xlabel(lstr)


if include_phase_flag == true
    subplot(num_plots,1,3)
    if fd_plot_mode == 'stem'
        stem(f,Xf_ph_rounded)
    else
        plot(f,Xf_ph_rounded)
    end
    grid on
    title('Phase of X(f)')
    lstr = strcat('Frequency (',fd_units,')');
    xlabel(lstr)
end

end

