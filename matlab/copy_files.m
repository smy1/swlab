% Copy all subjects' data (*.snirf and *.tri) file into one target folder
% Author: Chia-Feng Lu, 2024.1.21
% Edited by MYSia (20.3.2025) for MoChi
clear all

%% folder setup
MainFolder='C:\Users\user\Desktop\matlab\cflu\nirsdata\ori'; %where the subfolders of all data are currently stored
TargetFolder='C:\Users\user\Desktop\matlab\cflu\nirsdata\alldata'; %where the copied files should be stored
CFLFolder='C:\Users\user\Desktop\matlab\cflu\nirsdata\for_proflu'; %location to store data folders that should be sent to Prof Lu

%% Copy .snirf and .tri files
mdata=readtable('mochi_id.xlsx','Sheet','mochi');
mdata.solo_ok=str2double(mdata.solo_ok); %this column specifies our data selection criteria
mdata.test_date=datetime(mdata.test_date,'Format','yyyy-MM-dd'); %this column specifies the date of testing (which is the 1st-layer-subfolder)
mdata=table2struct(mdata);

for i = 1:length(mdata) %one row per participant
    if mdata(i).solo_ok<=2.5 %data is included even if the child talked to the parent, as long as the parent did not respond
        %for the child data
        SourceC=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsC]; %child ID is the 2nd-layer-subfolder
        dirinfo=dir(SourceC); 
        dirinfo(1:2)=[];
        for j = [2 9] %extract only snirf & tri file
            tmpchild=dir([SourceC filesep dirinfo(j).name]);
            copyfile([SourceC filesep tmpchild(1).name],...
                    [TargetFolder filesep tmpchild(1).name]);
        end
        %for the adult data
        SourceA=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsA]; %adult ID is the 2nd-layer-subfolder
        dirinfo=dir(SourceA); 
        dirinfo(1:2)=[];
        for j = [2 9] %%extract only snirf & tri file
            tmpadult=dir([SourceA filesep dirinfo(j).name]);
            if tmpchild.name(1:3) == 'c45' %special case: the mother participated with her older child a few days after she participated with her younger child
                copyfile([SourceA filesep tmpadult(1).name],...
                        [TargetFolder filesep tmpadult(1).name(1:3) filesep tmpadult(1).name(1:3) '_201' tmpadult(1).name(8:15)]);
            else
                copyfile([SourceA filesep tmpadult(1).name],...
                        [TargetFolder filesep tmpadult(1).name]);
            end
        end
    end
end

%% Copy usable data folders for prof lu
for i = 1:length(mdata) %one row per participant
    if mdata(i).solo_ok<=2.5 %the child might have talked to the parent, but the parent did not respond
        %for the child folder
        SourceC=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsC]; 
        copyfile([SourceC],...
                [CFLFolder filesep mdata(i).nirsC]);
        %for the adult folder
        SourceA=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsA]; 
        copyfile([SourceC],...
                [CFLFolder filesep mdata(i).nirsA]);
        %for the dyad folder
        SourceD=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsID]; 
        copyfile([SourceD],...
                [CFLFolder filesep mdata(i).nirsID]);        
    end
end
