import json
import matplotlib.pyplot as plt

f = open('gangham_labels.json')
data = json.load(f)

summary = []

for i in data['annotationResults'][0]['shotLabelAnnotations']:
    label = i['entity']['description']
    length = 0
    for j in i['segments']:
        start = j['segment']['startTimeOffset']
        end = j['segment']['endTimeOffset']
        duration = float(end[:-1]) - float(start[:-1])
        length += duration

    summary.append([label, round(length, 2)])
f.close()

summary = sorted(summary, key=lambda x:x[1], reverse=True)
summary = summary[:10]

labels = [i[0] for i in summary]
values = [i[1] for i in summary]

fig1, ax1 = plt.subplots()
ax1.pie(values, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=180)
fig1.suptitle('Top 10 subjects', fontsize=16)

plt.show()