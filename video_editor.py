from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QSlider, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressBar 
from moviepy.editor import VideoFileClip
import sys

class TimeSelectionDialog(QDialog):
    def __init__(self, duration, parent=None):
        super(TimeSelectionDialog, self).__init__(parent)
        self.duration = duration
        self.start_time_slider = QSlider(Qt.Horizontal)
        self.end_time_slider = QSlider(Qt.Horizontal)
        self.start_time_label = QLabel()
        self.end_time_label = QLabel()
        self.clip_duration_label = QLabel()
        self.start_time_slider.setMaximum(int(duration))
        self.end_time_slider.setMaximum(int(duration))
        self.end_time_slider.setValue(int(duration))
        self.start_time_slider.valueChanged.connect(self.update_start_time_label)
        self.end_time_slider.valueChanged.connect(self.update_end_time_label)
        self.start_time_slider.valueChanged.connect(self.update_clip_duration_label)
        self.end_time_slider.valueChanged.connect(self.update_clip_duration_label)
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.progress_bar = QProgressBar(self)

        layout = QVBoxLayout()
        layout.addWidget(self.start_time_slider)
        layout.addWidget(self.start_time_label)
        layout.addWidget(self.end_time_slider)
        layout.addWidget(self.end_time_label)
        layout.addWidget(self.clip_duration_label)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        self.update_start_time_label()
        self.update_end_time_label()
        self.update_clip_duration_label()

    def seconds_to_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    def update_start_time_label(self):
        start_time = self.seconds_to_time(self.start_time_slider.value())
        self.start_time_label.setText(start_time)

    def update_end_time_label(self):
        end_time = self.seconds_to_time(self.end_time_slider.value())
        self.end_time_label.setText(end_time)

    def update_clip_duration_label(self):
        start_time = self.start_time_slider.value()
        end_time = self.end_time_slider.value()
        duration = end_time - start_time
        duration_str = self.seconds_to_time(duration)
        self.clip_duration_label.setText(duration_str)

    def get_start_time(self):
        return self.start_time_slider.value()

    def get_end_time(self):
        return self.end_time_slider.value()

def clip_video(video_path, start_time, end_time, output_path):
    # Open the video file
    video = VideoFileClip(video_path)

    # Clip the video
    clip = video.subclip(start_time, end_time)

    # Write the clip to a file
    clip.write_videofile(output_path, audio=True)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_path = QFileDialog.getOpenFileName()[0]  # Show the "Open" dialog box and return the path of the selected file
    video = VideoFileClip(video_path)
    dialog = TimeSelectionDialog(video.duration)
    if dialog.exec_() == QDialog.Accepted:
        start_time = dialog.get_start_time()
        end_time = dialog.get_end_time()
        output_path = QFileDialog.getSaveFileName()[0]  # Show the "Save As" dialog box and return the path of the selected file
        clip_video(video_path, start_time, end_time, output_path)