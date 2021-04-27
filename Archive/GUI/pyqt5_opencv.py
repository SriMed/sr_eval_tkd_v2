import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class video (QtWidgets.QDialog):
    def __init__(self):
        super(video, self).__init__()
        uic.loadUi('video.ui',self)
        self.startButton.clicked.connect(self.start_webcam)
        self.capture.clicked.connect(self.capture_image)
        self.imgLabel.setScaledContents(True)
        self.capture = None
        self.timer = QtCore.QTimer(self, interval=5)
        self.timer.timeout.connect(self.update_frame)
        self._image_counter = 0

    @QtCore.pyqtSlot()
    def get_video(self):
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.timer.start()

    @QtCore.pyqtSlot()
    def update_frame(self):
        ret, image=self.capture.read()
        simage = cv2.flip(image, 1)
        self.displayImage(image, True)

    @QtCore.pyqtSlot()
    def capture_image(self):
        flag, frame= self.capture.read()
        path = r'J:\Face'
        if flag:
            QtWidgets.QApplication.beep()
            name = "opencv_frame_{}.png".format(self._image_counter)
            cv2.imwrite(os.path.join(path, name), frame)
            self._image_counter += 1

    def displayImage(self, img, window=True):
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape)==3 :
            if img.shape[2]==4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888
        outImage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window:
            self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(outImage))

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = video()
    window.setWindowTitle('main code')
    window.show()
    sys.exit(app.exec_())