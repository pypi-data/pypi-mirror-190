# !/usr/bin/env python3
# coding=utf8
"""
omit
"""
import datetime
import logging
import os
import pathlib


class LogHelper(object):
    """
    我需要在一个系统里面打日志, 我不知道这个系统有没有用 logging,
    哪里用了 logging, 怎么初始化的 logging, 怎么使用的 logging,
    反正我准备用 logging 打日志, 所以我的操作不能影响系统里原有的 logging,
    于是有了这个类, 参考自: vnpy/vnpy/trader/engine.py 里的 LogEngine,
    """

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        """
        name 是 None 或 "root" 时, 初始化的是 RootLogger 吗?
        """
        self.name: str = name
        self.level: int = level

        # TODO: 检查 logging 里面是不是已经存在了这个 name
        self.logger: logging.Logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)

        self.formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s  %(levelname)s: %(message)s"
        )

        self.add_null_handler()

    def add_null_handler(self) -> None:
        """"""
        null_handler: logging.NullHandler = logging.NullHandler()
        self.logger.addHandler(null_handler)

    def add_console_handler(self) -> None:
        """"""
        console_handler: logging.StreamHandler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def add_file_handler(self, path=None, dir=None, file=None) -> None:
        """"""
        if path is None:
            if dir is None:
                dir: str = pathlib.Path(__file__).parent.as_posix()

            if file is None:
                dttm: str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file: str = f"{dttm}_{self.name}.log"

            path: str = pathlib.Path(dir).joinpath(file).as_posix()

        os.makedirs(name=pathlib.Path(path).parent.as_posix(), exist_ok=True)

        file_handler: logging.FileHandler = logging.FileHandler(
            filename=path, mode="a", encoding="utf8",
        )
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def debug(self, msg, *args, **kwargs):
        """"""
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """"""
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """"""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """"""
        self.logger.error(msg, *args, **kwargs)


if __name__ == "__main__":
    logh = LogHelper(name="test", level=logging.INFO)
    logh.add_console_handler()
    logh.add_file_handler()

    pai: float = 3.14
    num: int = 7

    logh.info("pai=%s, num=%s,", pai, num)  # 使用 logger 的格式化
    logh.info("pai={}, num={},".format(pai, num))  # 使用 format 函数
