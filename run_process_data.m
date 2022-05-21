%%

clear all
close all

pathData = fullfile(cd, 'data_behave_merge');
dirData  = dir(fullfile(pathData, 'sub_2.mat'));

nSub = length(dirData);
nSide = 2;
nStimSide = 2;
nTarg = 2;
nSideFirst = 2;

nCond = nSide*nStimSide*nTarg*nSideFirst;
nBlock = 6;
nTrialBlock = 32;
nTrialCond = nBlock*nTrialBlock/nCond;

% 2, 1 for total trial accuracy, 2 for individual syllable accuracy
allCondData    = zeros(nSub, nCond, nTrialCond, 2);

% ---- Cond info ----
% Cond 1:  Stim Left,  Targ Left,  Left 1st,  Sham
% Cond 2:  Stim Left,  Targ Left,  Left 1st,  True
% Cond 3:  Stim Left,  Targ Left,  Right 1st, Sham
% Cond 4:  Stim Left,  Targ Left,  Right 1st, True
% Cond 5:  Stim Left,  Targ Right, Left 1st,  Sham
% Cond 6:  Stim Left,  Targ Right, Left 1st,  True
% Cond 7:  Stim Left,  Targ Right, Right 1st, Sham
% Cond 8:  Stim Left,  Targ Right, Right 1st, True
% Cond 9:  Stim Right, Targ Left,  Left 1st,  Sham
% Cond 10: Stim Right, Targ Left,  Left 1st,  True
% Cond 11: Stim Right, Targ Left,  Right 1st, Sham
% Cond 12: Stim Right, Targ Left,  Right 1st, True
% Cond 13: Stim Right, Targ Right, Left 1st,  Sham
% Cond 14: Stim Right, Targ Right, Left 1st,  True
% Cond 15: Stim Right, Targ Right, Right 1st, Sham
% Cond 16: Stim Right, Targ Right, Right 1st, True

% ---- Cond of interest ----

% Stim Left, Targ Left, Sham
cond{1} = [1 3];
% Stim Left, Targ Left, True
cond{2} = [2 4];
% Stim Left, Targ Right, Sham
cond{3} = [5 6];
% Stim Left, Targ Right, True
cond{4} = [6 8];
% Stim Right, Targ Left, Sham
cond{5} = [9 11];
% Stim Right, Targ Left, True
cond{6} = [10 12];
% Stim Right, Targ Right, Sham
cond{7} = [13 15];
% Stim Right, Targ Right, True
cond{8} = [14 16];

for iSub = 1:length(dirData)

    load(fullfile(pathData, dirData(iSub).name))
    condData = zeros(nCond, nTrialCond, 2);
    condDataCount = zeros(nCond, 1);

    for iRow = 2:size(allCSV, 1)

        trialInfo = cell2mat(allCSV(iRow, 1:4));
        iCond = bin2dec(num2str(trialInfo))+1;
        condDataCount(iCond) = condDataCount(iCond) + 1;

        response = allCSV{iRow, 37};
        idx = (response == '1') | (response == '2') | (response == '3');

        response = response(idx);
        targ = num2str(allCSV{iRow, 6});

        if strcmp(response, targ)
            condData(iCond, condDataCount(iCond), 1) = 1;
        end

        if length(response) == 3
            condData(iCond, condDataCount(iCond), 2) = sum(response == targ) / 3;
        end

    end

    allCondData(iSub, :, :, :) = condData;

end

%% Stim Ipsi to Attention vs. Stim Contra to Attention

iStimIpsiTrue = cell2mat(cond([2 8]));
iStimContTrue = cell2mat(cond([4 6]));
iStimIpsiSham = cell2mat(cond([1 7]));
iStimContSham = cell2mat(cond([3 5]));

for iAcc = 1:2

    accStimIpsiTrue = sum(mean(condData(iStimIpsiTrue, :, iAcc))) / nTrialCond;
    accStimContTrue = sum(mean(condData(iStimContTrue, :, iAcc))) / nTrialCond;
    accStimIpsiSham = sum(mean(condData(iStimIpsiSham, :, iAcc))) / nTrialCond;
    accStimContSham = sum(mean(condData(iStimContSham, :, iAcc))) / nTrialCond;

end
