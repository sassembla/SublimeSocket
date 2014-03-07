# toolTipを生成する
assert "path" in inputs and "crossed" in inputs, "not contained necessary parameters."+str(keys)

import os

path = inputs["path"]

name = os.path.basename(path)

crossed = inputs["crossed"]

# 試しに改行で分けてみる
lines = crossed.split("\n")

# create onselected
onselected = []

for line in lines:
	selectorContents = {"showAtLog":{"message":"here comes "+ line +" as a daredevil!!"}}

	selector = {}
	selector[line] = []
	selector[line].append(selectorContents)
	onselected.append(selector)

# create on cancelled
oncancelled = []
cancelSelector = {"showAtLog":{"message":"cancelled"}}
oncancelled.append(cancelSelector)

output({"name":name, "onselected":onselected, "oncancelled":oncancelled})