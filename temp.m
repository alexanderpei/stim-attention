%%

close all
clear all
clc

addpath(fullfile(cd, 'sounds', 'HRTFs'))

%% Parameters

allSyl = {'ba','da','ga'};
allGen = {'Male1','Male2','Female1','Female2','Neutral'};%1-5
lenSti = 350;%expected length of stimulus,exclude rise/fall (ms)
lenSti_Neut = 350;%slightly shorter neutral stimuli (ms)
time2rise = 0.05;%(s)
fs = 48000;%read from data

%% Construct variables for main loop

tempRise = sin(2*pi*1/(4*time2rise)*(0:1/fs:time2rise)).^2;
filtRise = [ones(1,round(lenSti/1000*fs)) tempRise(end-1:-1:1)];
filtRise_Neut = [ones(1,round(lenSti_Neut/1000*fs)) tempRise(end-1:-1:1)];

lenTot = length(filtRise);%total length
lenTot_Neut = length(filtRise_Neut);%total length

%% Main loop
% Extract all sounds
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

%%

hrtf.loc(1).data = load('HRTF_L15.mat');
hrtf.loc(3).data = load('HRTF_N00.mat');
hrtf.loc(2).data = load('HRTF_R15.mat');

%% Play all sounds

% for idxGen = 1:length(allGen)
%     for idxSyl = 1:length(allSyl)
%         temp1 = conv(allSound.spk(idxGen).syl(idxSyl).data,hrtf.loc(1).data.hrtf_left);
%         temp2 = conv(allSound.spk(idxGen).syl(idxSyl).data,hrtf.loc(1).data.hrtf_right);
%         sound([temp1, temp2],fs);
%         %pause(0.1)
%     end
% end

%% test make stream

delay = zeros(0.18*fs,2);
delay_start = zeros(0.3*fs,2);
iti = zeros(0.4*fs,2);
% 
% 
% stream1 = [sound1; iti; sound1; iti; sound1; delay];
% stream2 = [delay; sound2; iti; sound2; iti; sound2];
% stream3 = [delay; iti; sound3; iti; sound3; zeros(size(sound3))];
% 
% sound([stream1 + stream2 + stream3],fs)

%% Make all stim

p = perms([1 1 1 2 2 2 3 3 3]);
p = unique(p(:,1:3),'rows');

idxBad = [];
for idxRow = 1:size(p, 1)
   if sum(p(idxRow, :) == p(idxRow, 1)) == size(p, 2)
       idxBad = [idxRow idxBad];
   end
end

p(idxBad, :) = [];

neup = perms([1 1 1 2 2 2 3 3 3]);
neup = unique(neup(:,1:4),'rows');

% fileName, attention type, target side, target gender, target syl,
% distractor syl, neutral syl, text display, stim type, sham, cond_num
trialInf = cell(32,11);

