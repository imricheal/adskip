import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QSpinBox,
    QComboBox, QGraphicsDropShadowEffect, QFrame
)
from PyQt5.QtCore import QTimer, Qt, QRectF
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPen, QBrush, QLinearGradient


class GradientProgressBar(QProgressBar):
    """渐变进度条"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(35)
        self._progress = 0
        self.setRange(0, 100)
        self.setValue(0)
        self.setTextVisible(False)

    def setProgress(self, value):
        self._progress = value
        self.setValue(int(value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        radius = 17

        # 背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(40, 50, 70))
        painter.drawRoundedRect(rect, radius, radius)

        # 渐变进度
        if self._progress > 0:
            w = int(rect.width() * self._progress / 100)
            progress_rect = QRectF(0, 0, w, rect.height())
            gradient = QLinearGradient(progress_rect.topLeft(), progress_rect.bottomRight())
            gradient.setColorAt(0, QColor(0, 212, 255))
            gradient.setColorAt(1, QColor(0, 150, 255))
            painter.setBrush(gradient)
            painter.drawRoundedRect(progress_rect, radius, radius)


class AdSkipWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_platform = "爱奇艺"
        self.duration = 15
        self.timer_interval = 80
        self.elapsed_ms = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

        self.init_ui()
        self.show_input_state()

    def init_ui(self):
        # 深色背景
        p = QPalette()
        p.setColor(QPalette.Window, QColor(18, 22, 38))
        p.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(p)

        self.setWindowTitle("广告跳过助手")
        self.setFixedSize(750, 950)
        self.set_center()

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(60, 50, 60, 50)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # ========== 标题区 ==========
        title = QLabel("广告跳过助手")
        title.setFont(QFont("Microsoft YaHei", 38, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #FFFFFF;")
        main_layout.addWidget(title)

        subtitle = QLabel("AD SKIP TOOL")
        subtitle.setFont(QFont("Consolas", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #00D4FF; letter-spacing: 6px; margin-bottom: 20px;")
        main_layout.addWidget(subtitle)

        # ========== 状态标签 ==========
        self.status_label = QLabel("● 准备就绪")
        self.status_label.setFont(QFont("Microsoft YaHei", 13))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            color: #00D4FF;
            background: transparent;
            padding: 8px 0;
        """)
        main_layout.addWidget(self.status_label)

        main_layout.addSpacing(20)

        # ========== 输入卡片 ==========
        input_card = QFrame()
        input_card.setStyleSheet("""
            QFrame {
                background-color: rgba(35, 45, 70, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
            }
        """)
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(35, 30, 35, 30)
        input_layout.setSpacing(30)
        input_card.setLayout(input_layout)

        # 平台选择行
        platform_row = QHBoxLayout()
        platform_row.setSpacing(15)

        platform_icon = QLabel("📺")
        platform_icon.setFont(QFont("", 20))

        platform_text = QLabel("选择平台")
        platform_text.setFont(QFont("Microsoft YaHei", 15, QFont.Medium))
        platform_text.setStyleSheet("color: #E0E6F0;")

        self.combo_platform = QComboBox()
        self.combo_platform.addItems(["爱奇艺", "腾讯视频", "优酷", "芒果TV", "B站"])
        self.combo_platform.setFixedHeight(48)
        self.combo_platform.setFont(QFont("Microsoft YaHei", 14))
        self.combo_platform.setStyleSheet("""
            QComboBox {
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 0 20px;
                color: #FFFFFF;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #00D4FF;
            }
            QComboBox:focus {
                border: 2px solid #00D4FF;
                background-color: rgba(0, 212, 255, 0.05);
            }
            QComboBox::drop-down {
                border: none;
                width: 40px;
            }
            QComboBox::down-arrow {
                border: none;
                width: 0;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1f35;
                border: 1px solid #00D4FF;
                selection-background-color: rgba(0, 212, 255, 0.2);
                color: #FFFFFF;
                padding: 10px;
                outline: none;
            }
        """)

        platform_row.addWidget(platform_icon)
        platform_row.addWidget(platform_text)
        platform_row.addStretch()
        platform_row.addWidget(self.combo_platform)
        input_layout.addLayout(platform_row)

        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: rgba(255,255,255,0.06); max-height: 1px;")
        input_layout.addWidget(separator)

        # 时长选择行
        duration_row = QHBoxLayout()
        duration_row.setSpacing(15)

        duration_icon = QLabel("⏱")
        duration_icon.setFont(QFont("", 20))

        duration_text = QLabel("广告时长")
        duration_text.setFont(QFont("Microsoft YaHei", 15, QFont.Medium))
        duration_text.setStyleSheet("color: #E0E6F0;")

        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(1, 300)
        self.spin_duration.setValue(15)
        self.spin_duration.setFixedHeight(48)
        self.spin_duration.setFont(QFont("Microsoft YaHei", 16))
        self.spin_duration.setStyleSheet("""
            QSpinBox {
                background-color: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 0 20px;
                color: #FFFFFF;
                min-width: 100px;
            }
            QSpinBox:hover {
                border-color: #00D4FF;
            }
            QSpinBox:focus {
                border: 2px solid #00D4FF;
                background-color: rgba(0, 212, 255, 0.05);
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 4px;
                width: 28px;
            }
            QSpinBox::up-button { margin-right: 2px; }
            QSpinBox::down-button { margin-right: 2px; margin-bottom: 2px; }
            QSpinBox::up-arrow {
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-bottom: 6px solid #888;
            }
            QSpinBox::down-arrow {
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #888;
            }
        """)

        duration_unit = QLabel("秒")
        duration_unit.setFont(QFont("Microsoft YaHei", 14))
        duration_unit.setStyleSheet("color: #8899AA;")

        duration_row.addWidget(duration_icon)
        duration_row.addWidget(duration_text)
        duration_row.addStretch()
        duration_row.addWidget(self.spin_duration)
        duration_row.addWidget(duration_unit)
        input_layout.addLayout(duration_row)

        main_layout.addWidget(input_card)

        main_layout.addSpacing(40)

        # ========== 主按钮 ==========
        self.btn_start = QPushButton("跳过广告")
        self.btn_start.setFixedSize(240, 55)
        self.btn_start.setFont(QFont("Microsoft YaHei", 17, QFont.Bold))
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0099FF, stop:1 #00DDFF);
                color: #FFFFFF;
                border-radius: 30px;
                border: none;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00AAFF, stop:1 #00EEFF);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0077CC, stop:1 #00BBCC);
            }
        """)

        # 发光阴影
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(25)
        glow.setColor(QColor(0, 150, 255, 80))
        glow.setOffset(0, 5)
        self.btn_start.setGraphicsEffect(glow)

        main_layout.addWidget(self.btn_start, alignment=Qt.AlignCenter)
        self.btn_start.clicked.connect(self.start_skip)

        main_layout.addSpacing(45)

        # ========== 进度显示区 ==========
        self.progress_widget = QWidget()
        self.progress_widget.setFixedHeight(280)
        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(25)
        progress_layout.setAlignment(Qt.AlignCenter)
        self.progress_widget.setLayout(progress_layout)

        # 长条进度条
        self.progress_bar = GradientProgressBar()
        self.progress_bar.setFixedSize(500, 35)
        progress_layout.addWidget(self.progress_bar)

        # 状态文字
        self.status_text = QLabel("正在连接服务器...")
        self.status_text.setFont(QFont("Microsoft YaHei", 17))
        self.status_text.setAlignment(Qt.AlignCenter)
        self.status_text.setStyleSheet("color: #FFFFFF; margin-top: 10px;")
        progress_layout.addWidget(self.status_text)

        # 剩余时间
        self.time_text = QLabel("预计剩余: 15 秒")
        self.time_text.setFont(QFont("Microsoft YaHei", 14))
        self.time_text.setAlignment(Qt.AlignCenter)
        self.time_text.setStyleSheet("color: #8899AA;")
        progress_layout.addWidget(self.time_text)

        main_layout.addWidget(self.progress_widget)

        # ========== 成功提示区 ==========
        self.success_widget = QWidget()
        self.success_widget.setFixedHeight(280)
        success_layout = QVBoxLayout()
        success_layout.setContentsMargins(0, 0, 0, 0)
        success_layout.setSpacing(20)
        success_layout.setAlignment(Qt.AlignCenter)
        self.success_widget.setLayout(success_layout)

        # 成功图标
        success_icon = QLabel("✅")
        success_icon.setFont(QFont("", 70))
        success_icon.setAlignment(Qt.AlignCenter)

        success_title = QLabel("广告跳过成功")
        success_title.setFont(QFont("Microsoft YaHei", 28, QFont.Bold))
        success_title.setAlignment(Qt.AlignCenter)
        success_title.setStyleSheet("color: #00FF88;")

        success_desc = QLabel("已成功绕过平台广告验证")
        success_desc.setFont(QFont("Microsoft YaHei", 15))
        success_desc.setAlignment(Qt.AlignCenter)
        success_desc.setStyleSheet("color: #8899AA;")

        success_layout.addWidget(success_icon)
        success_layout.addWidget(success_title)
        success_layout.addWidget(success_desc)

        main_layout.addWidget(self.success_widget)

        # 初始隐藏
        self.progress_widget.hide()
        self.success_widget.hide()

    def set_center(self):
        screen = QApplication.primaryScreen()
        sg = screen.geometry()
        wg = self.geometry()
        self.move((sg.width() - wg.width()) // 2, (sg.height() - wg.height()) // 2)

    def show_input_state(self):
        """输入状态"""
        self.status_label.setText("● 准备就绪")
        self.status_label.setStyleSheet("color: #00D4FF; background: transparent; padding: 8px 0;")
        self.btn_start.show()
        self.progress_widget.hide()
        self.success_widget.hide()

    def show_progress_state(self):
        """进度状态"""
        self.status_label.setText("◐ 跳过中...")
        self.status_label.setStyleSheet("color: #FFAA00; background: transparent; padding: 8px 0;")
        self.btn_start.hide()
        self.progress_widget.show()
        self.success_widget.hide()
        self.progress_bar.setProgress(0)
        self.status_text.setText("正在连接服务器...")
        self.time_text.setText(f"预计剩余: {self.duration} 秒")

    def show_success_state(self):
        """成功状态"""
        self.status_label.setText("✓ 跳过完成")
        self.status_label.setStyleSheet("color: #00FF88; background: transparent; padding: 8px 0;")
        self.progress_widget.hide()
        self.success_widget.show()

    def update_progress(self):
        """更新进度"""
        self.elapsed_ms += self.timer_interval
        progress = min(100, self.elapsed_ms / (self.duration * 1000) * 100)

        self.progress_bar.setProgress(progress)
        self.status_text.setText(self.get_status_text(progress))

        remaining = max(0, self.duration - self.elapsed_ms / 1000)
        self.time_text.setText(f"预计剩余: {remaining:.1f} 秒")

        if progress >= 100:
            self.timer.stop()
            self.show_success_state()
            QTimer.singleShot(2000, self.reset_to_initial_state)

    def get_status_text(self, p):
        """状态文字"""
        if p < 20:
            return "正在连接广告服务器..."
        elif p < 40:
            return "正在分析广告协议..."
        elif p < 60:
            return "正在破解加密算法..."
        elif p < 80:
            return "正在绕过广告验证..."
        elif p < 100:
            return "验证通过，准备跳过..."
        return "完成!"

    def reset_to_initial_state(self):
        self.timer.stop()
        self.elapsed_ms = 0
        self.show_input_state()

    def start_skip(self):
        self.current_platform = self.combo_platform.currentText()
        self.elapsed_ms = 0
        self.duration = self.spin_duration.value()
        self.show_progress_state()
        self.timer.start(self.timer_interval)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AdSkipWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
