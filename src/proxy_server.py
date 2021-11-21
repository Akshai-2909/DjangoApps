import socket, sys, os, time


from cache import isCached, getCachedFile, putCacheFile, lruCache
from log import getTimeStamp
from _thread import start_new_thread 

path = "C:/Users/Samgeerh/Desktop/Cn-project/main/_cache/"

# Configuration for proxy 
config = {
	
	'max_connections': 5,
	'buffer': 8000,
	'PORT': 8080
}

# Socket to accept the client request

def socket_server():
	try:
		socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		socket_server.bind(('', config['PORT']))

		socket_server.listen(config['max_connections'])

		print(getTimeStamp()+"	Server has been initailized in port: 8080")
	
		while True:
			try:
				conn, addr = socket_server.accept()

				print(getTimeStamp()+"	Connection has been initailized...")

				start_new_thread(connection_resolving,(conn,addr))

			except Exception as e:
				print(getTimeStamp()+"	Cannot establish connection to the client")
				sys.exit(1)
		
	
	except Exception as e:
		print("Cannot able to create socket")
	
	finally:
		socket_server.close()

# Resolving the request to get the host,port,requested_file from the webserver

def connection_resolving(conn,addr):

	try:
		request = conn.recv(config['buffer'])
		header = request.split(b'\n')[0]

		requested_file = request
		requested_file = requested_file.split(b' ')
		requested_file = requested_file[1]
		method = request.split(b" ")[0]

   

		url = header.split(b' ')[1]


		hostIndex = url.find(b"://")
		if hostIndex == -1:
			temp = url 
		else:
			temp = url[(hostIndex + 3):]

		portIndex = temp.find(b":")

		serverIndex = temp.find(b"/")

		if serverIndex == -1:
			serverIndex = len(temp)
		webserver = ""
		port = -1

		if(portIndex == -1 or serverIndex < portIndex):
			port = 80
			webserver = temp[:serverIndex]
			proxy_server(webserver,port,conn,addr,request,requested_file)
		else:
			port = int((temp[portIndex + 1:])[:serverIndex - portIndex -1])
			webserver = temp[:portIndex]
			proxy_server(webserver,port,conn,addr,request,requested_file)
		print(f"The webserver is: {webserver}")

	except KeyboardInterrupt:
		sys.exit(1)

	except socket.gaierror as e:
		print(f"Error Occured due to: {e}")

# Proxy Server

def proxy_server(webserver,port,conn,addr,request,requested_file):
	
	requested_file = requested_file.replace(b".",b"_").replace( b"http://",b"_").replace(b"/",b"")

# Checking for the Cache hit in lrucache dict

	if isCached(str(requested_file)):
		print(isCached(str(requested_file)))
		print("Cache Hit......")
		cachedfile = getCachedFile(str(requested_file))
		print("The current state of Cache is" ,lruCache)
		response_object = open(path+cachedfile, 'rb')
		chunk = response_object.read(config['buffer'])

# Returning the cached response to the client 

		while len(chunk) > 0:
			conn.send(chunk)
			print("The data is : "+str(chunk))
			response_object.flush()
			chunk = response_object.read(config['buffer'])
		
		response_object.close()
		conn.close()

	else:
# Forwading the request to the webserver, if no cache hit
# Creating a copy of the response and save it in cache

		print("Forwarding the request to the webserver")
		proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		proxy.connect((webserver,port))
		proxy.sendall(request)
		
		cachefile = "cache_"+str(requested_file)
		putCacheFile(str(requested_file),cachefile)
		print("The current state of Cache is" ,lruCache)
		file = open(os.path.join(path,getCachedFile(str(requested_file))), 'wb')

		while True:

			data = proxy.recv(config["buffer"])
			if (len(data) > 0):
				file.write(data)
				file.flush()
				conn.send(data)
			else:
				break

		proxy.close()
		file.close()	

	conn.close()

# main

try:
	socket_server()
except KeyboardInterrupt:
	sys.exit(1)