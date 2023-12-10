'''
parse3dfingertip.py
version: 2.1  @2022/10/18
Wenchin Hsieh @Goomo.Net Studio, wenchin@goomo.net
References: 
1. https://google.github.io/mediapipe/solutions/hands.html
2. https://github.com/TemugeB/handpose3d
'''

import sys, datetime
import cv2 as cv
import mediapipe as mp
from utils import DLT, get_projection_matrix

mirror_camera = True # False
color_handedness = (255, 0, 0)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands0 = mp_hands.Hands(min_detection_confidence=0.5, max_num_hands=2, min_tracking_confidence=0.5)
hands1 = mp_hands.Hands(min_detection_confidence=0.5, max_num_hands=2, min_tracking_confidence=0.5)
c0 = mp_hands.HandLandmark.INDEX_FINGER_TIP.value
choice = [c0]

# 讀取指定的 Stereo Camera ID
if len(sys.argv) == 3:
    input_stream1 = int(sys.argv[1])
    input_stream2 = int(sys.argv[2])
else:
    print("Stereo Camera ID ?")
    quit()

# Input video stream
cap0 = cv.VideoCapture(input_stream1)
cap1 = cv.VideoCapture(input_stream2)
caps = [cap0, cap1]

frame0_height = int(cap0.get(cv.CAP_PROP_FRAME_HEIGHT))
frame0_width  = int(cap0.get(cv.CAP_PROP_FRAME_WIDTH))
frame1_height = int(cap1.get(cv.CAP_PROP_FRAME_HEIGHT))
frame1_width  = int(cap1.get(cv.CAP_PROP_FRAME_WIDTH))

print(f'鏡頭 {input_stream1} 解析度： Width = {frame0_width}, Height = {frame0_height}')
print(f'鏡頭 {input_stream2} 解析度： Width = {frame1_width}, Height = {frame1_height}\n')

if (frame0_height == frame1_height) and (frame0_width == frame1_width):
    frame_shape = [frame0_height, frame0_width]
else:        
    print('兩顆鏡頭的解析度不同！')
    quit()

# Set camera resolution
#frame_shape = [480, 640] # [720, 1280]
#for cap in caps:
#    cap.set(cv.CAP_PROP_FRAME_HEIGHT, frame_shape[0])
#    cap.set(cv.CAP_PROP_FRAME_WIDTH, frame_shape[1])

# DLT - Projection Matrices
P0 = get_projection_matrix(0)
P1 = get_projection_matrix(1)


# 解析 雙手 食指尖 3D 座標，轉譯成操控指令
def resolve_fingertip(Lfingertip, Rfingertip):
    # 重新調整 X Y Z 三個軸向，並平移調整座標原點至適當位置
    Lx, Ly, Lz = Lfingertip[1] - 20, 10 - Lfingertip[0], -Lfingertip[2] 
    Rx, Ry, Rz = Rfingertip[1] - 20, 10 - Rfingertip[0], -Rfingertip[2] 

    # 左指尖 在 Z 軸上的數值
    p = int(Lz / 25 * 99)
    if p >= 0:
        cmd_Lfw = 99 if p > 99 else p
        spd_Lwheel = cmd_Lfw
    else:
        cmd_Lbw = 99 if p < -99 else -p
        spd_Lwheel = - cmd_Lbw

    # 右指尖 在 Z 軸上的數值
    p = int(Rz / 25 * 99)
    if p >= 0:
        cmd_Rfw = 99 if p > 99 else p
        spd_Rwheel = cmd_Rfw
    else:
        cmd_Rbw = 99 if p < -99 else -p
        spd_Rwheel = - cmd_Rbw

    # 兩指尖 在 Y 軸上的平均數值
    p = int((Ly + Ry) / 2 / 30 * 99)
    cmd_H = 0 if p < 0 else 99 if p > 99 else p

    # 兩指尖 在 X 軸上之距離
    p = int((abs(Lx - Rx) - 10) / 30 * 99)
    cmd_C = 0 if p < 0 else 99 if p > 99 else p

    # 顯示操控指令
    sdt = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
    tip3d = f'L[{Lx:3d},{Ly:3d},{Lz:3d}]\tR[{Rx:3d},{Ry:3d},{Rz:3d}]'
    wheel = f'車輪L,R: ({spd_Lwheel:3d},{spd_Rwheel:3d})'
    servo = f'升降:{cmd_H:2d}\t夾鉗:{cmd_C:2d}'
    print(f'{sdt}\t{tip3d}\t{wheel}\t{servo}')

    resolved = True
    return resolved


