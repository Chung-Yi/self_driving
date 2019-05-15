# Importing the libraries
import cv2
import socket
import numpy as np
import gpio_mod as mod

# -------------------------------------------
# Doing some Face Recognition with the webcam
# video 1
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 320) #weight
video_capture.set(4, 240) #height

# video 2
video_capture2 = cv2.VideoCapture(1)
video_capture2.set(3, 320) #weight
video_capture2.set(4, 240) #height

# video 3
video_capture3 = cv2.VideoCapture(2)
video_capture3.set(3, 320) #weight
video_capture3.set(4, 240) #height

# -------------------------------------------

# -------------------------------------------
# 1 camera 1
TCP_IP = ""
print(TCP_IP)
TCP_PORT = 3333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)

# 2 camera 2
TCP_IP2 = ""
print(TCP_IP2)
TCP_PORT2 = 5278
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((TCP_IP2, TCP_PORT2))
s2.listen(True)

# 3 camera 3
TCP_IP3 = ""
print(TCP_IP3)
TCP_PORT3 = 5487
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3.bind((TCP_IP3, TCP_PORT3))
s3.listen(True)

# 4 distance
TCP_IP4 = ""
print(TCP_IP4)
TCP_PORT4 = 8787
s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s4.bind((TCP_IP4, TCP_PORT4))
s4.listen(True)
# -------------------------------------------

# -------------------------------------------
# accept client
conn, addr = s.accept()
conn2, addr2 = s2.accept()
conn3, addr3 = s3.accept()
conn4, addr4 = s4.accept()
# -------------------------------------------

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

while True:
    # -------------------------------------------
    # get frame
    _, frame = video_capture.read()
    _, frame2 = video_capture2.read()
    _, frame3 = video_capture3.read()
    # -------------------------------------------

    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # -------------------------------------------
    # socket video 1
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(imgencode)
    stringData = data.tostring()

    #print(str(len(stringData)).ljust(16))
    conn.send(str(len(stringData)).ljust(16).encode(encoding='utf_8', errors='strict'))
    conn.send(stringData)
    # -------------------------------------------

    # -------------------------------------------
    # socket video 2
    result2, imgencode2 = cv2.imencode('.jpg', frame2, encode_param)
    data2 = np.array(imgencode2)
    stringData2 = data2.tostring()

    #print(str(len(stringData)).ljust(16))
    conn2.send(str(len(stringData2)).ljust(16).encode(encoding='utf_8', errors='strict'))
    conn2.send(stringData2)
    # -------------------------------------------

    # -------------------------------------------
    # socket video 3
    result3, imgencode3 = cv2.imencode('.jpg', frame3, encode_param)
    data3 = np.array(imgencode3)
    stringData3 = data3.tostring()

    #print(str(len(stringData)).ljust(16))
    conn3.send(str(len(stringData3)).ljust(16).encode(encoding='utf_8', errors='strict'))
    conn3.send(stringData3)
    # -------------------------------------------

    # -------------------------------------------
    # socket sensor
    dis = mod.sendSonic()
    conn4.send(dis)
    # -------------------------------------------

    ret, frame = video_capture.read()
    decimg=cv2.imdecode(data,1)
    #cv2.imshow('SERVER2',decimg)    
    #
    
   # cv2.imshow('Video', decimg)
    
    

    # receive socket msg
    res = conn.recv(1024)
    if res is None:
        print('Not get')
    elif res == b'60':
        mod.go_60()
        print(res)
    elif res == b'30':
        mod.go_30()
        print(res)
    elif res == b'stop':
        mod.stop()
        print(res)
    elif res == b'1':
        mod.go_30()
        print(res)
    elif res == b'2':
        mod.right1()
        print(res)
    elif res == b'3':
        mod.left1()
        print(res)
    # receive socket msg
    #traffic sign use (Peter
    elif res == b'sf60':
        mod.SP_60()
        print(res)
    elif res == b'sf30':
        mod.SP_30()
        print(res)
    elif res == b'sr60':
        mod.SP_60R()
        print(res)
    elif res == b'sr30':
        mod.SP_30R()
        print(res)
    elif res == b'sl60':
        mod.SP_60L()
        print(res)
    elif res == b'sl30':
        mod.SP_30L()
    # elif res == b'stop':
        # mod.stop()
        # print(res)
#traffic sign use (Peter
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
video_capture2.release()
video_capture3.release()
cv2.destroyAllWindows()
