from typing import Dict
import jsonSenderAndReceiver
import json
import socket
import socket
import multiprocessing
import time


class BackTracking:
    def __init__(self, k):
        # target : [1 , 2]
        self.targetTracker = {}
        # tracker_id : [target1 , ...]
        self.target_can_tracked_by_node = {}
        self.assignment = {}
        self.K = k
        self.useless_target = []
        # self.recursive_backtracking(self.assignment)

    def node_status(self, node: int, list_of_target: list):
        self.target_can_tracked_by_node[node] = list_of_target
        # for target in list(self.target_can_tracked_by_node.values())[0]:
        #     print(target)
        #     if target not in targets:
        #         targets.append(target)
        #         self.update_target_tracker(target)
        for item in list_of_target:
            if item not in list(self.targetTracker.keys()):
                self.update_target_tracker(item)

    def update_target_tracker(self, target, tracker=None):
        if tracker is None:
            self.targetTracker.setdefault(target, [])
            return
        self.targetTracker[target].append(tracker)

    def unassigned_variable(self, assignment):
        unassigned_variable_list = []
        for element in self.target_can_tracked_by_node.keys():
            if element not in list(self.targetTracker.values()) and element not in list(assignment.keys()):
                unassigned_variable_list.append(element)

        unassigned_variable_list.sort(reverse=False, key=lambda item: len(
            [tar for tar in self.target_can_tracked_by_node.get(item, []) if
             tar not in [useless for useless in self.targetTracker.keys() if
                         len(self.targetTracker.get(useless, [])) == self.K]]))
        # unassigned_variable_list.sort(reverse=False, key=lambda item: len(self.domain_values2(item, self.K)))
        #  len([tar for tar in self.target_can_tracked_by_node.get(item, []) if tar not in assignment.get(item, [])]))
        return unassigned_variable_list

    def eligible_to_conditions(self, target, tracker, k):
        # First, check that the desired target has tracker comparison
        # > also , The condition of communication must also be established
        # if len(self.targetTracker.get(target)) < k  and \
        #     (k - len(self.targetTracker.get(target))) <= self.candidates_to_track(target) and \
        #     tracker not in self.targetTracker.get(target):
        if target != "":
            return True

    def candidates_to_track(self, target):
        var = self.unassigned_variable(self.assignment)
        counter = 0
        for element in var:
            if target in self.target_can_tracked_by_node.get(element):
                counter += 1
        return counter

    def domain_values(self, tracker, k):
        # try to ordred based on  need to tracker , in god mod , one get all other nothing !
        # > also should check if other can tolk with this tracker or not !
        # if
        domain_list = []
        for target in self.target_can_tracked_by_node.get(tracker):
            # print(self.targetTracker.get(target))
            if len(self.targetTracker.get(target)) < k:
                # print(str(tracker) + " i am tracker")
                # print(k - len(self.targetTracker.get(target)))
                # print(self.candidates_to_track(target))
                if (k - len(self.targetTracker.get(target))) <= self.candidates_to_track(target):
                    domain_list.append(target)

        # if len(domain_list) != 0:
        #     #print(domain_list)
        #     return domain_list

        domain_list.sort(reverse=True, key=lambda item: len(self.targetTracker.get(item, [])))
        return domain_list

    def recursive_backtracking(self, assignment):
        if len(list(self.assignment.keys())) == len(list(self.target_can_tracked_by_node.keys())):
            return assignment
        # variable = self.unassigned_variable(self.assignment)
        # if variable is not None:
        for item in self.unassigned_variable(self.assignment):
            # print(self.domain_values(item, 3))
            domain = self.domain_values(item, self.K)
            if len(domain) == 0:
                self.assignment.setdefault(item, [])
                return self.recursive_backtracking(self.assignment)
            else:
                for value in domain:
                    if self.eligible_to_conditions(value, item, self.K):
                        self.assignment.setdefault(item, []).append(value)
                        self.targetTracker.setdefault(value, []).append(item)
                        result = self.recursive_backtracking(assignment)
                        if result != False:
                            return result
                        assignment[item].remove(value)
            return False
        # var = ( lambda item : item not in self.unassigned_variable())


