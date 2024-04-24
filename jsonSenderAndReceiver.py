import json
import socket
import multiprocessing
import time


class MessageManager:
    process = False

    def __init__(self, my_port):
        self.client_socket = None
        self.server_socket = None
        # item in buffer is like that : { sensor_id : [ [ list of status ] , { dict tree } ] , . . . }
        self.general_buffer = {}
        self.my_port = my_port
        multiprocessing.Process(target=self.start_receiving, args=(my_port,)).start()

    def sending_message(self, message, host, port):
        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # client_socket.bind((host , sel))
                client_socket.connect((host, port))
                client_socket.send(json.dumps(message).encode())
                client_socket.close()
                break
            except ConnectionRefusedError:
                print("Connection refused. Retrying in 1 second...")
                time.sleep(1)

    def receive_message(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        while True:
            conn, addr = server_socket.accept()
            print(f"Got connection from {addr}")
            json_data = conn.recv(2048).decode()
            message = json.loads(json_data)
            if not message:
                continue  # Skip empty messages
            # print(f"Received message from client: {message}")
            self.general_buffer.update(message)
            conn.close()
        #
        # while True:
        #     print(f"Got connection from {addr}")
        #     message = conn.recv(1024).decode()
        #     if not message:
        #         break
        #     print(f"Received message from client: {message}")
        # conn.close()

    def start_receiving(self, my_port):
        message = MessageManager(my_port)
        message.receive_message(socket.gethostname(), my_port)

    def get_buffer(self):
        return self.general_buffer.popitem()
    # def create_process(self, port):
    #     if not self.process:
    #         multiprocessing.Process(target=self.start_receiving, args=(port,)).start()
    #         self.process = True


# if __name__ == '__main__':
#     message1 = MessageManager(19000)
#     # proces1 = multiprocessing.Process(target=message1.start_receiving, args=(8000,))
#     # proces1.start()
#     # message2 = MessageManager(19001)
#     message1.sending_message({1: "heelo"}, socket.gethostname(), 19000)
#     message1.sending_message({1: "heelooooo"}, socket.gethostname(), 19000)
#     time.sleep(3)
#     message1.sending_message({1: "heelo"}, socket.gethostname(), 19000)
    # message2.sending_message({1: "heelo"}, socket.gethostname(), 19000)
#     port1 = 19001
#     message2 = MessageManager(19001)
#     proces1 = multiprocessing.Process(target=message2.start_receiving, args=(port1,))
#     proces1.start()
#     message = MessageManager(19002)
#     # Send message
#     message.sending_message({1: "salam"}, socket.gethostname(), 19001)
#     time.sleep(1)
#     message.sending_message({1: "salam"}, socket.gethostname(), 19001)
#     time.sleep(3)
#     port2 = 19002
#     process2 = multiprocessing.Process(target=message.start_receiving, args=(port2,))
#     process2.start()
#     message2.sending_message({1: "salam"}, socket.gethostname(), 19002)
#     time.sleep(1)
#     message2.sending_message({1: "salam"}, socket.gethostname(), 19002)
#     message.sending_message({1: "salam"}, socket.gethostname(), 19002)
#     # message.sending_message("hello", socket.gethostname(), 19002)
#     # time.sleep(3)
#     # message.sending_message("hello", socket.gethostname(), 19002)
#     # message.sending_message("hello", socket.gethostname(), 19002)

# import json
# import socket
# import threading
#
#
# class MessageManager:
#     def __init__(self, my_port):
#         self.client_socket = None
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.buffer = {}
#         self.my_port = my_port
#
#     def sending_message(self, message, host, port):
#         self.server_socket.connect((host, port))
#         #self.client_socket, addr = self.server_socket.accept()
#         #print(f"get connected to : {addr} , soon will send message !")
#         self.server_socket.send(message.encode())
#
#     def receive_message(self ,host , port):
#         self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client_socket.bind((host, port))
#         self.client_socket.listen(1)
#         self.client_socket.setblocking(False)
#         while True:
#             # client_socket, addr = self.client_socket.accept()
#             # print(f"Got connection from {addr}")
#             message = self.client_socket.recv(1024).decode()
#             print(f"recive message from server :{message}")
#
#
# message = MessageManager(19001)
# message2 = MessageManager(19002)
# thread_1 = threading.Thread(target=message2.receive_message(socket.gethostname(), 19001))
#
# message.sending_message("hello", socket.gethostname(), 19002)
#
# thread_1.start()
# thread_1.join()

# class MessageManager:
#     def __init__(self, buffer_size, start_of_port_domain, server_port):
#         self.client_socket = None
#         self.buffer = {}
#         self.buffer_size = buffer_size
#         self.sending_port_domain = start_of_port_domain
#         self.server_port = server_port
#         self.establish_connection_for_receiver()
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     def establish_connection_for_receiver(self, host=socket.gethostname()):
#         self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         print(host, self.server_port)
#         self.client_socket.bind((host, self.server_port))  # Connect to server
#         self.client_socket.listen(1)
#         self.client_socket.setblocking(False)
#         # conn, _ = self.client_socket.accept()
#         # print("Receiver connected")
#
#     def establish_connection_for_sender(self, port, message, host):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conf:
#             try:
#                 conf.connect((host, port))
#                 # json_data = json.dumps(message, indent=4)
#                 # print(json_data)
#                 conf.send(message.encode())
#             except socket.error as error:
#                 print("have problem in sending message : %s" % (error))
#
#     def receive_message(self, sender_id, message):
#         self.buffer[sender_id] = message
#
#     def get_message(self, sender_id):
#         result = self.buffer.get(sender_id, [])
#         self.clear_buffer(sender_id)
#         return result
#
#     def clear_buffer(self, sender_id):
#         self.buffer[sender_id] = None
#
#     def receiver(self):
#         while True:
#             try:
#                 # print(f"Connected to {addr}")
#                 json_data = self.client_socket.recv(1024).decode()
#                 print(json_data)
#                 # message_dict = json.loads(json_data)
#                 # sender_id, message = next(iter(message_dict.items()))
#                 # self.buffer[sender_id] = message
#                 self.client_socket.close()  # Close the connection after receiving the message
#             except socket.error as error:
#                 print("There is a problem with the receiver:", error)
#         # while True:
#         #     try:
#         #         json_data = self.client_socket.recv(1024).decode()
#         #         #message_dict = json.loads(json_data)
#         #         #sender_id, message = next(iter(message_dict.items()))
#         #         self.buffer[1] = json_data
#         #     except socket.error as error:
#         #         print("there is problem with receiver %s" % (error))
#
#     def sender(self, message, neighbor_server_list):
#         for server in neighbor_server_list:
#             self.establish_connection_for_sender(self.sending_port_domain + server, message)
#
#
# messanger1 = MessageManager(1, 19000, 19001)
# messanger2 = MessageManager(1, 19000, 19002)
# thread_receiver1 = threading.Thread(target=messanger1.receiver)
# thread_receiver2 = threading.Thread(target=messanger2.receiver)
# thread_receiver1.start()
# thread_receiver2.start()
# messanger2.sender("hello you1", [1])
# messanger1.sender("hello you2", [2])
# print(messanger1.get_message(2))
# print(messanger2.get_message(1))
# thread_receiver1.join()
# thread_receiver2.join()
