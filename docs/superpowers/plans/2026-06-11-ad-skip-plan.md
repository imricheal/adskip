# 广告跳过恶搞工具 - 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建广告跳过恶搞工具，运行后显示正经的假进度和倒计时，最后弹出"广告跳过成功"

**Architecture:** 单文件 PyQt5 应用，QTimer 控制倒计时和进度条同步，通过状态切换控制界面显示

**Tech Stack:** Python 3 + PyQt5

---

## 文件结构

- 创建: `C:/Users/GY163/PycharmProjects/tools/ad_skip.py`

---

## 实现步骤

### Task 1: 创建基础窗口和导入

**Files:**
- 创建: `C:/Users/GY163/PycharmProjects/tools/ad_skip.py`

- [ ] **Step 1: 创建基础文件结构和导入**

```python
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QSpinBox,
    QButtonGroup, QRadioButton
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPalette, QColor


class AdSkipWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("广告跳过助手")
        self.setFixedSize(500, 550)
        self.set_center()

    def set_center(self):
        screen = QApplication.primaryScreen()
        screen_geo = screen.geometry()
        window_geo = self.geometry()
        x = (screen_geo.width() - window_geo.width()) // 2
        y = (screen_geo.height() - window_geo.height()) // 2
        self.move(x, y)


def main():
    app = QApplication(sys.argv)
    window = AdSkipWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
```

- [ ] **Step 2: 运行测试窗口**

Run: `python ad_skip.py`
Expected: 500×550 白底窗口居中显示，标题"广告跳过助手"

---

### Task 2: 实现主界面布局

**Files:**
- 修改: `C:/Users/GY163/PycharmProjects/tools/ad_skip.py`

- [ ] **Step 1: 添加主布局和标题**

在 `init_ui` 方法中添加:
- 主垂直布局 main_layout，contentsMargins(30, 30, 30, 30)
- 顶部标题 "广告跳过助手"，字体 Microsoft YaHei 18号 Bold，居中，文字颜色 #333333
- 副标题 "一键跳过视频广告"，字体 12号，颜色 #666666，居中

- [ ] **Step 2: 添加平台选择区域**

在标题下方添加:
- 卡片容器 QVBoxLayout，背景 #F5F7FA，圆角 12px，内边距 20px
- 卡片内标签 "选择广告所在平台"，居左，字体 14号 Bold，颜色 #333333
- 平台按钮行 QHBoxLayout，5个 QRadioButton 横向排列居中
  - 爱奇艺、腾讯视频、优酷、芒果TV、B站
  - 默认选中第一个（爱奇艺）
  - 按钮样式: 白底 #FFFFFF，边框 #E8E8E8，圆角 8px

- [ ] **Step 3: 添加时长输入区域**

在平台选择下方添加:
- 卡片容器同上样式
- 标签 "广告时长（秒）"
- QSpinBox，范围 1-300，默认 15，宽度 120px

- [ ] **Step 4: 添加主按钮**

在时长输入下方添加:
- QPushButton "开始跳过广告"
- 尺寸 200×50，圆角 25px（胶囊形）
- 背景色 #1890FF，白色文字 16号 Bold
- 居中显示

- [ ] **Step 5: 运行验证**

Run: `python ad_skip.py`
Expected: 窗口包含标题、平台选择（5个单选按钮）、时长输入、蓝色主按钮

---

### Task 3: 实现进度显示区域

**Files:**
- 修改: `C:/Users/GY163/PycharmProjects/tools/ad_skip.py`

- [ ] **Step 1: 添加进度区域容器**

