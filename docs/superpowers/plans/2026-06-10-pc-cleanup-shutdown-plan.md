# 电脑内存清理（整蛊版）- 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal：** 用 PyQt5 实现一个整蛊桌面程序，点击"立即清理"后显示假进度条，完成后弹出倒计时警告，3秒后自动关机

**Architecture：** 单文件 Python 程序 + PyQt5 GUI + Windows shutdown 命令打包成单文件 EXE

**Tech Stack：** Python 3.x, PyQt5, PyInstaller

---

## 文件结构

```
C:\Users\GY163\PycharmProjects\tools\
  cleanup.py              # 主程序（单文件）
  docs/
    superpowers/
      specs/
        2026-06-10-pc-cleanup-shutdown-design.md  # 设计文档
      plans/
        2026-06-10-pc-cleanup-shutdown-plan.md    # 本计划
```

---

## Task 1: 创建主程序 cleanup.py

**Files:**
- Create: `C:\Users\GY163\PycharmProjects\tools\cleanup.py`

- [ ] **Step 1: 创建主程序文件**

```python
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
        self.setWindowTitle("电脑内存清理")
        self.setFixedSize(400, 300)
        self.set_center()

        # 设置深蓝色科技感调色板
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(20, 30, 50))
        self.setPalette(palette)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # 标题
        self.title_label = QLabel("电脑内存清理")
        title_font = QFont("Microsoft YaHei", 20, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #00d4ff; background: transparent;")

        # 副标题
        self.subtitle_label = QLabel("一键清理系统垃圾，释放内存空间")
        subtitle_font = QFont("Microsoft YaHei", 10)
        self.subtitle_label.setFont(subtitle_font)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("color: #888888; background: transparent;")

        # 清理按钮
        self.clean_btn = QPushButton("立即清理")
        self.clean_btn.setFixedSize(160, 50)
        btn_font = QFont("Microsoft YaHei", 14, QFont.Bold)
        self.clean_btn.setFont(btn_font)
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                border-radius: 8px;
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
        self.progress_bar.setFixedHeight(25)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00d4ff;
                border-radius: 8px;
                background-color: #1a1a2e;
                text-align: center;
                color: #00d4ff;
            }
            QProgressBar::chunk {
                background-color: #00d4ff;
                border-radius: 6px;
            }
        """)
        self.progress_bar.hide()

        # 状态文字（初始隐藏）
        self.status_label = QLabel()
        self.status_label.setFont(QFont("Microsoft YaHei", 10))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #ffffff; background: transparent;")
        self.status_label.hide()

        # 阶段一布局（按钮）
        self.stage1_layout = QVBoxLayout()
        self.stage1_layout.setAlignment(Qt.AlignCenter)
        self.stage1_layout.addWidget(self.title_label)
        self.stage1_layout.addWidget(self.subtitle_label)
        self.stage1_layout.addSpacing(20)
        self.stage1_layout.addWidget(self.clean_btn)

        # 阶段二布局（进度条）
        self.stage2_layout = QVBoxLayout()
        self.stage2_layout.setAlignment(Qt.AlignCenter)
        self.stage2_layout.addWidget(self.progress_bar)
        self.stage2_layout.addWidget(self.status_label)

        # 主容器
        self.container_layout = QVBoxLayout()
        self.container_layout.setAlignment(Qt.AlignCenter)
        self.container_layout.addLayout(self.stage1_layout)

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
        self.warning_window.setText("<font size='5' color='red'><b>三秒后关机</b></font>")
        self.warning_window.setStandardButtons(QMessageBox.NoButton)
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
            self.warning_window.setText("<font size='5' color='red'><b>二秒后关机</b></font>")
        elif self.countdown_value == 1:
            self.warning_window.setText("<font size='5' color='red'><b>一秒后关机</b></font>")
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
```

---

## Task 2: 安装依赖

**Files:**
- Modify: 无

- [ ] **Step 1: 安装 PyQt5**

运行：`pip install PyQt5`
预期：Successfully installed PyQt5

- [ ] **Step 2: 安装 PyInstaller**

运行：`pip install pyinstaller`
预期：Successfully installed pyinstaller

---

## Task 3: 测试运行程序

**Files:**
- Test: `C:\Users\GY163\PycharmProjects\tools\cleanup.py`

- [ ] **Step 1: 运行程序测试界面**

运行：`python cleanup.py`
预期：窗口正常打开，显示"电脑内存清理"标题和"立即清理"按钮

- [ ] **Step 2: 测试点击按钮**

操作：点击"立即清理"
预期：进度条出现并跑动，文字按阶段切换

- [ ] **Step 3: 关闭程序（不等待关机）**

操作：手动关闭窗口

---

## Task 4: 打包成 EXE

**Files:**
- Create: `C:\Users\GY163\PycharmProjects\tools\dist\cleanup.exe`

- [ ] **Step 1: 使用 PyInstaller 打包**

运行：`pyinstaller --onefile --noconsole --name cleanup cleanup.py`
预期：生成 `dist/cleanup.exe`

- [ ] **Step 2: 验证 EXE 文件存在**

运行：`ls -la dist/cleanup.exe`
预期：文件存在

---

## Task 5: 最终验证

**Files:**
- Test: `dist\cleanup.exe`

- [ ] **Step 1: 双击 EXE 测试**

操作：直接双击运行 EXE
预期：窗口正常打开，无 CMD 黑窗口

- [ ] **Step 2: 验证所有交互**

操作：点击按钮 → 等待进度条完成 → 观察倒计时弹窗
预期：符合设计文档流程

---

## 依赖清单

| 包名 | 版本 | 用途 |
|------|------|------|
| PyQt5 | 最新 | GUI 界面 |
| PyInstaller | 最新 | 打包 EXE |

## 验收标准

1. 双击 EXE 打开窗口，标题显示"电脑内存清理"
2. 窗口居中，有"立即清理"大按钮
3. 点击按钮后显示进度条（蓝色）
4. 进度条 0-30% 显示"AI大模型正在分析系统垃圾文件"
5. 进度条 30-70% 显示"AI大模型正在分析多余应用"
6. 进度条 70-100% 显示"生成清理方案"
7. 进度完成后弹出警告弹窗，文字切换：三秒 → 二秒 → 一秒 → 关机
8. 关机命令正确执行（`shutdown /s /t 0`）
