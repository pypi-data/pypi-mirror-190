from test_package import open_face_processing

def process_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_folder_read_path",
                        help="Pass the folder containing all video files to read", type=str)
    parser.add_argument("--write_path_file_path",
                        help="save the outcomes of open face in this path", type=str)
    #parser.add_argument("--path",
    #                    help="Pass the first timestamp at the starting point of the video",
    #                    type=float)
    args = parser.parse_args()
    video_folder_read_path = args.video_file_read_path
    write_path_file_path = args.write_path_file_path
    #first_linux_time_stamp = args.first_time_stamp_info
    open_face_processing(video_folder_read_path, write_path_file_path)
