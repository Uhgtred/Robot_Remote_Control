#!/usr/bin/env python3
# @author: Markus Kösters

from dataclasses import dataclass

from GUI import Models, Views


@dataclass
class GuiConfig:
    model: Models = Models.ModelFactory.produceModel()
    view: Views = Views.ViewFactory.produceView()
