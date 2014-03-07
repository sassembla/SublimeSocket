assert "selectedtitle" in inputs, "not included in:"+str(inputs)

selectedTitle = inputs["selectedtitle"]

output({"source":selectedTitle})