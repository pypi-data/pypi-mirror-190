import sys
import os
import csv
import subprocess
import time
import argparse
import json


# This function is to check whether all necessary csv and video files exist or not and return info array
def get_file_dir_exist_array(check_dir, file_name_array_input):
    file_dir_exist_array = []
    for name in file_name_array_input:
        file_exist = os.path.isfile(os.path.join(check_dir, name))
        file_dir_exist_array.append([name, file_exist])
    return file_dir_exist_array


# This function is to get the positions in given array
def get_position(search_input, array_in):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(array_in):
        if val == search_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        print(f"{search_input} can not be found!")

    return return_idx


# This function is to read given csv and return first data of given column
def get_timestamp_from_csv(csv_dir_input, column_name_input):
    with open(csv_dir_input, "r") as csv_file:
        csv_data_array = csv.reader(csv_file, delimiter=',')
        header_array = next(csv_data_array)
        first_row = next(csv_data_array)
        data_position = get_position(column_name_input, header_array)

        return float(first_row[data_position])


# This function is to get video length from given string
def get_video_length(string_input):
    start_marker = "duration="
    end_marker = "[/FORMAT]"
    start_index = string_input.find(start_marker)
    end_index = string_input.find(end_marker)

    return float(string_input[start_index + len(start_marker):end_index])


# This function is to change sec to ffmpeg input format string
def change_sec_to_ffmpeg_time_format(time_input):
    millisecond_string_raw = "%.3f" % (time_input % 1,)
    start_marker = "."
    start_index = millisecond_string_raw.find(start_marker)
    millisecond_string = millisecond_string_raw[start_index:len(millisecond_string_raw)]
    hour_min_second_format_string = time.strftime('%H:%M:%S', time.gmtime(time_input))

    return hour_min_second_format_string + millisecond_string


# This function is to update gaze.csv by add 1 column called local_time
def update_gaze_csv(csv_dir_input, ts_column_name):
    csv_data_array = []
    with open(csv_dir_input, "r") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        header_array = next(csv_data)
        data_position = get_position(ts_column_name, header_array)
        start_time = None
        start_time_noted = False
        for data in csv_data:
            if not start_time_noted:
                start_time = float(data[data_position])
                start_time_noted = True
            local_time = str(float(data[data_position]) - start_time)
            data.append(local_time)
            csv_data_array.append(data)
        csv_file.close()

    header_array.append("local_time")
    out_put_csv = csv_dir_input.replace(".csv", "_updated.csv")
    with open(out_put_csv, mode='w', newline="") as destination_file:
        csv_writer = csv.DictWriter(destination_file, fieldnames=header_array)
        csv_writer.writeheader()
        for row in csv_data_array:
            temp_dict = {}
            for index, header in enumerate(header_array):
                temp_dict[header] = row[index]
            csv_writer.writerow(temp_dict)
        destination_file.close()
    print("")
    print(f"{csv_dir_input} is updated")


def get_timeline_trial_info(timeline_data_array_input, trial_id_input):
    timeline_trial_info = {}

    # tl = timeline, ts = timestamp
    for tl_data in timeline_data_array_input:
        trial_id = tl_data["start"]["event"]["trial_id"]
        if trial_id == "undefined":
            trial_id = tl_data["start"]["event"]["trial_index"]
        if trial_id == trial_id_input:
            start_ts = tl_data["start"]["timestamp"]["pts_time"]
            end_ts = tl_data["end"]["timestamp"]["pts_time"]
            trial_duration = end_ts - start_ts
            trial_type = tl_data["start"]["event"]["trial_type"]
            timeline_trial_info["trial_id"] = trial_id
            timeline_trial_info["trial_type"] = trial_type
            timeline_trial_info["start"] = start_ts
            timeline_trial_info["end"] = end_ts
            timeline_trial_info["duration"] = trial_duration
            break
    return timeline_trial_info


def get_trial_order(trial_name_input):
    trial_string, disk_string = str(trial_name_input).split("_")
    trial_number_array = str(trial_string).split("-")
    trial_order = (int(trial_number_array[1]) * 100) + int(trial_number_array[2])

    return int(trial_order)


