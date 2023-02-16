function spectrum_signal_dft(wav_fname,varargin)

% use a DFT to find the spectrum of the signal in a WAV file
% usage: spectrum_signal_dft 'file.wav' [optional arguments]
% first argument: path to the WAV file (quotes recommended)
% optional arg: 'two_sided', for a two-sided spectrum, default is one-sided
% optional arg: 'td_stem_plot', for stems in time-domain plot
% optional arg: 'fd_stem_plot', for stems in frequency-domain plot
% optional arg: 'skip_phase', to skip phase plot

% set defaults
two_sided = false;
td_plot_mode = 'line';   % stem line
fd_plot_mode = 'line';
include_phase = true;

% override defaults based on command line args
if isempty(varargin) == false
    for a = 1:length(varargin)
        
        % one or two sided spectrum
        if strcmp(varargin{a},'two_sided') == true
            two_sided = true;
        end

        % stem vs line plot
        if strcmp(varargin{a},'td_stem_plot') == true
            td_plot_mode = 'stem';
        end

        % stem vs line plot
        if strcmp(varargin{a},'fd_stem_plot') == true
            fd_plot_mode = 'stem';
        end

        % skip_phase
        if strcmp(varargin{a},'skip_phase') == true
            include_phase = false;
        end

    end
end


% load WAV file
[x,fs] = audioread(wav_fname);

% plot spectrum
cpe367_find_spectrum_and_plot(x,fs,td_plot_mode,fd_plot_mode, ...
    two_sided,include_phase,'Sec','Hz');

return
