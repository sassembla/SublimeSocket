import os

path = inputs["path"]
name = os.path.basename(path)

# input "body" = "a\nb\nc"
body = inputs["body"]

bodiesList = body.split("\n")

oncancelledContents = []

for bodyLine in bodiesList:
	itemDict = {}

	showAtMessageContents = {}
	showAtMessageContents["message"] = "this is " + bodyLine
	
	showAtMessageSelector = {}
	showAtMessageSelector["showAtLog"] = showAtMessageContents

	itemDict[bodyLine] = []
	itemDict[bodyLine].append(showAtMessageSelector)

	oncancelledContents.append(itemDict)

output({"onselected":oncancelledContents, "name":name})