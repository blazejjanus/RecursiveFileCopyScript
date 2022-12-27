#Python script aimed to make a copy of project files
#Script version: 1.2
#Changes from version: 1.1
#Fixed bug causing not creating folders in destination path
#Changed from version: 1.0
#Fixed the bug causing not maintaining subfolders structure in destiantion path

import shutil, errno, os, datetime, glob, fileinput
from distutils.dir_util import copy_tree

global num_of_folders_created

def two_num_str(src_str):
    if(len(src_str)==1):
        src_str="0"+src_str;
    return src_str
#End of two_num_str

def set_filename():
    #Get current time
    now = datetime.datetime.now()
    hour=now.hour;
    minute=now.minute;
    s_hour=str(hour);
    s_hour=two_num_str(s_hour);
    s_minute=str(minute);
    s_minute=two_num_str(s_minute);
    filename=s_hour+"-"+s_minute+".log";
    return filename
#End of set_filename

def set_foldername():
    now = datetime.datetime.now()
    day=now.day;
    month=now.month;
    year=now.year;
    s_day=str(day);
    s_day=two_num_str(s_day);
    s_month=str(month);
    s_month=two_num_str(s_month);
    folder=s_day+"-"+s_month+"-"+str(year);
    return folder
#End of set_foldername

def make_folder(name,path):
    full_path=path+"\\"+name;
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        return "created"
    if os.path.exists(full_path):
        return "exists"
    return "failure"
#End of make_folder

def get_time():
    ct=datetime.datetime.now();
    d=str(ct.day);
    d=two_num_str(d);
    m=str(ct.month);
    m=two_num_str(m);
    y=str(ct.year);
    h=str(ct.hour);
    h=two_num_str(h);
    m=str(ct.minute);
    m=two_num_str(m);
    s=str(ct.second);
    s=two_num_str(s);
    date=d+"."+m+"."+y;
    time=h+":"+m+":"+s;
    time_string = date+"   "+time;
    return time_string;
#End of get_time

def replace_placeholder(ext, counter, search, file_path):
    global num_of_folders_created;
    counter=str(counter);
    if(ext!='0'):
        replacement_text = "     "+ext+"   files:     "+counter+"\n"+search;
    else:
        replacement_text = "Number of all files copied:   "+counter+"\n"+"Number of all folders created:   "+str(num_of_folders_created)+"\n";
    file=open(file_path, "r");
    filedata = file.read()
    file.close()
    new_filedata=filedata.replace(search, replacement_text);
    file=open(file_path, "w");
    file.write(new_filedata);
    file.close();
#End of replace_placeholder

def remove_placeholder(file_path):
    search='placeholder';
    replacement_text='';
    file=open(file_path, "r");
    filedata = file.read()
    file.close()
    new_filedata=filedata.replace(search, replacement_text);
    file=open(file_path, "w");
    file.write(new_filedata);
    file.close();
#End of remove_placeholder

def copy_files_spec_ext(ext, file_path, root_path, dest_path):
    global num_of_folders_created
    ext_counter=0
    log_file=open(file_path, "r");
    old_file_data=log_file.read();
    log_file.close();
    log_file=open(file_path, "w");
    log_file.write(old_file_data);
    log_file.write("\nCopying ");
    log_file.write(ext);
    log_file.write(" files:\n");
    ext="."+ext;
    static_root_path=root_path;
    for root_path, dnames, fnames in os.walk(root_path):    
        for crt_file in fnames:
            if crt_file.endswith(ext):
                source_file_path =  os.path.join(root_path, crt_file)
                additional_folders=os.path.relpath(root_path, static_root_path);
                dest_folder_path   =  os.path.join(dest_path, additional_folders);
                #print(dest_folder_path);
                dest_file_path   =  os.path.join(dest_path, additional_folders, crt_file);
                if not os.path.exists(dest_folder_path):
                    os.makedirs(dest_folder_path);
                    num_of_folders_created=num_of_folders_created+1
                    log_file.write("   ");
                    log_file.write("Created missing folder:   ");
                    log_file.write(dest_folder_path);
                    log_file.write("\n");
                shutil.copyfile(source_file_path, dest_file_path)
                ext_counter=ext_counter+1;
                log_file.write("   ");
                log_file.write(str(crt_file));
                log_file.write("   copied from:   ");
                log_file.write(str(source_file_path));
                log_file.write("   to:   ");
                log_file.write(str(dest_file_path));
                log_file.write("\n\n");
    log_file.close();
    replace_placeholder(ext, ext_counter, "placeholder", file_path);
    return ext_counter;
#End of copy_files_spec_ext

def main():
    #Flags:
    debug=0;
    #End of flags
    global num_of_folders_created
    num_of_folders_created=0
    #Paths
    src = r'SOURCE_DIRECTORY_HERE'
    trg = r'TARGET_DIRECTORY_HERE'
    log = r'LOG_DIRECTORY_HERE'
    #End of paths
    
    filename=set_filename();
    foldername=set_foldername();
    if(debug==1):
        print("\nLog filename:   ", filename);
        print("\nLog foldername:   ", foldername);
    folder_status=make_folder(foldername,log);
    if(debug==1):
        print("\nStatus of log folder creation:   ", folder_status);
    #Making log file
    full_path=log+"\\"+foldername+"\\"+filename;
    if(folder_status!='failure'):
        current_time=get_time();
        log_file=open(full_path, "w+");
        log_file.write("This is log file from copying projects.\n");
        log_file.write(current_time);
        log_file.write("\n\n");
        log_file.write("Log folder creation status: %s" % folder_status);
        log_file.write("\n\n");
        log_file.write("general_number");
        log_file.write("\n");
        log_file.write("placeholder");
    #Copy files
    counter=0;
    #C
    log_file.close();
    c_counter=copy_files_spec_ext("c", full_path, src, trg);
    counter=counter+c_counter;
    #Cpp
    c_counter=copy_files_spec_ext("cpp", full_path, src, trg);
    counter=counter+c_counter
    #H
    c_counter=copy_files_spec_ext("h", full_path, src, trg);
    counter=counter+c_counter
    #Dev (Dev-C++ project)
    c_counter=copy_files_spec_ext("dev", full_path, src, trg);
    counter=counter+c_counter
    #Layout
    c_counter=copy_files_spec_ext("layout", full_path, src, trg);
    counter=counter+c_counter
    #Win
    c_counter=copy_files_spec_ext("win", full_path, src, trg);
    counter=counter+c_counter
    #Depend (Dependency files of Code::Blocks projects)
    c_counter=copy_files_spec_ext("depend", full_path, src, trg);
    counter=counter+c_counter
    #CBP (Code::Blocks project)
    c_counter=copy_files_spec_ext("cbp", full_path, src, trg);
    counter=counter+c_counter
    #Additional extensions should be placed here

    #Removing redundant placeholder
    remove_placeholder(full_path);

    replace_placeholder('0', counter, 'general_number', full_path);
    file=open(full_path, "a");
    file.write("\n\nEnd of log file");
    file.close();

    if(debug==1):
        print("\nFolders created:   ", num_of_folders_created);
        print("\nFiles copied:   ", counter);
    

#end of main


#Begining
main()

#End of Program
