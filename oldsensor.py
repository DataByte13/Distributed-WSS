from typing import Dict


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
        print("here list of tctbnnnnn:" , self.target_can_tracked_by_node)

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
        print("ino one! here the back info :", assignment)
        if len(list(self.assignment.keys())) == len(list(self.target_can_tracked_by_node.keys())):
            return assignment
        # variable = self.unassigned_variable(self.assignment)
        # if variable is not None:
        for item in self.unassigned_variable(self.assignment):
            domain = self.domain_values(item, self.K)
            print("here domain :", self.domain_values(item, 3))
            if len(domain) == 0:
                self.assignment.setdefault(item, [])
                return self.recursive_backtracking(self.assignment)
            else:
                for value in domain:
                    print("here domainee :", domain)
                    print("check value :", value)
                    if self.eligible_to_conditions(value, item, self.K):
                        self.assignment.setdefault(item, []).append(value)
                        self.targetTracker.setdefault(value, []).append(item)
                        result = self.recursive_backtracking(assignment)
                        if result != False:
                            return result
                        assignment[item].remove(value)
            return False

    # def recursive_backtracking(self, assignment):
    #     if len(list(self.assignment.keys())) == len(list(self.target_can_tracked_by_node.keys())):
    #         return assignment
    #     # variable = self.unassigned_variable(self.assignment)
    #     # if variable is not None:
    #     for item in self.unassigned_variable(self.assignment):
    #         # print(self.domain_values(item, 3))
    #         domain = self.domain_values(item, self.K)
    #         if len(domain) == 0:
    #             self.assignment.setdefault(item, [])
    #             return self.recursive_backtracking(self.assignment)
    #         else:
    #             for value in domain:
    #                 if self.eligible_to_conditions(value, item, self.K):
    #                     self.assignment.setdefault(item, []).append(value)
    #                     self.targetTracker.setdefault(value, []).append(item)
    #                     result = self.recursive_backtracking(assignment)
    #                     if result != False:
    #                         return result
    #                     assignment[item].remove(value)
    #         return False
    #     # var = ( lambda item : item not in self.unassigned_variable())


class Sensor(BackTracking):

    def __init__(self, neighbor: list, k: int, sensor_id: int):
        super().__init__(k)
        self.local_tree = {}
        self.neighbor = {}
        # self.K = k
        self.target = []
        self.suggestion_list = {}
        self.name = sensor_id

        # create dictionary of neighbor , each has a list
        # that specifies the status of its own targets
        for element in neighbor:
            self.neighbor[element] = []

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
        self.neighbor[list(neighbor_status.keys())[0]] = list(neighbor_status.values())[0]

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
                        print(self.suggestion_list)
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
            self.node_status(node, self.neighbor.get(node))

        self.recursive_backtracking(self.assignment)
        for sensor in list(self.assignment.keys()):
            if len(self.assignment.get(sensor)) == 0:
                self.assignment[sensor] = self.target_can_tracked_by_node.get(sensor);
        # for target in list(self.targetTracker.keys()):
        #     if len(self.targetTracker[target]) < self.K:
        #         for decision in self.targetTracker[target]:
        #             result[decision] = self.target_can_tracked_by_node.get(decision)
        self.local_tree = self.assignment
        print(self.assignment)
        return self.assignment

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
        # ++ target score way !
        my_tree_score = 0
        suggestion_tree_score = 0
        common_keys = set(self.local_tree.keys()) & set(tree.keys())
        for sensor in common_keys:
            if len(tree.get(sensor)) == len(self.local_tree.get(sensor)):
                continue
            elif len(tree.get(sensor)) == 1:
                suggestion_tree_score += 1
            elif len(self.local_tree.get(sensor)) == 1:
                my_tree_score += 1

        if my_tree_score == suggestion_tree_score:
            if len(list(self.local_tree.keys())) < len(list(tree.keys())):
                # I have better tree !
                return False
        if my_tree_score > suggestion_tree_score:
            # I have better tree
            return False

        for target in self.targetTracker:
            self.targetTracker[target] = []
        self.assignment = {}
        for sensor in list(tree.keys()):
            if sensor in self.neighbor.keys() or sensor == self.name:
                self.assignment[sensor] = tree.get(sensor)
                self.local_tree[sensor] = tree.get(sensor, [])
                self.target_can_tracked_by_node.update({sensor: tree.get(sensor, [])})
        return self.update_local_tree()

        # for target in list(tree.values()):
        # print("here target list : ")
        # print(self.target_can_tracked_by_node)
        # print("here target tracker :")
        # print(self.targetTracker)
        # print(self.local_tree)
        # print("i am done with neighbor")

    # def sort_unassigned_variable_list(unassigned_variable_list ):


if __name__ == '__main__':
    ins1 = Sensor([2], 2, 1)
    ins1.sense_object(["t2", "t3", "t1"])
    ins1.update_neighbor_status({2: ["t2", "t1", "t3 "]})
   # ins1.update_neighbor_status({3: ["t2", "t3", "t4"]})

    ins2 = Sensor([ 1], 2, 2)
    ins2.sense_object(["t2", "t1", "t3 "])
    #ins2.update_neighbor_status({3: ["t2", "t3", "t4"]})
    ins2.update_neighbor_status({1: ["t2", "t3", "t1"]})

    # ins3 = Sensor([2, 1], 2, 3)
    # ins3.sense_object(["t2", "t3", "t4"])
    # ins3.update_neighbor_status({2: ["t2", "t1", "t3 "]})
    # ins3.update_neighbor_status({1: ["t2", "t3", "t1"]})
    #
    print("data in sens 1 :: ")
    ins1.create_local_tree()
    result1 = ins1.update_local_tree()
    print(result1)

    # print("data in sens 2 :: ")
    # ins2.create_local_tree()
    # result2 = ins2.update_local_tree()
    #
    # print("data in sens 3 :: ")
    # ins3.create_local_tree()
    # result3 = ins3.update_local_tree()
    #
    # print("1 --> 3")
    # print(ins3.compair_neighbor_tree(result1))
    # print("1 --> 2")
    # print(ins2.compair_neighbor_tree(result1))
    #
    # print("2 --> 1")
    # result4 = ins1.compair_neighbor_tree(result2)
    # print(result4)
    # print("2 --> 3")
    # print(ins3.compair_neighbor_tree(result2))
    #
    # print("3 --> 2")
    # result4 = ins2.compair_neighbor_tree(result3)
    # print(result4)
    # print("3 --> 1")
    # print(ins1.compair_neighbor_tree(result3))
    #
    # print(ins1.local_tree)
    # 
    # print("data in sens 3 :: ")
    # ins1.create_local_tree()
    # result1 = ins1.update_local_tree()
    # 
    # print("data in sens 1 :: ")
    # ins2.create_local_tree()
    # result2 = ins2.update_local_tree()
    # 
    # print("data in sens 6 :: ")
    # ins3.create_local_tree()
    # result3 = ins3.update_local_tree()
    # print("3 --> 1")
    # print(ins2.compair_neighbor_tree(result1))
    # print("1 --> 3")
    # print(ins1.compair_neighbor_tree(result2))
    # print("6 --> 1")
    # result4 = ins2.compair_neighbor_tree(result3)
    # print(result4)
    # print("1 --> 3")
    # print(ins1.compair_neighbor_tree(result4))

    # ins1.compair_neighbor_tree({1: ['t2'], 2: ['t2'], 6: ['t2'], 3: ["t2", "t4", "t3"]})