def get_eye_timestamp_info(gaze_dir_input):
    info_dict = {}
    with open(gaze_dir_input, "r") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        header_array = next(csv_data)
        event_string_position = get_position("event_string", header_array)
        ts_position = get_position("sensor_timestamp", header_array)
        for data in csv_data:
            event_string = data[event_string_position]
            if "start" in str(event_string):
                trial_info = json.loads(event_string.replace("\'", "\""))
                trial_id = trial_info["trial_id"] \
                    if trial_info["trial_id"] != "undefined" else trial_info["trial_index"]
                trial_type = trial_info["trial_type"]
                timestamp_data = data[ts_position]
                info_dict[trial_id] = {"trial_type": trial_type, "timestamp": timestamp_data}
        csv_file.close()

    return info_dict


def create_syn_combined_eye_video(dir_input):
    os.chdir(dir_input)

    # read left and right timestamps
    # left_csv_dir = os.path.join(input_dir, "left_eye_timestamp.csv")
    left_timestamp = get_timestamp_from_csv("left_eye_timestamp.csv", "left_eye_timestamp")
    print("")
    print(f"Left timestamp: {left_timestamp}")
    print("")
    # right_csv_dir = os.path.join(input_dir, "right_eye_timestamp.csv")
    right_timestamp = get_timestamp_from_csv("right_eye_timestamp.csv", "right_eye_timestamp")
    print("")
    print(f"Right timestamp: {right_timestamp}")
    print("")
    timestamp_diff = round(left_timestamp - right_timestamp
                           if left_timestamp >= right_timestamp
                           else right_timestamp - left_timestamp, 3)
    print("")
    print(f"Timestamp difference: {timestamp_diff}")
    print("")
    timestamp_diff_ffmpeg_format = change_sec_to_ffmpeg_time_format(timestamp_diff)

    # check the length of both rotated videos
    left_v_len_check_cmd = "ffprobe -i left_video_rotated.mp4 -v quiet -show_entries format=duration " \
                           "-hide_banner "
    right_v_len_check_cmd = "ffprobe -i right_video_rotated.mp4 -v quiet -show_entries format=duration " \
                            "-hide_banner "
    left_v_len_check_output = subprocess.check_output(left_v_len_check_cmd, shell=True).decode('utf-8')
    left_v_length = get_video_length(left_v_len_check_output)
    print("")
    print(f"Left video length in sec: {left_v_length}")
    print("")
    right_v_len_check_output = subprocess.check_output(right_v_len_check_cmd, shell=True).decode('utf-8')
    right_v_length = get_video_length(right_v_len_check_output)
    print("")
    print(f"Right video length in sec: {right_v_length}")
    print("")

    # trimming the side which has earlier timestamp
    if left_timestamp >= right_timestamp:
        right_available_length = right_v_length - timestamp_diff
        right_available_length_ffmpeg_format = change_sec_to_ffmpeg_time_format(right_available_length)
        trim_type = "right"
        right_v_trim_cmd = f"ffmpeg -i right_video_rotated.mp4 " \
                           f"-ss {timestamp_diff_ffmpeg_format} " \
                           f"-t {right_available_length_ffmpeg_format} " \
                           f"-b:v 10M -c:a copy right_video_trimmed.mp4 -y"
        os.system(right_v_trim_cmd)
        print("")
        print("Right video is trimmed.")
        print("")
    else:
        left_available_length = left_v_length - timestamp_diff
        left_available_length_ffmpeg_format = change_sec_to_ffmpeg_time_format(left_available_length)
        trim_type = "left"
        left_v_trim_cmd = f"ffmpeg -i left_video_rotated.mp4 " \
                          f"-ss {timestamp_diff_ffmpeg_format} " \
                          f"-t {left_available_length_ffmpeg_format} " \
                          f"-b:v 10M -c:a copy left_video_trimmed.mp4 -y"
        os.system(left_v_trim_cmd)
        print("")
        print("Left video is trimmed.")
        print("")

    # merge videos
    right_trim_merge_cmd = "ffmpeg -i left_video_rotated.mp4 -i right_video_trimmed.mp4 -filter_complex " \
                           "hstack=inputs=2:shortest=1 -b:v 10M -c:a copy left_right_combined.mp4 -y"
    left_trim_merge_cmd = "ffmpeg -i left_video_trimmed.mp4 -i right_video_rotated.mp4 -filter_complex " \
                          "hstack=inputs=2:shortest=1 -b:v 10M -c:a copy left_right_combined.mp4 -y"
    if trim_type == "right":
        os.system(right_trim_merge_cmd)
        print("")
        print("Left and right videos are merged into left_right_combined.mp4")
        print("")
    elif trim_type == "left":
        os.system(left_trim_merge_cmd)
        print("")
        print("Left and right videos are merged into left_right_combined.mp4")
        print("")
    else:
        print("")
        print(f"Error! Trimming type is {trim_type}.")
        pass