class Sensor(BackTracking):

    def __init__(self, neighbor: list, k: int, sensor_id: int, sense: list):
        super().__init__(k)
        self.local_tree = {}
        self.neighbor = {}
        # self.K = k
        self.target = []
        self.suggestion_list = {}
        self.name = sensor_id
        self.waiting_for_message_from = []
        self.sense_object(sense)
        # create dictionary of neighbor , each has a list
        # that specifies the status of its own targets
        for element in neighbor:
            self.neighbor[element] = []
        # self.Sensor()

    # def sensor(self):
    #     # sensor prot is id + 19000
    #     sensor_port = self.name + 19000
    #     messenger = jsonSenderAndReceiver.MessageManager(sensor_port)
    #     messenger.start_receiving()
    #     have_change = True
    #     while (True):
    #         print("this is your neighbor :", self.neighbor, have_change)
    #         if have_change:
    #             for neighbor in list(self.neighbor.keys()):
    #                 dist_port = neighbor + 19000
    #                 messenger.sending_message({self.name: [self.target, self.local_tree]}, socket.gethostname(),
    #                                           dist_port)
    #             have_change = False
    #         for new_status in messenger.general_buffer:
    #             print("here the new status :" ,new_status)
    #             tmp = messenger.get_buffer()
    #             print("here is the  big tmp : ", tmp , self.name)
    #             print("update neighbor like this : ", {tmp[0]: tmp[1][0]})
    #             have_change = self.update_neighbor_status({tmp[0]: tmp[1][0]})
    #             self.update_local_tree()
    #             print("is thes proper three ? :", tmp[1][1])
    #             print(f"this is my three ? :{self.local_tree} i am : " , self.name)
    #             if len(tmp[1][1]) != 0:
    #                 have_change = self.compair_neighbor_tree(tmp[1][1])
    #             print("here the buffer after shit stuff :" , messenger.general_buffer)
    def sense_object(self, target):
        # it needs to change to 2 dimension
        # update target list
        for element in self.target:
            if element not in target:
                self.target.remove(element)

        for element in target:
            if element not in self.target:
                self.target.append(element)

    def update_neighbor_status(self, neighbor_status: Dict[int, list]):
        # neighborStatus is something look like this :
        # { neighbor_id : [ target 1 , target 2 , ... .. .  ] }
        # print(list(neighbor_status.keys())[0])

        if self.neighbor.get(list(neighbor_status.keys())[0], []) == list(neighbor_status.values())[0]:
            return False
        self.neighbor[list(neighbor_status.keys())[0]] = list(neighbor_status.values())[0]
        return True

    def create_local_tree(self):
        # Different situations of problem :
        # A :
        # If the sensor has only one target in its list,
        # it looks for K neighbors in the list that has similar conditions
        # and offers cooperation to the other sensor(s).

        # B :
        # If the sensor had one target and no similar neighbors (one target);
        # Suggests to K random neighbor, but it only changes its array
        #    (maybe a better decision will be made in the future for other sensor)

        # C :
        # If it has one target and a neighbor does not know the target, or if it has more than one target
        # it waits for a message from other neighbors for a proposal
        # (the final tree will be formed in nodes with several targets.
        #   The wait continues until the neighbors of a target make a decision.
        #   their decision will reduce the decision range of other neighbors!
        #   In the best case, a sequential decision will be made, but in normal conditions,
        #   if it still has uncertain conditions, it will try to make a decision using tree with the largest number of target
        #   Backtracking algorithm will be the main solution in this situation .)
        counter = 0
        if len(self.target) == 1:
            self.suggestion_list[self.name] = self.target
            for sen in (list(self.neighbor.keys())):
                if len(self.neighbor.get(sen)) == 1 and self.neighbor.get(sen)[0] == self.target[0]:
                    counter += 1
                    self.suggestion_list[sen] = list(self.neighbor.values())[0]
                    if counter == self.K - 1:
                        # print(self.suggestion_list)
                        return
        # are sensor have multiple target
        # It is very important that we do our best at this stage to involve K 'single target' node
        # I want to use backtracking !

        for element in self.target:
            self.suggestion_list[self.name] = self.target
            for sen in (list(self.neighbor.keys())):
                if sen not in list(self.suggestion_list.keys()) and element in self.neighbor.get(sen):
                    print(self.neighbor.get(sen))
                    counter += 1
                    self.suggestion_list[sen] = list(self.neighbor.get(sen))
                    if counter == self.K - 1:
                        print(self.suggestion_list)
                        return

        if counter != self.K - 1:
            print("target cannot get tracked")

    def update_local_tree(self):
        self.node_status(self.name, self.target)
        for node in list(self.neighbor.keys()):
            self.node_status(node, self.neighbor.get(node, []))
        self.recursive_backtracking(self.assignment)
        for sensor in list(self.assignment.keys()):
            if len(self.assignment.get(sensor)) == 0:
                self.assignment[sensor] = self.target_can_tracked_by_node.get(sensor);
        # for target in list(self.targetTracker.keys()):
        #     if len(self.targetTracker[target]) < self.K:
        #         for decision in self.targetTracker[target]:
        #             result[decision] = self.target_can_tracked_by_node.get(decision)
        self.local_tree = self.assignment
        # print(self.assignment)
        return True

    def compair_neighbor_tree(self, tree: dict):
        # There are two main intuitive conditions for comparing the node tree of two sensors.
        # The first condition that has more priority; The condition is that the number of targets is less per sensor.
        # This condition gives priority to the decision that has more certainty.
        # The second condition is priority with the tree that contains the least number of nodes.
        # This main condition solves the defect of the first condition to some extent.
        # In the first condition, a sensor may make a decision that is more certain due to ignorance of the
        # overall topology, but the cause of certainty is ignorance.
        # The second condition prioritizes the sensors that have fewer neighbors. This condition
        # allows the sensor that has a  smaller range of awareness to make a decision to have a more preferable opinion.
        for sensor in list(tree.keys()):
            if len(self.local_tree.get(sensor, [])) > len(tree.get(sensor, [])):
                return False
        if len(list(self.local_tree.keys())) < len(list(tree.keys())):
            return False

        for target in self.targetTracker:
            self.targetTracker[target] = []
        self.assignment = {}
        for sensor in list(tree.keys()):
            if len(tree.get(sensor)) == 1 and tree.get(sensor)[0] in self.targetTracker:
                self.targetTracker[tree.get(sensor)[0]].append(sensor)
                if sensor in self.neighbor.keys() or sensor == self.name:
                    self.assignment[sensor] = tree.get(sensor)
                    self.local_tree[sensor] = tree.get(sensor, [])
                    self.target_can_tracked_by_node.update({sensor: tree.get(sensor, [])})

        # for target in list(tree.values()):

        # print("here target list : ")
        # print(self.target_can_tracked_by_node)
        # print("here target tracker :")
        # print(self.targetTracker)
        # print(self.local_tree)
        # print("i am done with neighbor")
        return True


