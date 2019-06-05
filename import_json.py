import json
import pandas as pd

data = []
with open('tweets.json') as f:
    for line in f:
        data.append(json.loads(json.dumps(line)))  # Converts the file data

for line in data:
    tweet = json.loads(data[line])
    df = pd.DataFrame(data=[tweet.text])
print(d['user'])
