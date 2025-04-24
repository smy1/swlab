% Copy all subjects' data (*.snirf and *.tri) file into one target folder
% Author: Chia-Feng Lu, 2024.1.21
% Edited by MYSia (24.04.2025) to (1) include exclusion criteria, and (2) dig into another level of subfolder
clear all

%% folder setup
SourceFolder='C:\Users\user\Desktop\mochi\mochi_data_20250322';
nirsFolder='C:\Users\user\Desktop\mochi\alldata'; %where the copied snirf files should be stored
triFolder='C:\Users\user\Desktop\mochi\tri'; %where the copied tri files should be stored

%% Check table for excluded data
mdata=readtable('mochi_id.xlsx','Sheet','mochi');
mdata.solo_ok=double(mdata.solo_ok); %for v2017b (instead of str2double); our selection criteria
% mdata.test_date=datetime(mdata.test_date,'Format','yyyy-MM-dd'); %the date of testing (which is the 1st-lvl-subfolder)
mdata=table2struct(mdata);
istable(mdata) %check conversion: should be 0

excluded=[]; %to keep excluded IDs
for i = 1:length(mdata)
    if mdata(i).solo_ok==4 %exclusion criteria: parent's response was > 5 secs
        excluded=[excluded; mdata(i).nirsA; mdata(i).nirsC]; 
    end
end
excluded=cellstr(excluded);

%% Copy files
dirinfo=dir(SourceFolder);
dirinfo(1:2)=[];
for i=1:length(dirinfo)
    if dirinfo(i).isdir==1
        % snirf file
        tmpfile=dir([SourceFolder filesep dirinfo(i).name filesep '*' filesep '*.snirf']);
        for j=1:length(tmpfile)
            subfile=tmpfile(j).folder;
            if ismember(subfile(end-6:end), excluded)
                fprintf([subfile(end-6:end) ' is an unwanted ID. \n'])
            else
                if isempty(tmpfile)
                    fprintf(['No snirf file is found in ' dirinfo(i).name '. \n'])
                elseif strcmp(subfile(end-17:end-4), '2025-02-24\a17') %special case: same adult, different day
                    copyfile([subfile filesep tmpfile(j).name],...
                        [nirsFolder filesep tmpfile(j).name(1:3) '_201' tmpfile(j).name(8:13)]);
                else
                    copyfile([subfile filesep tmpfile(j).name],...
                        [nirsFolder filesep tmpfile(j).name]);
                end
            end
        end
        % tri file
        tmpfile=dir([SourceFolder filesep dirinfo(i).name filesep '*' filesep '*_lsl.tri']);
        for j=1:length(tmpfile)
            subfile=tmpfile(j).folder;
            if ismember(subfile(end-6:end), excluded)
                fprintf([subfile(end-6:end) ' is an unwanted ID. \n'])
            else
                if isempty(tmpfile)
                    fprintf(['No snirf file is found in ' dirinfo(i).name '. \n'])
                elseif strcmp(subfile(end-17:end-4), '2025-02-24\a17') %special case:same adult, different day
                    copyfile([subfile filesep tmpfile(j).name],...
                        [triFolder filesep tmpfile(j).name(1:3) '_201' tmpfile(j).name(8:15)]);
                else
                    copyfile([subfile filesep tmpfile(j).name],...
                        [triFolder filesep tmpfile(j).name]);
                end
            end
        end
    end
end
