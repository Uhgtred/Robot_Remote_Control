#!/usr/bin/env python3
# @author: Markus Kösters

from .View import View
from .ViewConfig import ViewConfig


class ViewFactory:

    @staticmethod
    def produceView():
        config = ViewConfig('test', 2, 3)
        return View(config)
