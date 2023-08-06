#!/usr/bin/env python3
import pyenerginetpowerrightnow
import json

data = pyenerginetpowerrightnow.getCurrentData()

print(json.dumps(data))

