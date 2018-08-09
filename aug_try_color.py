import numpy as np
import cv2
import time

# a simple augmented reality application
# which works on a chessboard pattern
# same setting parameters
patternSize = (9,6) # pattern size to look for
time_delay = 0.01 # time delay
cap = cv2.VideoCapture('video.mp4')
count = 0
img_mona = cv2.imread('mona.jpg')
rows,cols,ch = img_mona.shape
mona = np.zeros((720,1280,3), dtype=np.float32)
out_shape = (1280,720)
mona[250:250+rows, 500:500+cols, :] = img_mona
print("mona lisa shape is " + str(img_mona.shape))
# initializing the array that will keep the user choice for initial points of the augmented picture
initialCoordinates = np.zeros((4,2))
# four corners of the mona lisa which will be transformed according to user input
monaLisaCoordinates = np.array([[250,500+cols],[250,500],[250+rows,500],[250+rows,500+cols]])
monaLisaCoordinates = np.flip(monaLisaCoordinates,1)

# this function takes the coordinates of the 4 corners to initialCoordinates
def draw_circle(event, x, y, flags, param):
    global count_click
    if event == cv2.EVENT_LBUTTONDOWN:
        if(count_click<4):
            initialCoordinates[count_click][:] = x, y
            count_click += 1
        print(x,y)

count_click = 0

while(True):
    # Capture frame-by-frame
    try:
        ret, frame = cap.read()
        # Our operations on the frame come here
        # finding the chessboard corners
        retval, corners	= cv2.findChessboardCorners(frame, patternSize)
        #print("The corners are \n", corners)
        if(count==0):
            cornersInit = corners
            cv2.namedWindow('frame')
            cv2.imshow('frame', frame)
            cv2.setMouseCallback('frame', draw_circle)
            # wait for user input
            # user needs to pick 4 corners to fit the augmented picture
            # the order of the four points should be in clockwise direction
            # and the corners should begin with the top left corner
            k = cv2.waitKey(20000)
            if k == ord('c'):         # wait for c key to continues
                H, mask = cv2.findHomography(monaLisaCoordinates, initialCoordinates, method=0)
                mona = cv2.warpPerspective(mona, H, out_shape)
                count += 1
                continue
            elif k == ord('q'):
                break

        if(count):
            H, mask = cv2.findHomography(cornersInit, corners, method=0)
            dst = cv2.warpPerspective(mona, H, out_shape)
            dst_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
            #dst = np.uint8(dst)
            frame[dst_gray>0,:] = 0
            overlay = np.uint8(frame + dst)
        else:
            overlay = np.uint8(mona)

        cornersPrevious = corners
        # Display the resulting frame
        cv2.imshow('frame', overlay)
        time.sleep(time_delay) # wait for 1 sec
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print("The error at frame " + str(count) + " occured")
        break

# When everything done, release the capture
print(initialCoordinates)
cap.release()
cv2.destroyAllWindows()
