import requests
import sys

url = input("Enter the url of the site: ")


proxies = {
	"http": "http://127.0.0.1:8080",
#     "https":"http://127.0.0.1:8080" 
}


try:
	response = requests.get(url, proxies=proxies)
	print("The response time is:"+str(response.elapsed))

except KeyboardInterrupt:
	sys.exit(1)

finally:
	print("Succefully fetched the content")



