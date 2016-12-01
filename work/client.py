import sys
import requests

if len(sys.argv) != 2:
    print('Specify an image file to detect face shape.')
    exit(1)

uploadfile = sys.argv[1]

data = open(uploadfile, 'rb').read()
res = requests.post(url='http://localhost:5000/detect', data=data)
print(res.text)