#
# if __name__ == '__main__':
#     ins1 = Sensor([1], 3, 1, ["t2", "t3", "t1"])
#     ins1.sensor()
# ins2 = Sensor.Sensor([3, 1, 6], 3, 2, ["t2", "t1", "t3 "])
# process2 = multiprocessing.Process(target=ins2.sensor, args=())
# process2.start()
#
# ins3 = Sensor.Sensor([2, 1, 4, 5], 3, 3, ["t2", "t3", "t4"])
# process3 = multiprocessing.Process(target=ins3.sensor, args=())
# process3.start()
#
# ins4 = Sensor.Sensor([5, 3, 1], 3, 4, ["t3", "t4"])
# process4 = multiprocessing.Process(target=ins4.sensor, args=())
# process4.start()
#
# ins5 = Sensor.Sensor([3, 4], 3, 5, ["t3", "t4"])
# process5 = multiprocessing.Process(target=ins5.sensor, args=())
# process5.start()
#
# ins6 = Sensor.Sensor([1, 2], 3, 6, ["t2", "t1"])
# process6 = multiprocessing.Process(target=ins6.sensor, args=())
# process6.start()

if __name__ == '__main__':
    ins1 = Sensor([1, 2, 5, 4], 3, 3,["t2", "t4", "t3"])
    ins1.update_neighbor_status({4: ["t3", "t4"]})
    ins1.update_neighbor_status({1: ["t2", "t3"]})
    ins1.update_neighbor_status({2: ["t2", "t1"]})
    ins1.update_neighbor_status({5: ["t4", "t3"]})

    ins2 = Sensor([3, 2, 6], 3, 1,["t2", "t1", "t3 "])
    ins2.update_neighbor_status({6: ["t1", "t2"]})
    ins2.update_neighbor_status({2: ["t1", "t2"]})
    ins2.update_neighbor_status({3: ["t4", "t2", "t3"]})

    ins3 = Sensor([2, 1], 3, 6,["t2", "t1"])
    ins3.update_neighbor_status({2: ["t1", "t2"]})
    ins3.update_neighbor_status({1: ["t1", "t2"]})

    print("data in sens 3 :: ")
    ins1.create_local_tree()
    result1 = ins1.update_local_tree()

    print("data in sens 1 :: ")
    ins2.create_local_tree()
    result2 = ins2.update_local_tree()

    print("data in sens 6 :: ")
    ins3.create_local_tree()
    result3 = ins3.update_local_tree()
    print("3 --> 1")
    print(ins2.compair_neighbor_tree(result1))
    print("1 --> 3")
    print(ins1.compair_neighbor_tree(result2))
    print("6 --> 1")
    result4 = ins2.compair_neighbor_tree(result3)
    print(result4)
    print("1 --> 3")
    print(ins1.compair_neighbor_tree(result4))

