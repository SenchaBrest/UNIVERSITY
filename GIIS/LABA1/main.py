import sys
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QPushButton, QFileDialog, QGridLayout, QTabWidget, QSlider, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressBar
import numpy as np
import cv2


class ImageViewerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.file_name = None
        self.pixmap = None
        self.scaled_pixmap = None
        self.edit_im = None
        self.progress_bar = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('NOISE CANCELLER')
        self.setFixedSize(1000, 800)

        self.image_label1 = QLabel(self)
        self.image_label2 = QLabel(self)

        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)

        self.save_button = QPushButton('Save Image', self)
        self.save_button.clicked.connect(self.save_image)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.init_tab_widgets()

        layout = QGridLayout(self)
        layout.addWidget(self.image_label1, 0, 0, 1, 2)
        layout.addWidget(self.image_label2, 1, 0, 1, 2)
        layout.addWidget(self.load_button, 2, 0, 1, 1)
        layout.addWidget(self.save_button, 2, 1, 1, 1)
        layout.addWidget(self.tab_widget, 0, 2, 3, 1)
        layout.addWidget(self.progress_bar, 3, 0, 1, 5)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 1)

    def init_tab_widgets(self):
        self.tab_widget = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, 'Recover photo')
        self.tab_widget.addTab(self.tab1, 'Make noise photo')

        self.noise_slider = self.make_slider(Qt.Horizontal, 0, 10, 250, 20, self.noise_value_changed)
        self.noise_value = 0
        self.noise_slider_label = QLabel("Noise Level: " + str(self.noise_slider.value()))
        self.noise_slider_label.setAlignment(Qt.AlignCenter)

        self.noise_button = QPushButton('Make noise', self.tab1)
        self.noise_button.clicked.connect(self.make_noise)

        layout_tab1 = QGridLayout(self.tab1)
        layout_tab1.addWidget(self.noise_slider, 0, 1, Qt.AlignCenter)
        layout_tab1.addWidget(self.noise_slider_label, 0, 2)
        layout_tab1.addWidget(self.noise_button, 1, 0, 1, 3)
        self.tab1.setLayout(layout_tab1)

        self.x_slider_cross = self.make_slider(Qt.Horizontal, 0, 1, 250, 20, self.horizontal_slider_changed)
        self.x_value = 0
        self.x_slider_cross_label = QLabel("X Position: " + str(self.x_slider_cross.value()))
        self.x_slider_cross_label.setAlignment(Qt.AlignCenter)

        self.y_slider_cross = self.make_slider(Qt.Vertical, 0, 1, 20, 250, self.vertical_slider_changed)
        self.y_value = 0
        self.y_slider_cross.setInvertedAppearance(True)
        self.y_slider_cross_label = QLabel("Y Position: " + str(self.y_slider_cross.value()))
        self.y_slider_cross_label.setAlignment(Qt.AlignCenter)

        self.size_slider = self.make_slider(Qt.Horizontal, 1, 15, 250, 20, self.size_slider_changed)
        self.size_value = 3
        self.size_slider_label = QLabel("Size: " + str(3))
        self.size_slider_label.setAlignment(Qt.AlignCenter)

        self.recover_button = QPushButton('Recover', self.tab2)
        self.recover_button.clicked.connect(self.recover)

        layout_tab2 = QGridLayout(self.tab2)
        layout_tab2.addWidget(self.x_slider_cross, 0, 1, Qt.AlignCenter)
        layout_tab2.addWidget(self.x_slider_cross_label, 0, 2)
        layout_tab2.addWidget(self.y_slider_cross, 0, 1, Qt.AlignCenter)
        layout_tab2.addWidget(self.y_slider_cross_label, 1, 1, Qt.AlignCenter)
        layout_tab2.addWidget(self.size_slider, 2, 1, Qt.AlignCenter)
        layout_tab2.addWidget(self.size_slider_label, 2, 2)
        layout_tab2.addWidget(self.recover_button, 3, 0, 3, 3)  # Уменьшил пропорцию выделенного места для кнопки
        self.tab2.setLayout(layout_tab2)

    def make_slider(self, situation, min, max, x_size, y_size, function):
        slider = QSlider(situation)
        slider.setRange(min, max)
        slider.setSingleStep(1)
        slider.setFixedSize(x_size, y_size)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(1)
        slider.valueChanged.connect(function)
        return slider

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '',
                                                   'Image Files (*.png *.jpg *.jpeg);;All Files (*)',
                                                   options=options)
        if file_name:
            self.file_name = file_name
            self.pixmap = QPixmap(self.file_name)
            self.label_size = self.image_label1.size()
            self.scaled_pixmap = self.pixmap.scaled(self.label_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.image_label1.setPixmap(self.scaled_pixmap)
            self.image_label2.setPixmap(self.scaled_pixmap)

    def save_image(self):
        if self.file_name is not None:
            if self.edit_im is not None:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                file_name, _ = QFileDialog.getSaveFileName(self, 'Save Image', '',
                                                           'Image Files (*.png *.jpg *.jpeg);;All Files (*)',
                                                           options=options)
                self.edit_im.save(file_name)
            else:
                self.call_message_box("Error", "You haven't changed anything.", QMessageBox.Critical)
        else:
            self.call_message_box("Error", "Choose photo first.", QMessageBox.Critical)

    def noise_value_changed(self, value):
        self.noise_slider_label.setText("Noise Level: " + str(value))
        self.noise_value = value

    def make_noise(self):
        if self.file_name:
            edit_im = cv2.cvtColor(cv2.imread(self.file_name), cv2.COLOR_BGR2RGB)

            height, width, channels = edit_im.shape
            if (num_pixels_to_alter := round(self.noise_value / 100 * height * width)) == 0:
                self.image_label2.setPixmap(self.scaled_pixmap)
                return
            x_coordinates = np.random.randint(0, width - 1, num_pixels_to_alter)
            y_coordinates = np.random.randint(0, height - 1, num_pixels_to_alter)
            colors = np.random.randint(0, 255, (num_pixels_to_alter, 3), dtype=np.uint8)
            edit_im[y_coordinates, x_coordinates] = colors

            height, width, channels = edit_im.shape
            edit_im = QImage(edit_im, width, height, width * channels, QImage.Format_RGB888)

            self.edit_im = edit_im

            pixmap = QPixmap(edit_im).scaled(self.label_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.image_label2.setPixmap(pixmap)
        else:
            self.call_message_box("Error", "Choose photo first.", QMessageBox.Critical)

    def horizontal_slider_changed(self, value):
        self.x_slider_cross_label.setText("X Position: " + str(value))
        self.x_value = value

    def vertical_slider_changed(self, value):
        self.y_slider_cross_label.setText("Y Position: " + str(value))
        self.y_value = value

    def size_slider_changed(self, value):
        value = 2 * value + 1
        self.size_slider_label.setText("Size: " + str(value))
        self.y_slider_cross.setRange(0, value - 1)
        self.y_slider_cross.setValue(0)
        self.x_slider_cross.setRange(0, value - 1)
        self.x_slider_cross.setValue(0)
        self.size_value = value

    def recover(self):
        if self.file_name:
            self.toggle_buttons_state(False)
            self.progress_bar.setVisible(True)

            edit_im = cv2.cvtColor(cv2.imread(self.file_name), cv2.COLOR_BGR2RGB)
            height, width, channels = edit_im.shape
            num_of_iterations = height * width * channels

            size = self.size_value
            x = self.x_value
            y = self.y_value

            kernel = np.zeros((size, size))
            kernel[x, :], kernel[:, y] = 1, 1

            top_padding = y
            bottom_padding = size - y - 1
            left_padding = x
            right_padding = size - x - 1
            edit_im = np.pad(edit_im,
                             ((top_padding, bottom_padding), (left_padding, right_padding), (0, 0)), mode="constant")

            height, width, channels = edit_im.shape
            num_of_zeros = size ** 2 - 2 * size + 1
            median = int((size - 1) / 2 + 1)
            filter_im = np.zeros_like(edit_im, dtype=np.int8)

            k = 0
            for i in range(top_padding, height - bottom_padding):
                for j in range(left_padding, width - right_padding):
                    for c in range(channels):
                        filter_im[i, j, c] = np.sort(
                            (edit_im[i - top_padding:i + bottom_padding + 1, j - left_padding:j + right_padding + 1, c]
                             * kernel)
                            .flatten())[num_of_zeros:][median]

                        k += 1
                        progress_value = int(k / num_of_iterations * 100)
                        self.progress_bar.setValue(progress_value)
                        QApplication.processEvents()

            edit_im = filter_im[top_padding:height - bottom_padding, left_padding:width - right_padding, :]

            edit_im = edit_im.astype(np.uint8).copy()
            height, width, channels = edit_im.shape
            edit_im = QImage(edit_im, width, height, width * channels, QImage.Format_RGB888)

            self.edit_im = edit_im

            pixmap = QPixmap(edit_im).scaled(self.label_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.image_label2.setPixmap(pixmap)

            self.toggle_buttons_state(True)
            self.progress_bar.setVisible(False)
        else:
            self.call_message_box("Error", "Choose photo first.", QMessageBox.Critical)

    def toggle_buttons_state(self, state):
        self.load_button.setEnabled(state)
        self.save_button.setEnabled(state)
        self.noise_button.setEnabled(state)
        self.recover_button.setEnabled(state)

    def call_message_box(self, title, message, type_of_message):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.setIcon(type_of_message)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewerApp()
    window.show()
    sys.exit(app.exec())
