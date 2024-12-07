Run clean.py and input document size to get desired dataset
Run getfile.py to retrieve texts from Perseus

Dataset has 2 front values:
1. 1 if plato, 0 if notplato, -1 if unknown
2. name of work
These are followed by the document of length n: the folder name is data_n

Ion and Xenocrates are put into validation
Crito and Isocrates Helen are put into test