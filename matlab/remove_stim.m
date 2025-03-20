%%  INFO
% Affiliation: SW-Lab, Dept of CFS, NTNU
% Project: Peekaboo (aka Omi2)
% Date: 05.07.2024 (long count: 13.0.11.12.14, 6 Ix')
% Original script was written by Chi-Chuan Chen on June 2020 (see README.md for why it needs to be adapted)
% Edited by MY Sia (with LOTS of help from the web, see README.md for more)

% Aim of script: Toggle off rejected stimuli for each .snirf file
% Input: Individual snirf files or folders and an excel file showing which stimuli needs to be rejected
% Output: Updated groupResults.mat with rejected stimuli toggled off
% Recommended directory: project folder -> .snirf files/folders + excel file
% Requirement: Homer3 is included in MATLAB path (see README.md for more)
% - This script was edited using MATLAB R2017b (but it also runs on MATLAB R2019b, not sure about the other versions)
% - Homer3 v1.80.2 was used, not sure if the script is compatible with other versions

%% START HERE:
clear all
cd = 'C:\Users\users\Desktop\PEEKABOO\peekanirs\peek_021';

% start Homer3 to create groupResults.mat, if the .mat file already exists, skip this
Homer3
% - click cancel when prompted for cfg files, then close the opened Homer3 window

%% PREPARE THE EXCEL FILE:
% One sheet "nirs2ID" that matches snirf file name to participant ID
% Another sheet "gaze" that codes for each trial whether the child was looking at the screen
[n1, t1, nirs2ID] = xlsread('peeka021.xlsx', 'nirs2ID'); %use the raw file so that we can read IDs as characters
[gaze, t2, r2] = xlsread('peeka021.xlsx', 'gaze'); %use the number file so that the gaze coding is treated as a double

% Regardless of children's gaze:
% - we want to retain only the first training trial to make it a "block design"
[row, col] = size(gaze);
for px = 2:row %one row per participant
    for tr = 2:col %one column per trial
        % (1)make all first training trials as 1
        if (~isnan(gaze(px, tr))) && (gaze(1, tr)==1)
            gaze(px, tr) = 1;
        % (2)for other training trials, make them 0
        elseif (~isnan(gaze(px, tr))) && (gaze(1, tr)>1)
            gaze(px, tr) = 0;
        end
    end
end

%% WORK ON GROUPRESULTS.MAT:
load .\derivatives\homer\groupResults.mat;

% Loop "subjs" to deal with each test date
for sj = 1:length(group(1).subjs)
    num_test = group(1).subjs(sj).sess(1).runs;
    
    % Loop "runs" to deal with each participant
    for r = 1:length(num_test) 
        % (1)Extract snirf file name
        snirf_file = group(1).subjs(sj).sess(1).runs(r).name;
        [filepath, name, ext] = fileparts(snirf_file);
        snirf_id = name;
        
        % (2)Find the corresponding ID position (row number) in the excel file
        % - in the snirf to participant ID matching sheet
        IDflag = find(nirs2ID(:, 1)==string(snirf_id));
        subj_id = nirs2ID{IDflag, 2};
        % - in the gaze coding sheet
        IDflag = find(gaze(:, 1)==subj_id);
        lookingvec = gaze(IDflag, :);
        lookingvec = lookingvec(~isnan(lookingvec)); %remove NAN
        lookingvec = lookingvec(2:end); %remove ID number
        
        % (3)Prepare the "stim.states" table
        % - "states" of stimuli (aka "triggers") are either 1 (stimulus is accepted) or -1 (stimulus is rejected)
        % - stimuli in Homer3's GroupResults are stored separately,
        % - whereas the gaze coding sheet sorts the stimuli by timepoints
        % - hence, we need to compile the stimulus-state tables
        all_trig = zeros(1, 2); %create a dummy
        for tg = 1:3 %we have 3 triggers
            xx = group(1).subjs(sj).sess(1).runs(r).procStream.input.acquired.stim(1, tg).states; %extract each table
            all_trig = vertcat(all_trig, xx); %append the table to the dummy
        end
        all_trig = all_trig(2:end, :); %remove 0 from the dummy
        all_trig = sortrows(all_trig, 1); %sort the compiled table by timepoints
        
        % (4)Reject the stimulus if the child did not look at the screen
        % - flag no-look timepoints
        while length(lookingvec) > length(all_trig)
            lookingvec = lookingvec(1:end-1);
        end
        % - index no-look position
        nolookflag = all_trig(lookingvec==0);
        % - turn no-look timepoints into -1
        for i = 1:length(nolookflag)
            rownum = find(all_trig(:, 1)==nolookflag(i));
            all_trig(rownum, 2) = all_trig(rownum, 2)*-1;
        end
        
        % (5)Transfer the compiled "stim.states" back to GroupResults
        % - compare the timepoints and update the "stim.states" in GroupResults
        for tg = 1:3
            for j = 1:length(all_trig)
                rownum = group(1).subjs(sj).sess(1).runs(r).procStream.input.acquired.stim(1, tg).states(:, 1)==all_trig(j, 1);
                group(1).subjs(sj).sess(1).runs(r).procStream.input.acquired.stim(1, tg).states(rownum, 2) = all_trig(j, 2);
            end
        end        
    end
end

%% NOW SAVE IT:
save .\derivatives\homer\groupResults.mat;
Homer3 %start Homer3 again to check visually whether the rejected stimuli have been toggled off

%%%% END OF SCRIPT %%%%
