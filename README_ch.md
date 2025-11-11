# tkparam

tkparam提供了一种简单的方法使用tkinter的GUI面板中来动态调整参数，方便在循环程序中调整参数.

## 安装


使用pip：


```bash
pip install tkparam
```

## 用例

```python
import tkparam
import time

# 创建个tk窗口，窗口在线程中运行
window = TKParamWindow(title="example window")

# 定义窗口中需要调整的参数
float_param = window.get_scalar("float param", default_value=2, range_min=-1.5, range_max=2.3)
int_param = window.get_scalar("int param", default_value=2.3, range_min=-10, range_max=10, is_int=True)
bool_button = window.button_bool("button", default_value=False,
                                 on_change=lambda status: print(f"Button clicked: status: {status}"))

loop_duration = 10
print(
    f"The program will enter a loop for {loop_duration} seconds, you can adjust the parameters in GUI and see the printed real-time value")
end_time = time.time() + loop_duration

while True:
    print(f"{float_param} | {int_param} | {bool_button}")
    if time.time() > end_time:
        break

# 退出窗口，自动结束线程
window.quit()
```