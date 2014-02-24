import os

view = inputs["view"]
# but it's instance. cannot stringify.
view = "unmeasure"

path = inputs["path"]
basepath = os.path.basename(path)

message = "view:"+ view + ", path:" + str(basepath) + ", body:" + str(inputs["body"]) + ", rowcol:" + str(inputs["rowcol"]) + ", identity:" +  str(inputs["identity"])
output({"keys":str(keys), "message":message})