#Revathy Ramamoorthy
#https://realpython.com/python-sockets/
#https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
#https://www.geeksforgeeks.org/socket-programming-python/
#https://stackabuse.com/basic-socket-programming-in-python/
#https://www.youtube.com/watch?v=SepyXsvWVfo
#https://stackoverflow.com/questions/2905965/creating-threads-in-python
#https://stackoverflow.com/questions/7585435/best-way-to-convert-string-to-bytes-in-python-3
#https://www.tutorialspoint.com/python/python_gui_programming.htm
#http://effbot.org/tkinterbook/label.htm
import socket
import threading
from tkinter import *
import select

#client gui
def gui():
    win = Tk()
    win.geometry('200x400')
    print("GUI started")
    global b
    b = Label(win, text="Client GUI", fg="blue", font=("Helvetica", 16)) #Label to display message
    button = Button(win, text='close', width=30, command=win.quit())	 #To close the connection
    b.pack()
    button.pack()
    win.mainloop()


def client_connection():
	try:
		host = '127.0.0.1'
		port = 5000
		global client
		client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Client socket creation
		client.connect((host,port))      #Connection
		print("connected")
		s_name = input("Enter UserName")
		sc_name=s_name
		client.send(s_name.encode('utf8'))		#Sending username - Registration
		while (1):
			a=input("press 1 to send 2 to receive ")
			if(a=="1") :
				message = input("Enter the message") #Getting message from source client
				client.send(message.encode('utf-8'))	#Sending message
				choice = ''
				choice = input("Message delivery preference : 1. ONE TO ONE enter the client name  or 2. ONE TO MANY") #Getting preference
				if choice != "all":
					client.send(choice.encode('utf-8')) #Sending preference to server
				else:
					client.send(choice.encode('utf-8'))
				print("Message sent successfully")
				client.send(sc_name.encode('utf-8'))
				
			elif(a=="2"):
				print("enter the recieved")
				recv_message=client.recv(1024).decode() #Receiving message
				print(recv_message)
				b['text']=b['text']+'\n'+recv_message	#Displaying message on GUI
			else:
				print("enter the corect choice")
				continue
			ans = input('\nDo you want to continue(y/n) :') 
			if (ans == 'y'):
				continue
			else:
				sd="no"
				client.send(sd.encode('utf-8'))
				client.send(sc_name.encode('utf-8'))
				break
	except select.error:	#error handling
		print("error")
		client.close()

if __name__ == '__main__':
	threading.Thread(target=client_connection).start() #Starting thread
	gui()

