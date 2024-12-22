from threading import Thread
from .tk_param import *
import time
from typing import Callable


class TKParamWindow:
    def __init__(self, title="参数面板"):
        self.root = None
        self.title = title
        self._mainloop_thread = None
        self._is_running: bool = False

        self._start_thread_loop()
        time.sleep(0.1)  # 留些时间用于tk初始化

    def _start_thread_loop(self):
        if self._is_running:
            return
        self._is_running = True
        self._mainloop_thread = Thread(target=self._creat_tk_thread)
        self._mainloop_thread.start()

    def _join_loop_thread(self):
        if self._mainloop_thread:
            return
        self._mainloop_thread.join()
        self._is_running = False

    def _creat_tk_thread(self):
        self.root = ttk.Window()
        self.root.title(self.title)
        self.root.mainloop()

    def quit(self):
        """
        quit the window and join the thread
        """
        self.root.quit()
        self._join_loop_thread()

    def get_scalar(self,
                   param_name: str,
                   default_value: float = None,
                   range_min: float = None,
                   range_max: float = None,
                   is_int: bool = False) \
            -> TkScalar:
        """
        get a scalar parameter from the window
        :param param_name: parameter name
        :param default_value: default value
        :param range_min: minimum value
        :param range_max: maximum value
        :param is_int: is integer or float
        :return: the scalar parameter, using TkScalar.get() to get the value
        """
        data_type = TKDataType.INT if is_int else TKDataType.FLOAT
        param = TK_PARAM_SCALAR_MAP[data_type](self.root, param_name, data_type, default_value, range_min, range_max)
        return param

    def get_button(self,
                   param_name: str,
                   default_value: bool = True,
                   on_change: Callable[[bool], None] = None) \
            -> TkBoolBtn:
        """
        get a button parameter from the window
        :param param_name: parameter name
        :param default_value: default value
        :param on_change: callback function when the button is clicked
        :return: the button parameter, using TkBoolBtn.get() to get the value
        """
        data_type = TKDataType.BOOL
        param = TK_PARAM_SCALAR_MAP[data_type](self.root, param_name, default_value, on_change)
        return param


# if __name__ == '__main__':
#
#     # 创建个tk窗口，窗口在线程中运行
#     # create a tkinter window running in a thread
#     window = TKParamWindow(title="example window")
#
#     # 定义窗口中需要调整的参数
#     # define parameters to be adjusted in the window
#     float_param = window.get_scalar("float param", default_value=2, range_min=-1.5, range_max=2.3)
#     int_param = window.get_scalar("int param", default_value=2.3, range_min=-10, range_max=10, is_int=True)
#     bool_button = window.get_button("button", default_value=False, on_change=lambda status: print(f"Button clicked: status: {status}"))
#
#     loop_duration = 10
#     print(f"The program will enter a loop for {loop_duration} seconds, you can adjust the parameters in GUI and see the printed real-time value")
#     end_time = time.time() + loop_duration
#
#     while True:
#         print(f"{float_param} | {int_param} | {bool_button}")
#         if time.time() > end_time:
#             break
#
#     # 退出窗口，自动结束线程
#     # quit the window and end the thread automatically
#     window.quit()