for idxSub = 9:30
    disp(idxSub)
    for idxBlock = 1:6
        trialInf = cell(32,10);
        
        count = 0;
        cond = 100;
        for stimSide = {'Left','Right'}
            for shamTrue = {'True','Sham'}
                for targOrd = {'First','Second'}
                    for targSide = {'Left','Right'}
                        for talkGen = {'Male','Female'}
                            
                            cond = cond + 1;
                            
                            for idxP = randperm(length(p), 1)
                                count = count + 1;
                                
                                % Store the trial info
                                trialInf{count,11} = cond;
                                
                                % Changed to speaker always female
                                spk1 = 4;
                                spk2 = 4;

                                targGen = talkGen;
                                textGen = talkGen;  
                                
                                switch targSide
                                    case 'Left'
                                        loc1 = 2;
                                        loc2 = 1;
                                    case 'Right'
                                        loc1 = 1;
                                        loc2 = 2;
                                end
                                
                                targLoc = targSide;
                                textLoc = targSide;
                                
                                % fill in trial info
                                trialInf{count,2} = targOrd;
                                trialInf{count,3} = targLoc;
                                trialInf{count,4} = targGen;
                                
                                % right vs left, true vs sham
                                trialInf{count,9} = stimSide;
                                trialInf{count,10} = shamTrue;
                                
                                % First stream target
                                syls = p(idxP,:);
                                trialInf{count,5} = polyval(syls,10); % store syls
                                sounds = cell(1,3);
                                
                                for i = 1:3
                                    
                                    temp1 = conv(allSound.spk(spk1).syl(syls(i)).data,hrtf.loc(loc1).data.hrtf_left,'same');
                                    temp2 = conv(allSound.spk(spk1).syl(syls(i)).data,hrtf.loc(loc1).data.hrtf_right,'same');
                                    
                                    sounds{i} = [temp1, temp2];
                                    
                                end
                                
                                switch targOrd
                                    case 1
                                        stream1 = [delay_start; delay; sounds{1}; iti; sounds{2}; iti; sounds{3}];
                                    case 2
                                        stream1 = [delay_start; sounds{1}; iti; sounds{2}; iti; sounds{3}];
                                end
                                
                                % Second stream distractor
                                syls = p(randi(length(p),[1 1]),:);
                                trialInf{count,6} = polyval(syls,10);
                                
                                sounds = cell(1,3);
                                
                                for i = 1:3
                                    
                                    temp1 = conv(allSound.spk(spk2).syl(syls(i)).data,hrtf.loc(loc2).data.hrtf_left,'same');
                                    temp2 = conv(allSound.spk(spk2).syl(syls(i)).data,hrtf.loc(loc2).data.hrtf_right,'same');
                                    
                                    sounds{i} = [temp1, temp2];
                                    
                                end
                                
                                switch targOrd
                                    case 1
                                        stream2 = [delay_start; sounds{1}; iti; sounds{2}; iti; sounds{3}];
                                    case 2
                                        stream2 = [delay_start; delay; sounds{1}; iti; sounds{2}; iti; sounds{3}];
                                end
                                                                
                                % Third stream
                                syls = neup(randi(length(neup),[1 1]),:);
                                trialInf{count,7} = polyval(syls,10);
                                sounds = cell(1,length(syls));
                                
                                for i = 1:length(syls)
                                    
                                    temp1 = conv(allSound.spk(5).syl(syls(i)).data,hrtf.loc(3).data.hrtf_left,'same');
                                    temp2 = conv(allSound.spk(5).syl(syls(i)).data,hrtf.loc(3).data.hrtf_right,'same');
                                    
                                    sounds{i} = [temp1, temp2];
                                    
                                end
                                
                                stream3 = [sounds{1}; iti; sounds{2}; iti; sounds{3}; iti; sounds{4};];
                                
                                %sound([stream1 + stream2 + stream3],fs)
                                
                                pathOut = 'C:\Users\Alex\Documents\MATLAB\cmu\stim\exp\sounds';
                                fname = ['targ_' targLoc '_' targGen '_' num2str(targOrd) '_' num2str(idxP) '_' num2str(polyval(syls,10)) '.wav'];
                                
                                % Pad zeros
                                zeros_pad = size(stream3, 1) - size(stream1, 1);
                                stream1 = [stream1; zeros(zeros_pad, 2)];
      
                                zeros_pad = size(stream3, 1) - size(stream2, 1);
                                stream2 = [stream2; zeros(zeros_pad, 2)];
                                
                                stream = stream1 + stream2 + stream3;
                                % soundsc(stream, fs)
                                audiowrite(fullfile(pathOut,fname),stream, fs)
                                
                                trialInf{count,1} = fullfile('sounds',fname);
                                trialInf{count,8} = textLoc;
                                
                            end
                        end
                    end
                end
            end
        end
        %trialInf = trialInf(randperm(length(trialInf)),:);
        T = cell2table(trialInf,'VariableNames',{'fileName', 'attType', 'targSide', 'targGen', 'targSyl', 'distSyl', 'neuSyl','textDisp','stimType','sham','cond'});
        T = T(randperm(size(T,1)), :);

        if ~isfolder(fullfile(pathOut,'..','trialTypes',num2str(idxSub)))
            mkdir(fullfile(pathOut,'..','trialTypes',num2str(idxSub)))
        end
        
        writetable(T,fullfile(pathOut,'..','trialTypes',num2str(idxSub),['trialTypes_' num2str(idxBlock) '.csv']))
        
    end
end

% Do practice trial 50 trials

T = cell2table(trialInf(randperm(length(trialInf),30),:),'VariableNames',{'fileName', 'attType', 'targSide', 'targGen', 'targSyl', 'distSyl', 'neuSyl','textDisp','stimType','sham','cond'});
writetable(T,fullfile(pathOut,'..','trialTypes_practice.csv'))

% %%
% 
% v{1} = [1 1 1 2 3];
% v{2} = [1 1 2 2 3];
% v{3} = [1 1 2 3 3];
% v{4} = [1 2 2 3 3];
% 
% v = [perms(v{1}); perms(v{2}); perms(v{3}); perms(v{4})];
% 
% % find rows where there are no same syllables repeated
% idx = diff(v,[],2) == 0; % diff will equal zero if there are repeated syllables
% idx = sum(idx,2) == 0; % find where there are no zeros
% 
% v = v(idx,:);
% 
% %%
% 




%% Convolve sounds

% for idxGen = 1:length(allGen)
%     for idxSyl = 1:length(allSyl)
%         for idxConv = [1 5]
%             temp1 = conv(allSound.spk(idxGen).syl(idxSyl).data,hrtf.loc(idxConv).data.hrtf_left);
%             temp2 = conv(allSound.spk(idxGen).syl(idxSyl).data,hrtf.loc(idxConv).data.hrtf_right);
%             switch idxConv
%                 case 1
%                     loc = 'L90';
%                 case 5
%                     loc = 'R90';
%             end
%             nameOut = fullfile(cd,'sounds',[allGen{idxGen} '_' allSyl{idxSyl} '_' loc '.wav']);
%             audiowrite(nameOut,[temp1, temp2],fs)
%         end
%     end
% end
