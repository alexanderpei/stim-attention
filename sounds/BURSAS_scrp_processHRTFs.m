clear all
clc

angles = {'00','15','30','90'};

for idxAng = 1:length(angles)
   fileName = fullfile('HRTFs',['H0e0' angles{idxAng} 'a.wav']); 
   temp = audioread(fileName);
   hrtf_left = temp(:,1);
   hrtf_right = temp(:,2);
   save(fullfile('HRTFs',['HRTF_L' angles{idxAng} '.mat']),'hrtf_left','hrtf_right');
   
   hrtf_left = temp(:,2);
   hrtf_right = temp(:,1);
   save(fullfile('HRTFs',['HRTF_R' angles{idxAng} '.mat']),'hrtf_left','hrtf_right');
end