function allSounds = fn_gen_sounds_v2(iSub)

addpath(fullfile(cd, 'sounds', 'HRTFs'))
nBlock = 6;
nTrial = 32;

allSounds = cell(nBlock, nTrial);

%% Process Sounds

allSyl = {'ba','da','ga'};
allGen = {'Male1','Male2','Female1','Female2','Neutral'};%1-5
lenSti = 350;%expected length of stimulus,exclude rise/fall (ms)
lenSti_Neut = 350;%slightly shorter neutral stimuli (ms)
time2rise = 0.05;%(s)
fs = 48000;%read from data

tempRise = sin(2*pi*1/(4*time2rise)*(0:1/fs:time2rise)).^2;
filtRise = [ones(1,round(lenSti/1000*fs)) tempRise(end-1:-1:1)];
filtRise_Neut = [ones(1,round(lenSti_Neut/1000*fs)) tempRise(end-1:-1:1)];

lenTot = length(filtRise);%total length
lenTot_Neut = length(filtRise_Neut);%total length

for idxSyl = 1:length(allSyl)
    for idxGen = 1:length(allGen)
        fileName = fullfile('sounds', 'Sounds_Final', [allSyl{idxSyl} '_' allGen{idxGen} '.wav']);
        [tempSound,fs] = audioread(fileName);

        if idxGen ~= 5
            tempData = zeros(round(fs*(time2rise+lenSti/1000)),1);
            tempData(1:min(lenTot,length(tempSound))) = tempSound(1:min(lenTot,length(tempSound)));
            allSound.spk(idxGen).syl(idxSyl).data = tempData.*filtRise';
        else
            tempData = zeros(round(fs*(time2rise+lenSti_Neut/1000)),1);
            tempData(1:min(lenTot_Neut,length(tempSound))) = tempSound(1:min(lenTot_Neut,length(tempSound)));
            allSound.spk(idxGen).syl(idxSyl).data = tempData.*filtRise_Neut';
        end
        power(idxSyl,idxGen) = rms(allSound.spk(idxGen).syl(idxSyl).data);
    end
end
minPower = min(min(power));
for idxGen = 1:length(allGen)%normalize RMS
    for idxSyl = 1:length(allSyl)
        allSound.spk(idxGen).syl(idxSyl).data = allSound.spk(idxGen).syl(idxSyl).data*minPower/power(idxSyl,idxGen);
    end
end

hrtf.loc(1).data = load('HRTF_L90.mat');
hrtf.loc(3).data = load('HRTF_N00.mat');
hrtf.loc(2).data = load('HRTF_R90.mat');
hrtf.loc(4).data = load('HRTF_L30.mat');
hrtf.loc(5).data = load('HRTF_R30.mat');

%% Generate the streams

