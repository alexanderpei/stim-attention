%% Make the file for tACS stimulation to be read by Soterix Device

clc
clear
close all

steps = 100:100:3000;

% Waveform Parameters

for step = steps

    freq      = 10;       % Frequency in Hz
    dur       = 10;       % Duration in seconds
    dt        = 1/1000;   % Sampling period
    t         = 0:dt:dur; % Time vector
    rampOnset = 2;        % Onset of the ramp
    rampDur   = 1;        % Duration of the ramp
    stimDur   = 2.8;      % Duration of stimulation

    elecR = {'CP2', 'P4', 'Pz', 'PO4', 'P2'};
    elecL = {'CP1', 'P3', 'Pz', 'PO3', 'P1'};
    mA   = [-0.6, -0.225, -0.075, -0.6, 1.5]/1e6; % peak-to-peak
    mA = mA.*step;

    pathOut = fullfile(cd, 'waveforms_steps', num2str(step));
    if ~exist(pathOut)
        mkdir(pathOut)
    end

    %% Create the base waveforms for sham and true

    waveTrue = zeros(1, length(t));
    waveSham = zeros(1, length(t));

    % True stimulation
    ramp = 0:dt:rampDur-dt;

    iRampUpStart = rampOnset/dt + 1;
    iRampUpEnd   = iRampUpStart + rampDur/dt - 1;

    iStimStart = iRampUpEnd + 1;
    iStimEnd   = iStimStart + stimDur/dt - 1;

    iRampDownStart = iStimEnd + 1;
    iRampDownEnd   = iRampDownStart + rampDur/dt - 1;

    waveTrue(iRampUpStart:iRampUpEnd) = ramp;
    waveTrue(iStimStart:iStimEnd) = 1;
    waveTrue(iRampDownStart:iRampDownEnd) = fliplr(ramp);

    % Sham stimulation
    ramp = 0:dt:rampDur/2-dt;
    ramp = [ramp fliplr(ramp)];

    waveSham(iRampUpStart:iRampUpEnd) = ramp;
    waveSham(iRampDownStart:iRampDownEnd) = ramp;

    % Multiply by sine wave
    waveSham = waveSham.*sin(2*pi*freq*t);
    waveTrue = waveTrue.*sin(2*pi*freq*t);

    % Plot
    figure
    subplot(1,2,1)
    plot(waveTrue)
    subplot(1,2,2)
    plot(waveSham)

    %% Make the files and waveforms at the electrodes

    % iSide - Left/Right (0 - Left, 1 - Right);
    % iElec - Which electrode

    figure
    hold on

    for iSide = [0 1]

        switch iSide
            case 0
                tempElec = elecL;
            case 1
                tempElec = elecR;
        end

        for iElec = 1:length(tempElec)

            tempWaveTrue = waveTrue.*mA(iElec)/2';
            tempWaveSham = waveSham.*mA(iElec)/2';

            dlmwrite(fullfile(pathOut, [tempElec{iElec} '_true.txt']), tempWaveTrue, 'delimiter', '\n')
            dlmwrite(fullfile(pathOut, [tempElec{iElec} '_sham.txt']), tempWaveSham, 'delimiter', '\n')

            % Plot test
            if iSide == 1
                plot(tempWaveTrue)
            end

        end

    end

end