# def sort_unassigned_variable_list(unassigned_variable_list ):
# class message_manager:
#     def __init__(self , buffer_size):
#         self.buffer = {}
#         self.buffer_size = buffer_size
#
#     def receive_message(self, sender_id , message):
#         self.buffer[sender_id] = message
#
#     def get_message(self , sender_id):
#         result = self.buffer.get(sender_id, [])
#         self.clear_buffer(sender_id)
#         return result
#
#     def clear_buffer(self , sender_id):
#         self.buffer[sender_id] = None
#
#     def receiver(self):
#         while True:
#


# class MessageManager:
#     def __init__(self, my_port_tosend):
#         self.client_socket = None
#         self.server_socket = None
#         self.buffer = {}
#         self.my_port_tosend = my_port_tosend
#
#     def sending_message(self, message, host, port):
#         while True:
#             try:
#                 client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                 client_socket.connect((host, port))
#                 client_socket.send(message.encode())
#                 client_socket.close()
#                 break  # Exit the loop if message sent successfully
#             except ConnectionRefusedError:
#                 print("Connection refused. Retrying in 1 second...")
#                 time.sleep(1)
#
#     def receive_message(self, host, port):
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.bind((host, port))
#         server_socket.listen(1)
#         conn, addr = server_socket.accept()
#         while True:
#             conn, addr = server_socket.accept()
#             print(f"Got connection from {addr}")
#             message = conn.recv(1024).decode()
#             if not message:
#                 continue  # Skip empty messages
#             print(f"Received message from client: {message}")
#             conn.close()
#         #
#         # while True:
#         #     print(f"Got connection from {addr}")
#         #     message = conn.recv(1024).decode()
#         #     if not message:
#         #         break
#         #     print(f"Received message from client: {message}")
#         # conn.close()
#     def start_receiving(self , port):
#         message = MessageManager(19002)
#         message.receive_message(socket.gethostname(), 19002)
#
#

#
# # after full day , intruduse you to message manager function !!!!!( still dont know its call function method or ...)
#  # Start receiving message thread
#     port1 = 19002
#     message2 = MessageManager(19001)
#
#     proces1 = multiprocessing.Process(target=message2.start_receiving, args=(port1 , ))
#     proces1.start()
#     #   proces1.join()
#     # thread_1 = threading.Thread(target=message2.receive_message,args=(socket.gethostname(), 19002))
#     # thread_1.start()
#     message = MessageManager(19001)
#
#     # Send message
#     message.sending_message("hello", socket.gethostname(), 19002)
#     time.sleep(3)
#     message.sending_message("hello", socket.gethostname(), 19002)
#     time.sleep(3)
#     message.sending_message("hello", socket.gethostname(), 19002)
#     time.sleep(3)
#     message.sending_message("hello", socket.gethostname(), 19002)
#     # message.sending_message("hello", socket.gethostname(), 19002)


# ins1.compair_neighbor_tree({1: ['t2'], 2: ['t2'], 6: ['t2'], 3: ["t2", "t4", "t3"]})