在主布局底部添加 QVBoxLayout:
- 初始状态 hide()
- 包含:
  - 分隔线 QLabel("───────────────")，颜色 #E8E8E8
  - 进度条 QProgressBar，高度 24px，圆角 12px，背景 #E8E8E8，填充 #1890FF
  - 百分比标签 QLabel("0%")，居中，14号
  - 状态文字 QLabel("正在获取平台广告接口...")，居中，14号，颜色 #333333
  - 剩余时间 QLabel("剩余: 15.00 秒"，居中，14号，颜色 #666666

- [ ] **Step 2: 添加成功提示气泡**

在进度区域下方添加 QLabel:
- 文本 "✅ 广告已成功跳过！"
- 背景 #D4EDDA（浅绿），边框 #C3E6CB，圆角 8px，内边距 15px
- 字体 16号 Bold，颜色 #155724
- 初始 hide()

- [ ] **Step 3: 运行验证**

Run: `python ad_skip.py`
Expected: 进度区域和成功提示初始隐藏

---

### Task 4: 实现状态切换逻辑

**Files:**
- 修改: `C:/Users/GY163/PycharmProjects/tools/ad_skip.py`

- [ ] **Step 1: 添加状态存储属性**

在 `__init__` 后添加属性:
```python
self.current_platform = "爱奇艺"  # 当前选中的平台
self.duration = 15  # 广告时长（秒）
self.timer_interval = 100  # 定时器间隔（毫秒）
self.elapsed_ms = 0  # 已过去的时间（毫秒）
```

- [ ] **Step 2: 实现状态切换方法**

添加以下方法:

```python
def show_input_state(self):
    """显示输入区域，隐藏进度区域"""
    # 显示平台选择、时长输入、主按钮
    # 隐藏进度条区域和成功提示
    pass

def show_progress_state(self):
    """显示进度区域，隐藏输入区域"""
    # 隐藏平台选择、时长输入
    # 显示进度条区域
    # 隐藏成功提示
    # 重置进度条为 0
    pass

def show_success_state(self):
    """显示成功状态"""
    # 隐藏进度条
    # 显示成功提示气泡
    pass
```

- [ ] **Step 3: 绑定主按钮点击事件**

在主按钮创建后添加:
```python
self.start_btn.clicked.connect(self.start_skip)
```

- [ ] **Step 4: 实现 start_skip 方法**

```python
def start_skip(self):
    """开始跳过广告流程"""
    # 获取选中的平台和时长
    # 调用 show_progress_state()
    # 启动定时器
    pass
```

- [ ] **Step 5: 运行验证**

Run: `python ad_skip.py` → 点击主按钮
Expected: 输入区域消失，进度区域显示

---

### Task 5: 实现倒计时和进度同步

**Files:**
- 修改: `C:/Users/GY163/PycharmProjects/tools/ad_skip.py`

- [ ] **Step 1: 添加 QTimer 初始化**

在 `__init__` 中添加:
```python
self.timer = QTimer()
self.timer.timeout.connect(self.update_progress)
```

- [ ] **Step 2: 实现 update_progress 方法**

```python
def update_progress(self):
    """更新进度条和倒计时"""
    # 增加已过去的时间 (self.elapsed_ms += self.timer_interval)
    # 计算进度百分比 (progress = elapsed_ms / (duration * 1000) * 100)
    # 更新进度条值
    # 更新百分比文字
    # 更新剩余时间文字
    # 更新状态文字（根据进度阶段）
    #
    # 如果进度 >= 100:
    #     停止定时器
    #     调用 show_success_state()
    #     启动恢复定时器 (2秒后调用 show_input_state)
```

- [ ] **Step 3: 完善 start_skip 方法**

```python
def start_skip(self):
    # 获取用户选择的时长
    self.duration = self.duration_input.value()
    # 重置已过去时间
    self.elapsed_ms = 0
    # 切换到进度状态
    self.show_progress_state()
    # 启动定时器
    self.timer.start(self.timer_interval)
```

- [ ] **Step 4: 完善状态文字分阶段**

```python
def get_status_text(self, progress):
    """根据进度返回状态文字"""
    if progress < 30:
        return "正在获取平台广告接口..."
    elif progress < 60:
        return "正在破解广告加密算法..."
    elif progress < 90:
        return "正在绕过广告验证..."
    else:
        return "广告跳过成功！"
```

- [ ] **Step 5: 实现恢复逻辑**

```python
def reset_to_initial_state(self):
    """恢复到初始状态"""
    self.timer.stop()
    self.elapsed_ms = 0
    self.show_input_state()
```

- [ ] **Step 6: 运行验证**

Run: `python ad_skip.py` → 选择平台 → 填时长 5秒 → 点击开始
Expected:
- 进度条从 0% 到 100% 线性增长
- 倒计时同步显示剩余时间
- 状态文字分4个阶段变化
- 完成后显示成功气泡
- 2秒后自动恢复

---

### Task 6: 完善细节和样式

**Files:**
- 修改: `C:/Users/GY163/PycharmProjects/tools/ad_skip.py`

- [ ] **Step 1: 设置窗口背景色**

在 `init_ui` 开头添加:
```python
palette = QPalette()
palette.setColor(QPalette.Window, QColor(255, 255, 255))
self.setPalette(palette)
```

- [ ] **Step 2: 优化按钮样式**

平台按钮样式（默认）:
```python
"""
QRadioButton {
    background-color: #FFFFFF;
    border: 1px solid #E8E8E8;
    border-radius: 8px;
    padding: 10px 20px;
    color: #666666;
}
QRadioButton:checked {
    border: 2px solid #1890FF;
    color: #1890FF;
    background-color: #E6F7FF;
}
"""
```

主按钮悬停效果:
```python
self.start_btn.setStyleSheet("""
    QPushButton {
        background-color: #1890FF;
        color: white;
        border-radius: 25px;
        border: none;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #40A9FF;
    }
    QPushButton:pressed {
        background-color: #096DD9;
    }
    QPushButton:disabled {
        background-color: #CCCCCC;
    }
""")
```

- [ ] **Step 3: 平台按钮组设置**

在创建按钮后添加:
```python
self.platform_group = QButtonGroup()
self.platform_group.addButton(self.btn_iqy, 0)
self.platform_group.addButton(self.btn_tx, 1)
# ... 添加其他按钮
self.platform_group.buttonClicked.connect(self.on_platform_selected)
```

- [ ] **Step 4: 运行时验证所有功能**

Run: `python ad_skip.py`
Expected:
- 白色背景窗口
- 平台按钮可选中，选中时蓝色边框+蓝字
- 输入时长可用
- 点击主按钮后正确切换状态
- 进度条和倒计时同步
- 成功气泡显示
- 2秒后恢复

---

### Task 7: 最终测试

**Files:**
- 测试: `C:/Users/GY163/PycharmProjects/tools/ad_skip.py`

- [ ] **测试1: 基本功能**

Run: `python ad_skip.py`
- [ ] 窗口居中显示
- [ ] 5个平台按钮正常单选
- [ ] 时长输入默认15，可调
- [ ] 点击按钮后输入区隐藏，进度区显示

- [ ] **测试2: 倒计时准确性**

设置时长 5秒，观察:
- [ ] 倒计时从 5.00 到 0.00
- [ ] 进度条同步从 0% 到 100%
- [ ] 状态文字4个阶段变化

- [ ] **测试3: 完成流程**

- [ ] 完成后显示成功气泡
- [ ] 2秒后自动恢复初始状态
- [ ] 可以再次使用

- [ ] **测试4: 边界情况**

- [ ] 时长设为 1秒能正常工作
- [ ] 时长设为 300秒能正常工作
- [ ] 快速重复点击不会出问题

---

## 验收标准回顾

- [x] 窗口启动居中显示
- [x] 5个平台按钮单选有效
- [x] 时长输入默认15秒，范围1-300秒
- [x] 点击主按钮后输入区域隐藏，进度区域显示
- [x] 进度条与倒计时同步（0% → 100%）
- [x] 状态文字分4个阶段变化
- [x] 倒计时结束后显示成功气泡
- [x] 2秒后自动恢复到初始状态
- [x] 可以重复使用
