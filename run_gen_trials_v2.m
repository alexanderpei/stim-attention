%% Generates the trial files for the Psychopy trial handler

clear all
close all
clc

rng('default')
rng(1)

nBlock = 6;
nTrial = 32;
nSub   = 61;

pathOut = fullfile(cd, 'trialInfo');
if ~exist(pathOut)
    mkdir(pathOut)
end

%% Syllables for the left/right streams

sylPerm = perms([1 1 1 2 2 2 3 3 3]);
sylPerm = unique(sylPerm(:, 1:3),'rows');

% Remove three of a kind
iRemove = [];
for iPerm = 1:size(sylPerm, 1)
    tempPerm = sylPerm(iPerm, :);

    if length(unique(tempPerm)) == 1
        iRemove = [iRemove iPerm];
    end
end

sylPerm(iRemove, :) = [];

% Want to increase number of trials with 3 unique syllables and no 2
% sequential syllables
iBad = [];

for iPerm = 1:size(sylPerm, 1)

    tempPerm = sylPerm(iPerm, :);

    if tempPerm(1) == tempPerm(2) || tempPerm(2) == tempPerm(3)
        iBad = [iBad iPerm];
    end

end

iGood = setdiff(1:size(sylPerm, 1), iBad);
goodPerm = sylPerm(iGood, :);

sylPerm = [sylPerm; goodPerm; goodPerm; goodPerm];

%% Syllables for the center distractor

sylPermCenter = perms([1 1 1 2 2 2 3 3 3]);
sylPermCenter = unique(sylPermCenter(:, 1:4),'rows');

sylPermFlank  = perms([1 1 1 2 2 2 3 3 3]);
sylPermFlank  = unique(sylPermFlank(:, 1:3),'rows');

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
    'iGen', 'sylTarg', 'sylDist', 'sylCent', 'sylFlank', 'sylFlankFirst'};

trialInfo = cell(nTrial, 5);

for iSub = 1:nSub
    for iBlock = 1:nBlock

        binCond = dec2bin(0:2^5-1) - '0';
        binCond = binCond(randperm(size(binCond,1)), :);

        sylFlankOrder = [zeros(1, nTrial/2) ones(1, nTrial/2)];
        sylFlankOrder = sylFlankOrder(randperm(nTrial));

        % Add in extra stim trials for the StairCase
        if iSub == 61
            iTemp = find(binCond(:, 4) == 0);
            iTemp = iTemp(randperm(length(iTemp)));
            iTemp(1:length(iTemp)/2) = [];
            binCond(iTemp, 4) = 1;
        end

        for iTrial = 1:nTrial

            tempPerm = sylPerm(randperm(size(sylPerm, 1), 2), :);
            while sum(tempPerm(1, :) == tempPerm(2, :)) > 0
                tempPerm = sylPerm(randperm(size(sylPerm, 1), 2), :);
            end

            trialInfo{iTrial, 6} = polyval(tempPerm(1, :), 10);
            trialInfo{iTrial, 7} = polyval(tempPerm(2, :), 10);

            % Center stream
            iPermCenter = randperm(size(sylPermCenter, 1), 1);
            trialInfo{iTrial, 8} = polyval(sylPermCenter(iPermCenter, :), 10);

            % Left flank
            iPerm = randperm(size(sylPermFlank, 1), 1);
            trialInfo{iTrial, 9} = polyval(sylPermFlank(iPerm, :), 10);

            % Right flank
            trialInfo{iTrial, 10} = sylFlankOrder(iTrial);

            for iCond = 1:5

                trialInfo{iTrial, iCond} = binCond(iTrial, iCond);

            end

        end

        T = cell2table(trialInfo, 'VariableNames', names);

        if iSub == 61
            tempPathOut = fullfile(pathOut, 'StairCase');
        else
            tempPathOut = fullfile(pathOut, num2str(iSub));
        end

        if ~exist(tempPathOut)
            mkdir(tempPathOut)
        end

        writetable(T, fullfile(tempPathOut, [num2str(iBlock), '.csv']))

    end
end

