% Copy all subjects' data (*.snirf and *.tri) file into one target folder
% Author: Chia-Feng Lu, 2024.1.21
% Edited by MYSia (19.4.2025) for MoChi
clear all

%% Folder setup
MainFolder='C:\Users\user\Desktop\matlab\mochi_data_20250322'; %where the subfolders of all data are currently stored
nirsFolder='C:\Users\user\Desktop\matlab\alldata'; %where the copied snirf files should be stored
triFolder='C:\Users\user\Desktop\matlab\tri'; %where the copied tri files should be stored
%CFLFolder='C:\Users\user\Desktop\matlab\cflu\nirsdata\for_proflu'; %location to store data folders that should be sent to Prof Lu

%% Check table - to copy or not to copy
mdata=readtable('mochi_id.xlsx','Sheet','mochi');
mdata.solo_ok=double(mdata.solo_ok); %for v2017b (instead of str2double) our data selection criteria
mdata.test_date=datetime(mdata.test_date,'Format','yyyy-MM-dd'); %the date of testing (which is the 1st-lvl-subfolder)
mdata=table2struct(mdata);
istable(mdata) %check conversion: should be 0

% Copy .snirf and .tri files
for i = 1:length(mdata) %one row per participant
    if mdata(i).solo_ok<4 %inclusion criteria: parent's response was <= 5 secs
        %for the child data
        SourceC=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsC]; %child ID is the 2nd-lvl-subfolder
        dirinfo=dir(SourceC); %check the order of files here
        dirinfo(1:2)=[];
        if i <= 4 %hard coding: pilot data's files are ordered differently
             for j = [3] %extract snirf file
                tmpchild=dir([SourceC filesep dirinfo(j).name]);
                copyfile([SourceC filesep tmpchild(1).name],...
                        [nirsFolder filesep tmpchild(1).name]);
             end
             for j = [10] %extract tri file
                tmpchild=dir([SourceC filesep dirinfo(j).name]);
                copyfile([SourceC filesep tmpchild(1).name],...
                        [triFolder filesep tmpchild(1).name]);
             end
        else %for other test IDs
            for j = [2] %extract snirf file
                tmpchild=dir([SourceC filesep dirinfo(j).name]);
                copyfile([SourceC filesep tmpchild(1).name],...
                        [nirsFolder filesep tmpchild(1).name]);
            end
            for j = [9] %extract tri file
                tmpchild=dir([SourceC filesep dirinfo(j).name]);
                copyfile([SourceC filesep tmpchild(1).name],...
                        [triFolder filesep tmpchild(1).name]);
            end
        end
        %for the adult data
        SourceA=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsA]; %adult ID is the 2nd-layer-subfolder
        dirinfo=dir(SourceA); %check the order of files here
        dirinfo(1:2)=[];
        if i <= 4 %hard coding: see above
             for j = [3] %extract snirf file
                tmpadult=dir([SourceA filesep dirinfo(j).name]);
                copyfile([SourceA filesep tmpadult(1).name],...
                        [nirsFolder filesep tmpadult(1).name]);
             end
             for j = [10] %extract tri file
                tmpadult=dir([SourceA filesep dirinfo(j).name]);
                copyfile([SourceA filesep tmpadult(1).name],...
                        [triFolder filesep tmpadult(1).name]);
             end
        else %for other test IDs
            for j = [2] %extract snirf file
                tmpadult=dir([SourceA filesep dirinfo(j).name]);
                if tmpchild.name(1:3) == 'c45' %special case: the mother participated with another child a few days later
                    copyfile([SourceA filesep tmpadult(1).name],...
                        [nirsFolder filesep tmpadult(1).name(1:3) '_201' tmpadult(1).name(8:13)]);
                else
                    copyfile([SourceA filesep tmpadult(1).name],...
                         [nirsFolder filesep tmpadult(1).name]);
                end
            end
            for j = [9] %extract tri file
                tmpadult=dir([SourceA filesep dirinfo(j).name]);
                if tmpchild.name(1:3) == 'c45' %special case: see above
                    copyfile([SourceA filesep tmpadult(1).name],...
                        [triFolder filesep tmpadult(1).name(1:3) '_201' tmpadult(1).name(8:15)]);
                else
                    copyfile([SourceA filesep tmpadult(1).name],...
                        [triFolder filesep tmpadult(1).name]);
                end
            end
        end
    else
        i = i+1;
        fprintf('skipped excel line: %i\n', i)
    end
end

%% Copy usable data folders for prof lu
% for i = 1:length(mdata) 
%     if mdata(i).solo_ok<=3 
%         %for the child folder
%         SourceC=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsC]; 
%         copyfile([SourceC],...
%                 [CFLFolder filesep mdata(i).nirsC]);
%         %for the adult folder
%         SourceA=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsA]; 
%         if SourceC(59:61) == 'c45' %special case: the mother participated with her older child a few days after she participated with her younger child
%             copyfile([SourceA],...
%                     [CFLFolder filesep mdata(i).nirsA(1:3) '_201']);
%         else        
%             copyfile([SourceA],...
%                     [CFLFolder filesep mdata(i).nirsA]);
%         end
%         %for the dyad folder
%         SourceD=[MainFolder filesep char(mdata(i).test_date) filesep mdata(i).nirsID]; 
%         copyfile([SourceD],...
%                 [CFLFolder filesep mdata(i).nirsID]);        
%     end
% end