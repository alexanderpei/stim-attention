%%

clear
close all

try
    playrec('reset')
catch
end

iSub = 1;
% Generate the sound stimuli
allSounds = fn_gen_sounds(iSub);
%% Connect to RME

fprintf('Initializing connection to sound card...\n')
Devices=playrec('getDevices');
if isempty(Devices)
    error(sprintf('There are no devices available using the selected host APIs.\nPlease make sure the RME is powered on!')); %#ok<SPERR>
else
    i=1;
    while ~strcmp(Devices(i).name,'ASIO Fireface USB') && i <= length(Devices)
        i=i+1;
    end
end
fs = 48000;%Devic1es(i).defaultSampleRate;
playDev = Devices(i).deviceID;
playrec('init',fs,playDev,-1,14,-1);
fprintf('Success! Connected to %s.\n', Devices(i).name);

%% instantiate the librar1y
disp('Loading the library...');
lib = lsl_loadlib();

% resolve a stream...
disp('Resolving marker stream...');
result = {};
while isempty(result)
    result = lsl_resolve_byprop(lib,'source_id','peiPCtrial'); 
end

% create a new inlet
disp('Opening an inlet...');
inlet = lsl_inlet(result{1});

disp('Now receiving data...');
while true
    % get data from the inlet
    [mrk_,ts] = inlet.pull_sample();

    % What was just pulled?
    mrk_ = mrk_{1};
    
    if contains(mrk_, 'Block')
        disp(mrk_)
        temp = strsplit(mrk_, ':');
        blockNum = str2double(temp{2});
    elseif contains(mrk_, 'Trial')
        disp(mrk_)
        temp = strsplit(mrk_, ':');
        trialNum = str2double(temp{2});
    elseif contains(mrk_, 'StartSound')
        disp(mrk_)
        stimchanList=[1,2,14];
        stim = allSounds{blockNum, trialNum};
        trig = trignum2scalar(9)*ones(size(stim,1),1);
        allStim = [stim,trig];
        
        playrec('play',allStim,stimchanList);

    end
    
end
