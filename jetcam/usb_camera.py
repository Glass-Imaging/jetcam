from .camera import Camera
import atexit
import cv2
import numpy as np
import threading
import traitlets


class USBCamera(Camera):
    
    capture_fps = traitlets.Integer(default_value=30)
    capture_width = traitlets.Integer(default_value=640)
    capture_height = traitlets.Integer(default_value=480)   
    capture_device = traitlets.Integer(default_value=0)
    
    def __init__(self, *args, **kwargs):
        super(USBCamera, self).__init__(*args, **kwargs)

        print(f'Capture FPS :: {self.capture_fps} | capture_width :: {self.capture_width} | capture_height :: {self.capture_height} | capture_device :: {self.capture_device}')
        try:
            self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)

            re , image = self.cap.read()
            
            if not re:
                raise RuntimeError('Could not read image from camera.')
            
        except:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.cap.release)
                
    def _gst_str(self):
        # return 'v4l2src device=/dev/video{} ! video/x-raw, width=(int){}, height=(int){}, framerate=(fraction){}/1 ! videoconvert !  video/x-raw ! appsink'.format(self.capture_device, self.capture_width, self.capture_height, self.capture_fps)

        # return 'v4l2src device=/dev/video0 io-mode=2 ! image/jpeg, framerate=30/1, width=1920, height=1080 ! appsink'

        return 'v4l2src device=/dev/video0 io-mode=2 ! image/jpeg, framerate=30/1, width=1920, height=1080 ! nvjpegdec ! video/x-raw, format=(string)I420 ! nvvidconv flip-method=4 ! nvjpegenc ! appsink'

    
    def _read(self):
        re, image = self.cap.read()
        if re:
            # image_resized = cv2.resize(image,(int(self.width),int(self.height)))
            return image
        else:
            raise RuntimeError('Could not read image from camera')
