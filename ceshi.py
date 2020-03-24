import requests
url='http://123.206.87.240:8002/web3/'
response=requests.get(url).text
print(response)