%% Merge the output of the Psychopy files

clear all
close all

pathData    = fullfile(cd, 'data_behave');
pathDataOut = fullfile(cd, 'data_behave_merge');
if ~isfolder(pathDataOut)
    mkdir(pathDataOut)
end
dirData  = dir(pathData);
dirData  = dirData(3:end);

nSub = length(dirData);
nTrial = 32;
nColKeep = 1:52;

for iSub = 1:nSub

    tempDir  = dir(fullfile(pathData, dirData(iSub).name, '*.csv'));

    % Merge and loop over CSV files
    allCSV = {};

    for iFile = 1:length(tempDir)
        
        tempCell = readcell(fullfile(tempDir(iFile).folder, tempDir(iFile).name));

        if iFile == 1
            allCSV = [allCSV; tempCell(1, nColKeep)];
        end

        iBlockStart = 25; % Index of the 'Space' for the block start;
        
        % Get idx of block starts
        iAllBlockStart = [];
        for iRow = 1:size(tempCell, 1)

            if strcmp(tempCell{iRow, iBlockStart}, 'space')
                iAllBlockStart = [iAllBlockStart iRow];
            end

        end

        iAllBlockStart = [iAllBlockStart size(tempCell, 1)];

        iGood = diff(iAllBlockStart) >= nTrial;
        iGood = iAllBlockStart(iGood);

        for idx = iGood
            allCSV = [allCSV;  tempCell(idx:idx+nTrial-1, nColKeep)];
        end

    end

    save(fullfile(pathDataOut, ['sub_' num2str(iSub)]), 'allCSV')

end