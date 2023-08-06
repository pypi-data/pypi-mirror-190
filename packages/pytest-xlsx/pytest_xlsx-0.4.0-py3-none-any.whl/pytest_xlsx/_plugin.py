from abc import ABCMeta, abstractmethod

import allure
import pytest

from pytest_xlsx.file import XlsxItem
from pytest_xlsx.runner import Runner


class XlsxPlugin(metaclass=ABCMeta):
    def __init__(self, config: pytest.Config):
        self.config = config

    @abstractmethod
    def pytest_xlsx_execute_step(self, item: XlsxItem, xlsx_runner: Runner):
        ...


class CallRuner(XlsxPlugin):
    def pytest_xlsx_execute_step(self, item: XlsxItem, xlsx_runner: Runner):
        xlsx_runner.execute(item)


class Allure(XlsxPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta_column_name = self.config.getini("xlsx_meta_column_name")

    @pytest.hookimpl(tryfirst=True)
    def pytest_xlsx_execute_step(self, item: XlsxItem, xlsx_runner: Runner):

        if self.meta_column_name not in item.current_step:
            return

        keys = list(item.current_step)
        arg_column_index = keys.index(self.meta_column_name) + 1
        if len(keys) <= arg_column_index:
            return None
        else:
            arg_column_name = keys[arg_column_index]

        mark = str(item.current_step.get(self.meta_column_name, ""))
        value = str(item.current_step.get(arg_column_name, ""))

        if not mark.startswith("allure"):
            return None
        if not value:
            return None

        label = mark.split("_")[-1]

        if label == "step":
            with allure.step(value):
                ...
        else:
            f = getattr(allure.dynamic, label)
            f(value)

        return True
