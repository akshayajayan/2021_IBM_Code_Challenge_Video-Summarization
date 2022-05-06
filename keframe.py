import os
import cv2
import subprocess
import numpy as np
filename = 'ped.mp4'

f = open("train.txt", 'a+')

def get_frame_types(video_fn):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [video_fn]).decode()
    frame_types = out.replace('pict_type=','').split()
    return zip(range(len(frame_types)), frame_types)

def save_i_keyframes(video_fn):
    frame_types = get_frame_types(video_fn)
    i_frames = [x[0] for x in frame_types if x[1]=='I']
    
    count=0
    if i_frames:
        basename = os.path.splitext(os.path.basename(video_fn))[0]
        cap = cv2.VideoCapture(video_fn)
        ret, prev = cap.read()
        
        grayImage = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
        (thresh, prev) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
        for frame_no in i_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            
            
            ret, frame = cap.read()
            grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            (thresh, frameNew) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
            diff = cv2.absdiff(prev, frameNew)
            non_zero_count = np.count_nonzero(diff)
            #print(non_zero_count)
            if non_zero_count>1000:
                print(non_zero_count)
                c=str(count)
                while len(c)!=3: c="0"+c
                outname ='key_frames/i_frame_'+str(c)+'.jpg'
                file_name = outname + '\n'
                f.write(file_name)
                cv2.imwrite(outname, frame)
                count+=1
                print ('Saved: '+outname)
            prev=frameNew
        cap.release()
    else:
        print ('No I-frames in '+video_fn)


if __name__ == '__main__':
    save_i_keyframes(filename) 