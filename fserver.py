#Revathy Ramamoorthy
#https://pymotw.com/2/socket/tcp.html
#https://www.youtube.com/watch?v=SepyXsvWVfo
#http://effbot.org/tkinterbook/label.htm
import socket
import threading
from tkinter import *
import select
import time


client_num = {}		#Dictionary to store connected clients and their socket details
message=''
a={}				#Dictionary to store users and their port numbers

#server gui
def gui():
    win = Tk()
    win.geometry('500x500')
    print("GUI started")
    global b
    b = Label(win, text="Server GUI", fg="blue", font=("Helvetica", 16))  	#Label to display message
    button = Button(win, text='close', width=30, command=win.quit())		#To close the connection
    b.pack()
    button.pack()
    win.mainloop()


def server_connection():
	while(1):
		try:
			connection, client_address=server.accept()		#Accepting the client
			print(client_address[1])						#Displaying client port number
			data1 = connection.recv(1024).decode('utf8')	#Registration with username
			source_client = str(data1)
			print('Source_client:'+source_client)			
			client_num[source_client] = connection          #Storing client details
			a[source_client]=client_address[1]
			print(client_num)
			print(a)
			threading.Thread(target=server_send, args=(connection, address)).start()  #thread to handle receiving and sending messages
		except select.error:  #error handling
			print("error")
			server.close()

def server_send(connection,address):
	while(1):
		try:
			data2 = connection.recv(1024).decode('utf8')	#Receiving username from client
			message= str(data2)
			print("recieved")
			data4 = connection.recv(1024).decode('utf-8')	#Receiving message from client
			delivery_preference = str(data4)
			print('Destination_client:'+delivery_preference)
			if(message!="no"):
				final_message = ''
				date = ''
				date = time.strftime("%a, %d %b %Y %H:%M:%S")	#function to current calcualte date and time
				final_message = 'HTTP/1.1 200 OK\n'+date+'\nContent-Type: test/xml; charset="utf-8"\nhost: 127.0.0.1:5000\nUser-Agent:Socket-Client\n'+ str(message)
				b['text']=b['text']+'\n'+final_message		#displaying message in HTTP format
				print('Message:\n'+message)
				data5=connection.recv(1024).decode('utf-8')
				if delivery_preference=="all":				#one to many message delivery
					message1="\nThis is a 1-n"
					message2=message1 + message + data5
					for sock in client_num:
						print(client_num[sock])
						client_num[sock].send(message2.encode('utf-8'))
						print("sent")
				else:
					message1="\nThis is a 1-1"				#one to one message delivery
					message2=message1 +'\n'+ message +'\n'+ data5
					for sock in client_num:
						if sock==delivery_preference:
							client_num[sock].send(message2.encode('utf-8'))
							print("sent")
			else:
				if sock==delivery_preference:
					client_num[sock].close()
		except select.error:	#exception handling
			print("error")
			server.close()




if __name__ == '__main__':
	serverIP = '127.0.0.1'
	port = 5000
	address = (serverIP, port)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(address)
	server.listen(3)
	print("listening")
	threading.Thread(target=server_connection).start()
	gui()