import time
import signal
import cv2
import threading
from JetsonCamera import Camera
from Focuser import Focuser
from Autofocus import FocusState, doFocus

exit_ = False
def sigint_handler(signum, frame):
    global exit_
    exit_ = True

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

if __name__ == "__main__":
	camera = Camera()
	focuser = Focuser(7)

	focusState = FocusState()
	# focusState.verbose = True
	doFocus(camera, focuser, focusState)

	start = time.time()
	frame_count = 0

	while not exit_:
		frame = camera.getFrame(2000)

		cv2.imshow("Test", frame)
		key = cv2.waitKey(1)
		if key == ord('q'):
			exit_ = True
		if key == ord('f'):
			if focusState.isFinish():
				focusState.reset()
				doFocus(camera, focuser, focusState)
			else:
				print("Focus is not done yet.")

		frame_count += 1
		if time.time() - start >= 1:
			print("{}fps".format(frame_count))
			start = time.time()
			frame_count = 0

	camera.close()