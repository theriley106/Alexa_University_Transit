import json

a = json.load(open('agencyInfo.json'))["agencies"]
text = ""
allList = []
for v in a:
	val = v["short_name"].strip().lower()
	if val not in allList:
		allList.append(val)
		text += '''{"name": {"value": "$VAL"}},'''.replace("$VAL", val)
	val = v["long_name"].strip().lower()
	if val not in allList:
		allList.append(val)
		text += '''{"name": {"value": "$VAL"}},'''.replace("$VAL", val)
	val = v["name"].strip().lower()
	if val not in allList:
		allList.append(val)
		text += '''{"name": {"value": "$VAL"}},'''.replace("$VAL", val)

print text
