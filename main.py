from typing import Dict

class Sensor:

    def __init__ (self, neighbor: list, k: int, sensor_id: int):
        self.neighbor = {}
        self.K = k
        self.target = []
        self.suggestion_list = {}
        self.name = sensor_id

        # create dictionary of neighbor , each has a list
        # that specifies the status of its own targets
        for element in neighbor :
            self.neighbor[element] = []

    def sense_object(self, target):
        # it needs to change to 2 dimension
        # update target list
        for element in self.target:
            if element not in target:
                self.target.remove(element)

        for element in target:
            if element not in self.target :
                self.target.append(element)

    def update_neighbor_status(self , neighbor_status: Dict[int, list]):
        # neighborStatus is something look like this :
        # { neighbor_id : [ target 1 , target 2 , ... .. .  ] }
        #print(list(neighbor_status.keys())[0])
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
                    self.suggestion_list[sen] = self.target
                    if counter == self.K-1:
                        print(self.suggestion_list)
            if counter != self.K-1:
                for sen in (list(self.neighbor.keys())):
                    if sen not in list(self.suggestion_list.keys()) and self.target[0] in self.neighbor.get(sen):
                        counter += 1
                        self.suggestion_list[sen] = self.target
                        if counter == self.K - 1:
                            print(self.suggestion_list)
            if counter != self.K - 1:
                print("target cannot get tracked")













if __name__ == '__main__':
    ins1 = Sensor([2, 3, 4, 5], 3, 1)
    ins1.sense_object(["t4"])
    ins1.update_neighbor_status({2: ["t1", "t2"]})
    ins1.update_neighbor_status({3: ["t1"]})
    ins1.update_neighbor_status({4: ["t1"]})
    ins1.update_neighbor_status({5: ["t1"]})
    ins1.create_local_tree()
