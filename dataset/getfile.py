import requests
import os

# Download text from Perseus website

importURL = "https://scaife.perseus.org/reader/urn:cts:greekLit:tlg1799.tlg001.perseus-grc2:1-2"
importURL = importURL.replace("reader", "library/passage") + "/text/"

exportPath = "other/Euclid Elements 1-2"

if not os.path.exists(exportPath + ".txt") or os.path.getsize(exportPath + ".txt") == 0:
    response = requests.get(importURL)
    data = response.text
    print(len(data.split()))

    output = open(exportPath + ".txt", 'w', encoding='utf-8')
    output.write(data)
    output.close()

else:
    print("EXISTS")