# Main Loop
while True:
    #read frames from stream
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

    if not ret0 or not ret1: 
        print("Some Cameras are not ready !")
        break
        #continue

    # Crop to square: 480x480 or 720x720 
    # Note: camera calibration parameters are set to this resolution.If you change this, make sure to also change camera intrinsic parameters
    frame0 = frame0[:, (frame_shape[1]//2 - frame_shape[0]//2) : (frame_shape[1]//2 + frame_shape[0]//2)]
    frame1 = frame1[:, (frame_shape[1]//2 - frame_shape[0]//2) : (frame_shape[1]//2 + frame_shape[0]//2)]

    # the BGR image to RGB.
    frame0 = cv.cvtColor(frame0, cv.COLOR_BGR2RGB)
    frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2RGB)

    # To improve performance, optionally mark the image as not writeable to pass by reference.
    frame0.flags.writeable = False
    frame1.flags.writeable = False
    results0 = hands0.process(frame0)
    results1 = hands1.process(frame1)

    LH2d = [-1, -1] # 記錄 [在 frame0 中被判別為左手的 Hand 序號 , 在 frame1 中被判別為左手的 Hand 序號]
    RH2d = [-1, -1] # 記錄 [在 frame0 中被判別為右手的 Hand 序號 , 在 frame1 中被判別為右手的 Hand 序號]
    

    # Camera 0:
    frame0_keypoints = [[],[]]
    if results0.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results0.multi_hand_landmarks):
            if i < 2:
                hlabel = results0.multi_handedness[i].classification[0].label
                for p in range(21):
                    if p in choice:
                        x = int(round(frame0.shape[1]*hand_landmarks.landmark[p].x))
                        y = int(round(frame0.shape[0]*hand_landmarks.landmark[p].y))
                        frame0_keypoints[i].append([x, y])

                    if p == mp_hands.HandLandmark.INDEX_FINGER_TIP.value:
                        if hlabel == 'Left':
                            handedness, badge, tabs = '右手', 'R', '\t\t\t'
                            RH2d[0] = i
                        elif hlabel == 'Right':
                            handedness, badge, tabs = '左手', 'L', ''
                            LH2d[0] = i
                        cv.putText(frame0, badge, (x, y), cv.FONT_HERSHEY_COMPLEX, 0.8, color_handedness, 2)
                        #print(f'鏡頭 {input_stream1}, Hand {i}: 為{handedness}，食指尖 {tabs}@({x},{y})')


    # Camera 1:
    frame1_keypoints = [[],[]]
    if results1.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results1.multi_hand_landmarks):
            if i < 2:
                hlabel = results1.multi_handedness[i].classification[0].label
                for p in range(21):
                    if p in choice:
                        x = int(round(frame1.shape[1]*hand_landmarks.landmark[p].x))
                        y = int(round(frame1.shape[0]*hand_landmarks.landmark[p].y))
                        frame1_keypoints[i].append([x, y])

                    if p == mp_hands.HandLandmark.INDEX_FINGER_TIP.value:
                        if hlabel == 'Left':
                            handedness, badge, tabs = '右手', 'R', '\t\t\t'
                            RH2d[1] = i
                        elif hlabel == 'Right':
                            handedness, badge, tabs = '左手', 'L', ''
                            LH2d[1] = i
                        cv.putText(frame1, badge, (x, y), cv.FONT_HERSHEY_COMPLEX, 0.8, color_handedness, 2)
                        #print(f'鏡頭 {input_stream2}, Hand {i}: 為{handedness}，食指尖 {tabs}@({x},{y})')


    # Draw the hand annotations on the image.
    frame0.flags.writeable = True
    frame1.flags.writeable = True
    frame0 = cv.cvtColor(frame0, cv.COLOR_RGB2BGR)
    frame1 = cv.cvtColor(frame1, cv.COLOR_RGB2BGR)

    if results0.multi_hand_landmarks:
        for hand_landmarks in results0.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame0, hand_landmarks, mp_hands.HAND_CONNECTIONS, None, 
                mp_drawing_styles.get_default_hand_connections_style())

    if results1.multi_hand_landmarks:
        for hand_landmarks in results1.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame1, hand_landmarks, mp_hands.HAND_CONNECTIONS, None, 
                mp_drawing_styles.get_default_hand_connections_style())


    # Show Up Frames
    cv.imshow(f'Camera {input_stream1}', cv.flip(frame0, 1) if mirror_camera else frame0)
    cv.imshow(f'Camera {input_stream2}', cv.flip(frame1, 1) if mirror_camera else frame1)


    # Calculate Finger 3D Coordinate in World Space
    frame_p3ds_L, frame_p3ds_R = [], []

    LH3d = LH2d[0] >= 0 and LH2d[1] >= 0
    RH3d = RH2d[0] >= 0 and RH2d[1] >= 0

    if LH3d:
        for uv1, uv2 in zip(frame0_keypoints[LH2d[0]], frame1_keypoints[LH2d[1]]):
            if uv1[0] == -1 or uv2[0] == -1:
                _p3d = [-1, -1, -1]
            else:
                _p3d = DLT(P0, P1, uv1, uv2)
            frame_p3ds_L.append(_p3d)

        Lfingertip = [int(round(v)) for v in frame_p3ds_L[0]]
        #print('左手食指尖 3D 座標：\t\t\t\t\t\t', Lfingertip)

    if RH3d:
        for uv1, uv2 in zip(frame0_keypoints[RH2d[0]], frame1_keypoints[RH2d[1]]):
            if uv1[0] == -1 or uv2[0] == -1:
                _p3d = [-1, -1, -1]
            else:
                _p3d = DLT(P0, P1, uv1, uv2)
            frame_p3ds_R.append(_p3d)

        Rfingertip = [int(round(v)) for v in frame_p3ds_R[0]]
        #print('右手食指尖 3D 座標：\t\t\t\t\t\t\t\t', Rfingertip)

    if LH3d and RH3d:
        resolve_fingertip(Lfingertip, Rfingertip)


    # End of This Iteration
    #if LH2d[0] >= 0 or LH2d[1] >= 0 or RH2d[0] >= 0 or RH2d[1] >= 0:
    #    print(datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3], '\n')

    k = cv.waitKey(1)
    if k & 0xFF == 27: break #27 is ESC key.


cv.destroyAllWindows()
for cap in caps:
    cap.release()