for iBlock = 1:nBlock

    pathIn = fullfile(cd, 'trialInfo', num2str(iSub), [num2str(iBlock) '.csv']);
    trialInfo = readtable(pathIn);

    % Delays
    delayLead = zeros(0.18*fs, 2);
    delayLag  = zeros(0.48*fs, 2);
    ISI       = zeros(0.40*fs, 2);

    for iTrial = 1:nTrial

        iTargSide = trialInfo.iTargSide(iTrial);
        iSideFrst = trialInfo.iSideFirst(iTrial);
        iSpeaker = 4;

        % Make the target
        switch iTargSide
            case 0
                iTarg = 1;
                iDist = 2;
            case 1
                iTarg = 2;
                iDist = 1;
        end

        LTargHRTF = hrtf.loc(iTarg).data.hrtf_left;
        RTargHRTF = hrtf.loc(iTarg).data.hrtf_right;
        LDistHRTF = hrtf.loc(iDist).data.hrtf_left;
        RDistHRTF = hrtf.loc(iDist).data.hrtf_right;
        LCentHRTF = hrtf.loc(3).data.hrtf_left;
        RCentHRTF = hrtf.loc(3).data.hrtf_right;
        

        sylTarg = cell(1, 3);
        sylDist = cell(1, 3);
        % Convolve the syllables for target and distractor stream
        sylListTarg = num2str(trialInfo.sylTarg(iTrial));
        sylListDist = num2str(trialInfo.sylDist(iTrial));
        for iSyl = 1:3

            iTempTarg = str2double(sylListTarg(iSyl));
            iTempDist = str2double(sylListDist(iSyl));

            sylTargL = conv(allSound.spk(iSpeaker).syl(iTempTarg).data, LTargHRTF, 'same');
            sylTargR = conv(allSound.spk(iSpeaker).syl(iTempTarg).data, RTargHRTF, 'same');

            sylDistL = conv(allSound.spk(iSpeaker).syl(iTempDist).data, LDistHRTF, 'same');
            sylDistR = conv(allSound.spk(iSpeaker).syl(iTempDist).data, RDistHRTF, 'same');

            sylTarg{1, iSyl} = [sylTargR, sylTargL];
            sylDist{1, iSyl} = [sylDistR, sylDistL];

        end

        % Center stream
        sylCent = cell(1, 4);
        sylListCent = num2str(trialInfo.sylCent(iTrial));
        for iSyl = 1:4

            iTempCent = str2double(sylListCent(iSyl));

            sylCentL = conv(allSound.spk(5).syl(iTempCent).data, LCentHRTF, 'same');
            sylCentR = conv(allSound.spk(5).syl(iTempCent).data, RCentHRTF, 'same');

            sylCent{1, iSyl} = [sylCentR, sylCentL];

        end
        
        % Flanking center
        sylFlank = cell(1, 3);
        sylListFlank = num2str(trialInfo.sylFlank(iTrial));

        if trialInfo.sylFlankFirst == 0
            iLoc = [4 5 4];
        else
            iLoc = [5 4 5];
        end
        
        for iSyl = 1:3

            sylFlankL = conv(allSound.spk(1).syl(iTempCent).data, hrtf.loc(iLoc(iSyl)).data.hrtf_left, 'same');
            sylFlankR = conv(allSound.spk(1).syl(iTempCent).data, hrtf.loc(iLoc(iSyl)).data.hrtf_right, 'same');

            sylFlank{1, iSyl} = [sylFlankR, sylFlankL];
        
        end

        % Lead Stream: [0.18, 0.35, 0.4,  0.35, 0.4,  0.35]
        % Lag  Stream: [0.48, 0.35, 0.4,  0.35, 0.4,  0.35];
        % Cent Stream: [0.35, 0.4,  0.35, 0.4,  0.35, 0.4,  0.35];
        % Flnk Stream: [0.4,  0.35, 0.4,  0.35, 0.4,  0.35, 0.4];

        % Construct stream
        if iSideFrst == iTargSide
            leadStream = [delayLead; sylTarg{1}; ISI; sylTarg{2}; ISI; sylTarg{3}];
            lagStream  = [delayLag;  sylDist{1}; ISI; sylDist{2}; ISI; sylDist{3}];
        else
            leadStream = [delayLead; sylDist{1}; ISI; sylDist{2}; ISI; sylDist{3}];
            lagStream  = [delayLag;  sylTarg{1}; ISI; sylTarg{2}; ISI; sylTarg{3}];
        end

        % Center stream
        centStream = [sylCent{1}; ISI; sylCent{2}; ISI; sylCent{3}; ISI; sylCent{4}];

        % Flank Stream
        flankStream = [ISI; sylFlank{1}; ISI; sylFlank{2}; ISI; sylFlank{3}; zeros(size(sylCent{4}))];

        % Add streams together by padding zeros
        nPadLead = size(centStream, 1) - size(leadStream, 1);
        nPadLag  = size(centStream, 1) - size(lagStream, 1);

        leadStream = [leadStream; zeros(nPadLead, 2)];
        lagStream  = [lagStream; zeros(nPadLag, 2)];

        allStream = leadStream + lagStream + centStream + flankStream;
        
        soundsc(allStream, fs)
        keyboard

        allSounds{iBlock, iTrial} = allStream;

    end
end