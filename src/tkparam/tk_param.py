from ttkbootstrap.constants import *
import ttkbootstrap as ttk
import tkinter as tk
from enum import Enum
from typing import Callable


class TKDataType(Enum):
    INT = 1,
    FLOAT = 2,
    BOOL = 3,


class TkParamBase:
    def __init__(self, root, param_name: str, data_type: TKDataType):
        self._root = root
        self._data_type = data_type

        self.name = param_name
        self.name_hash_id = hash(param_name)


class TkScalar(TkParamBase):
    DEFAULT_RANGE_MIN = 0
    DEFAULT_RANGE_MAX = 10
    DEFAULT_VALUE = DEFAULT_RANGE_MIN

    def __init__(self, root, param_name: str, data_type: TKDataType,
                 default_value: [int|float], r_min: [int|float], r_max: [int|float]):
        super().__init__(root, param_name, data_type)
        self.range_min = self.DEFAULT_RANGE_MIN if not r_min else r_min
        self.range_max = self.DEFAULT_RANGE_MAX if not r_max else r_max
        self.value: [int|float] = self.DEFAULT_VALUE if not default_value else default_value

        self.frame = ttk.Frame(self._root)
        self.frame.pack(side=TOP, fill=X)  # 从上往下排列

        self.label = ttk.Label(self.frame)
        self.label.pack(side=LEFT)  # label左对齐
        self._update_label_content()

        resolution = 1 if data_type is TKDataType.INT else 0.0001
        self.scalar = tk.Scale(self.frame, variable=self.value, from_=self.range_min, to=self.range_max,
                               command=self.on_change, orient=HORIZONTAL, resolution=resolution, showvalue=True)
        self.scalar.set(self.value)
        self.scalar.pack(side=RIGHT, fill=X, expand=True)

    def __str__(self):
        return f"{self.name}: {self.value}"

    def _update_label_content(self):
        self.label.config(text=f"{f'{self.name}【{self.value}】' :<30}")

    def get(self) -> int | float:
        return self.value

    def on_change(self, editor):
        self.value = self.scalar.get()
        self._update_label_content()

    def __add__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value + other_value

    def __sub__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value - other_value

    def __mul__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value * other_value

    def __truediv__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value / other_value

    def __floordiv__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value // other_value

    def __mod__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value % other_value

    def __pow__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value ** other_value

    def __eq__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value == other_value

    def __ne__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value != other_value

    def __lt__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value < other_value

    def __le__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value <= other_value

    def __gt__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value > other_value

    def __ge__(self, other):
        other_value = other.value if isinstance(other, TkScalar) else other
        return self.value >= other_value


class TkBoolBtn(TkParamBase):
    def __init__(self, root, param_name: str, default_value: bool, on_change_callback: Callable[[bool], None]):
        super().__init__(root, param_name, TKDataType.BOOL)
        self.value: bool = default_value
        self.on_change_callback: Callable[[bool], None] = on_change_callback

        self.btn = ttk.Button(self._root, text=param_name, command=self.on_change)
        self.btn.pack(fill=X, expand=True)
        self._update_btn_label()

    def __str__(self):
        return f"{self.name}: {self.value}"

    def _update_btn_label(self):
        btn_state = "开ON" if self.value else "关OFF"
        txt = f"{self.name}【status: {btn_state}】"
        self.btn.config(text=f"{txt: <45}")
        self.btn.config(style="success.TButton" if self.value else "secondary.Outline.TButton")

    def get(self) -> bool:
        return self.value

    def on_change(self):
        self.value = not self.value
        if self.on_change_callback is not None:
            self.on_change_callback(self.value)
        self._update_btn_label()


TK_PARAM_SCALAR_MAP = {
    TKDataType.INT: TkScalar,
    TKDataType.FLOAT: TkScalar,
    TKDataType.BOOL: TkBoolBtn,
}