def create_syn_videos_in_trials(dir_input):
    trial_dir = os.path.join(dir_input, "trials")

    # v = video, ts = timestamp, tl = timeline
    left_ts_csv_location = os.path.join(dir_input, "left_eye_timestamp.csv")
    right_ts_csv_location = os.path.join(dir_input, "right_eye_timestamp.csv")
    tl_file_location = os.path.join(dir_input, "timeline.json")
    left_v_location = os.path.join(dir_input, "left_video_rotated.mp4")
    right_v_location = os.path.join(dir_input, "right_video_rotated.mp4")
    gaze_file_location = os.path.join(dir_input, "gaze.csv")
    face_video_location = os.path.join(dir_input, "video.mp4")

    timeline_file = open(tl_file_location)
    timeline_data_array = json.load(timeline_file)

    eye_event_info = get_eye_timestamp_info(gaze_file_location)

    folder_array = [name for name in os.listdir(trial_dir) if os.path.isdir(os.path.join(trial_dir, name))]
    folder_array_sorted = sorted(folder_array, key=lambda x: get_trial_order(x))

    left_ts = get_timestamp_from_csv(left_ts_csv_location, "left_eye_timestamp")
    right_ts = get_timestamp_from_csv(right_ts_csv_location, "right_eye_timestamp")
    offset = 0

    for folder in folder_array_sorted:
        print("")
        print(f"Trial folder name:{folder} is work in progress.")
        print("")
        current_trial_dir = os.path.join(trial_dir, folder)
        video_folder_dir = os.path.join(current_trial_dir, "video")
        dir_exist = os.path.exists(video_folder_dir)
        if not dir_exist:
            os.makedirs(video_folder_dir)
        os.chdir(video_folder_dir)
        trial_id_string, disk_string = str(folder).split("_")
        tl_trial_info = get_timeline_trial_info(timeline_data_array, trial_id_string)

        if any(tl_trial_info) and "start" in tl_trial_info:
            # nj = node js, ff = in ffmpeg format, ts= timestamp, st = start time, tbt = to be trimmed
            print(tl_trial_info)
            trial_start_time_nj = float(tl_trial_info["start"]) + offset

            trial_start_time_nj_ff = change_sec_to_ffmpeg_time_format(trial_start_time_nj)

            trial_duration_nj = tl_trial_info["duration"]
            trial_duration_nj_ff = change_sec_to_ffmpeg_time_format(trial_duration_nj)

            trial_event_info = eye_event_info[trial_id_string]
            trial_start_ts = float(trial_event_info["timestamp"])
            diff_with_left_ts = trial_start_ts - left_ts
            diff_with_right_ts = trial_start_ts - right_ts
            left_v_st_tbt = change_sec_to_ffmpeg_time_format(diff_with_left_ts)
            right_v_st_tbt = change_sec_to_ffmpeg_time_format(diff_with_right_ts)

            # l = left, r = right, v = video
            face_v_trim_cmd = f"ffmpeg -i {face_video_location} " \
                              f"-ss {trial_start_time_nj_ff} " \
                              f"-t {trial_duration_nj_ff} " \
                              f"-b:v 10M -c:a copy trial_face_video.mp4 -y"
            os.system(face_v_trim_cmd)

            l_v_trim_cmd = f"ffmpeg -i {left_v_location} " \
                           f"-ss {left_v_st_tbt} " \
                           f"-t {trial_duration_nj_ff} " \
                           f"-b:v 10M -c:a copy trial_left_video.mp4 -y"
            os.system(l_v_trim_cmd)

            r_v_trim_cmd = f"ffmpeg -i {right_v_location} " \
                           f"-ss {right_v_st_tbt} " \
                           f"-t {trial_duration_nj_ff} " \
                           f"-b:v 10M -c:a copy trial_right_video.mp4 -y"
            os.system(r_v_trim_cmd)

            l_r_merge_cmd = f"ffmpeg -i trial_left_video.mp4" \
                            f" -i trial_right_video.mp4 -filter_complex " \
                            f"hstack=inputs=2:shortest=1 " \
                            f"-b:v 10M -c:a copy trial_left_right_video.mp4 -y"
            os.system(l_r_merge_cmd)

            overlay_cmd = f"ffmpeg -i   trial_face_video.mp4    -vf   \"movie=trial_left_right_video.mp4, " \
                          f"scale=192: -1 [inner]; [in][inner] overlay =10: 10 [out]\" " \
                          f"trial_left_right_face_video.mp4 -y "
            os.system(overlay_cmd)
        else:
            print(f"{trial_id_string} could not find in {tl_file_location}")
            error_string = f"Could not produce any trial video because " \
                           f"{trial_id_string} could not find in {tl_file_location}."
            log_writer = open("error_log.txt", "w")
            log_writer.write(error_string)
            log_writer.close()


