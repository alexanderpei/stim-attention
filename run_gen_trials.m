%% Generates the trial files for the Psychopy trial handler

clear all
close all
clc

nBlock = 6;
nTrial = 32;
nSub   = 60;

pathOut = fullfile(cd, 'trialInfo');
if ~exist(pathOut)
    mkdir(pathOut)
end

%% Syllables for the left/right streams

sylPerm = perms([1 1 1 2 2 2 3 3 3]);
sylPerm = unique(sylPerm(:, 1:3),'rows');

% Want to increase number of trials with 3 unique syllables and no 2
% sequential syllables
iBad = [];

for iPerm = 1:size(sylPerm, 1)

    tempPerm = sylPerm(iPerm, :);

    if length(unique(tempPerm)) == 1
        iBad = [iBad iPerm];
    elseif tempPerm(1) == tempPerm(2) || tempPerm(2) == tempPerm(3)
        iBad = [iBad iPerm];
    end

end

iGood = setdiff(1:size(sylPerm, 1), iBad);
goodPerm = sylPerm(iGood, :);

sylPerm = [sylPerm; goodPerm; goodPerm; goodPerm];

%% Syllables for the center distractor

sylPermCenter = perms([1 1 1 2 2 2 3 3 3]);
sylPermCenter = unique(sylPermCenter(:, 1:4),'rows');

%%

% (1) iStimSide: 0 - left, 1 - right
% (2) iTargSide: 0 - left, 1 - right
% (3) iSideFrst: 0 - left, 1 - right
% (4) iStim:     0 - sham, 1 - true
% (5) iGen:      0 - male, 1 - female
% (6) sylTarg
% (7) sylDist
% (8) sylCent

names = {'iStimSide', 'iTargSide', 'iSideFirst', 'iStim', ...
    'iGen', 'sylTarg', 'sylDist', 'sylCent'};

trialInfo = cell(nTrial, 5);

for iSub = 1:nSub
    for iBlock = 1:nBlock
        for iTrial = 1:nTrial

            tempPerm = sylPerm(randperm(size(sylPerm, 1), 2), :);
            while sum(tempPerm(1, :) == tempPerm(2, :)) > 0
                tempPerm = sylPerm(randperm(size(sylPerm, 1), 2), :);
            end

            trialInfo{iTrial, 6} = polyval(tempPerm(1, :), 10);
            trialInfo{iTrial, 7} = polyval(tempPerm(2, :), 10);

            iPermCenter = randperm(size(sylPermCenter, 1), 1);

            trialInfo{iTrial, 8} = polyval(sylPermCenter(iPermCenter, :), 10);

        end

        for iCond = 1:5

            iRand = ones(1, nTrial);
            iRand(nTrial/2+1: nTrial) = 0;
            iRand = iRand(randperm(nTrial));

            for iTrial = 1:nTrial
                trialInfo{iTrial, iCond} = iRand(iTrial);
            end

        end

        T = cell2table(trialInfo, 'VariableNames', names);

        tempPathOut = fullfile(pathOut, num2str(iSub));
        if ~exist(tempPathOut)
            mkdir(tempPathOut)
        end

        writetable(T, fullfile(tempPathOut, [num2str(iBlock), '.csv']))

    end
end

