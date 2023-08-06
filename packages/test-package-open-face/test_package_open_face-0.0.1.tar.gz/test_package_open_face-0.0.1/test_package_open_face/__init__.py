import json
import os
import time
import argparse

def open_face_processing(files_list_path,write_file_path):
    path = "/opt/openface-20220208/"
    os.chdir(path)
    count = 0
    for file in os.listdir(files_list_path):
        if file.endswith(".mp4"):
            print("#####################"+str(file)+"#################")
            print(count)
            file_path = os.path.join(files_list_path,file)
            file_write_path = os.path.join(write_file_path,file.split(".")[0])
            if not os.path.exists(file_write_path):
                os.mkdir(file_write_path)
            print(file_write_path+"/")
            path_exe = "./FaceLandmarkVidMulti -f "+ str(file_path)+" -out_dir "+ str(file_write_path)+"/"
            print(path_exe)
            os.system(path_exe)
            count = count + 1
            time.sleep(10)