def main():
    parser = argparse.ArgumentParser(prog='pim_video',
                                     description='PIM_VIDEO package.')
    parser.add_argument('--version', action='version', version='2.0.0'),
    parser.add_argument("-d", dest="input_directory", required=True, default=sys.stdin,
                        help="directory folder to be processed", metavar="directory name")
    parser.add_argument('-e', '--eye', dest="eye_boolean", help="eye video boolean",
                        action='store_true')
    parser.add_argument('-t', '--trial', dest="trial_boolean", help="trial videos boolean",
                        action='store_true')

    args = parser.parse_args()
    input_dir = args.input_directory
    eye_boolean = args.eye_boolean
    trial_boolean = args.trial_boolean

    # check whether input directory exists or not
    dir_exist = os.path.isdir(input_dir)
    if not dir_exist:
        print("")
        print(f"Error! Input directory:{input_dir} does not exist.")
        print("")
    else:
        print("")
        print("Input directory is found.")
        print("")
        # check whether any of those files is missing or not
        file_name_array = ["gaze.csv", "left_eye_timestamp.csv",
                           "right_eye_timestamp.csv", "left_video.mp4",
                           "right_video.mp4", "timeline.json"]
        dir_exist_array = get_file_dir_exist_array(input_dir, file_name_array)
        all_file_found = True
        for exist_array in dir_exist_array:
            if not exist_array[1]:
                print("")
                print(f"Error! {exist_array[0]} file is missing.")
                print("")
                all_file_found = False
        if all_file_found:
            print("")
            print("All necessary csv files and videos are found.")
            print("")

            # check whether there is ffmpeg or not
            ffmpeg_check_cmd = "ffmpeg -version"
            try:
                ffmpeg_check_output = subprocess.check_output(ffmpeg_check_cmd, shell=True)
                ffmpeg_check_output = ffmpeg_check_output.decode('utf-8')
                print(ffmpeg_check_output)
                is_there_ffmpeg = True
            except Exception as error:
                print(error)
                is_there_ffmpeg = False

            if is_there_ffmpeg:
                print("")
                print("Essential software, ffmpeg is found and start processing...")
                print("")
                st = time.time()
                os.chdir(input_dir)
                # update the gaze.csv
                update_gaze_csv("gaze.csv", "sensor_timestamp")

                # rotate the eye videos
                left_v_rotate_cmd = "ffmpeg -i left_video.mp4 -vf \"transpose=2\" -b:v 10M -c:a copy " \
                                    "left_video_rotated.mp4 -y"
                right_v_rotate_cmd = "ffmpeg -i right_video.mp4 -vf \"transpose=2\" -b:v 10M -c:a copy " \
                                     "right_video_rotated.mp4 -y"
                os.system(left_v_rotate_cmd)
                os.system(right_v_rotate_cmd)

                print("")
                print("Left and right videos have been rotated.")
                print("")

                # only eye videos synchronizing will be done
                # because there is only -t in input command line
                if not eye_boolean and trial_boolean:
                    print("")
                    print("Eye videos synchronizing and combination are disabled but trial videos will be created.")
                    print("")
                    create_syn_videos_in_trials(input_dir)

                # only trial videos will be created
                # because there is only -e in input command line
                elif eye_boolean and not trial_boolean:
                    print("")
                    print("Trial videos creating is disabled but eye videos will be synchronized and combined.")
                    print("")
                    create_syn_combined_eye_video(input_dir)

                # both processes will be done
                else:
                    create_syn_combined_eye_video(input_dir)
                    create_syn_videos_in_trials(input_dir)

                et = time.time()
                print(f"Process took {(et - st) / 60} minutes.")
            else:
                print("")
                print("Essential software, ffmpeg is not found.")
                print("Please read how to install ffmpeg from links below.")
                print("For windows: https://www.wikihow.com/Install-FFmpeg-on-Windows")
                print("For mac: https://bbc.github.io/bbcat-orchestration-docs/installation-mac-manual/")
