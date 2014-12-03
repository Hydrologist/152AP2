import random
import simpy
import math

RANDOM_SEED = 31
SIM_TIME = 10
MU = 1
class host:
    def __init__(self, env, ethernet, arrival_rate, slot_length, my_id):
        self.ethernet = ethernet#the resource
        self.env = env
        self.transmit_slot= 0
        self.success_packets = 0
        self.flag_processing = 0
        self.packet_number = 0
        self.arrival_rate = arrival_rate
        self.slot_len = slot_length
        self.attempts = 0
        self.queue_len = 0
        self.id = my_id


    def process_packet(self, env, ethernet):
        print("Call process packet on Host ", self.id)
        process_time = random.expovariate(MU)
        print("Process takes ", process_time)
        self.queue_len -= 1
        yield env.timeout(process_time)
        print("After call process packet, Host ", self.id, " quelength is ", self.queue_len)
        #if self.queue_len == 0:
         #   self.flag_processing = 0
          #  self.start_idle_time = env.now
        #finish processing set attmpt to 0
        self.attempts = 0
        self.success_packets += 1
        self.transmit_slot += 1
  

    def packets_arrival(self, env):
        # packet arrivals
        print('Initiating packet arrival.')
        while True:
             # Infinite loop for generating packets
            yield env.timeout(random.expovariate(self.arrival_rate))
            print("Host ", self.id, "has incomming packet. <---------------------------------------")
              # arrival time of one packet

            self.packet_number += 1
            self.queue_len += 1
              # packet id
            #arrival_time = env.now
            #print(self.num_pkt_total, "packet arrival")
            #new_packet = Packet(self.packet_number,arrival_time)
            #if self.flag_processing == 0:
             #   self.flag_processing = 1
                #print("Idle period of length {0} ended".format(idle_period))
            print("Host ", self.id, " queue is now ", self.queue_len)
            #env.process(self.process_packet(env, new_packet))

    #if collision this reset host's next transmit slot
    def delay_transmission(self):
        print("Inside delay packet.")
        self.transmit_slot = self.transmit_slot + random.randint(0, 2**min(self.attempts, 10)) + 1
        self.attempts += 1
        print("Host ", self.id, " delayed packet to slot ", self.transmit_slot, " with attempts ", self.attempts)
    def delay_transmission1(self):
        self.transmit_slot = self.transmit_slot + min(self.attempts, 1024)
        self.attempts += 1
        #print("Host ",self.id," is delayed to ", self.transmit_slot, "with attempts", self.attempts)
class ethernet:
    def __init__(self, env, slot_length, num_hosts, arrival_rate):
        self.env = env
        self.server = simpy.Resource(env, capacity=1)
        self.slot_length = slot_length
        self.num_hosts = num_hosts
        self.slot_number = 0
        self.success_slots = 0
        self.hosts = []
        self.arrival_rate = arrival_rate
        for x in range(num_hosts):
            self.hosts.append(host(env, ethernet, arrival_rate, slot_length, x))

    def ethernet_control(self):
    #enable packet arrival at simultaneous time
        for x in range(self.num_hosts):
            self.env.process(self.hosts[x].packets_arrival(self.env))

        while True:
            #wait for slot time
            yield self.env.timeout(self.slot_length)
            print("=====================")
            print("Time ", self.env.now)
            print("Slot number", self.slot_number)
            request = 0
            #see if there is collision, number of request for this slot
            host_index = -1
            for x in range(self.num_hosts):
                if(self.hosts[x].queue_len == 0):
                    continue
                #if the host's slot is smaller than ethernet's current slot
                # and it has queue then it can transfer in this slot
                if((self.hosts[x].transmit_slot < self.slot_number)):
                    request += 1
                    host_index = x
                    self.hosts[x].transmit_slot = self.slot_number
                elif(self.hosts[x].transmit_slot == self.slot_number ):
                    request += 1 
                    host_index = x
                    if request > 1:
                        self.hosts[x].delay_transmission()


                print("Host ", x, " can possibly transmit at slot ", self.hosts[x].transmit_slot, "Queue is ", self.hosts[x].queue_len)
                #count only hosts that have stuff to transmit
            print("total host request at current slot: ", request)

            #allow the host to process
            if request == 1:
                self.success_slots += 1
                print(">>Can TRANSMIT<< since request = 1")
                self.env.process(self.hosts[host_index].process_packet(self.env, self.server))
                '''for x in range(self.num_hosts):
                    if(self.hosts[x].queue_len > 0) & (self.hosts[x].transmit_slot == self.slot_number):
                        self.env.process(self.hosts[x].process_packet(self.env, self.server))
                        break'''
            #detected collision
            '''elif request > 1:
                print("Call delay packets")
                for x in range(self.num_hosts):
                    if (self.hosts[x].transmit_slot == self.slot_number) & (self.hosts[x].queue_len >= 1):
                        self.hosts[x].delay_transmission()'''

            #update link's slot number
            self.slot_number += 1
    def get_throughput(self):
        print("At arrival rate: ", self.arrival_rate);
        print(self.success_slots, " success slots")
        print( self.success_slots/self.slot_number, " throughput")
        return (self.success_slots / self.slot_number)



        
                
""" Packet class """
class Packet:
    def __init__(self, identifier, arrival_time):
        self.identifier = identifier
        self.arrival_time = arrival_time
        self.attempts = 0


def main():
    throughput = [0]*9
    x = 0
    for arrival_rate in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]:
        slot_length = 1
        num_hosts = 10
        env = simpy.Environment()
        myethernet = ethernet(env, slot_length, num_hosts, arrival_rate)
        print("Slot length: ", slot_length)
        print("Number of hosts: ", num_hosts)
        env.process(myethernet.ethernet_control())
        env.run(until=SIM_TIME)
        throughput[x] = myethernet.get_throughput()
        x += 1
    print("Now we print all throughtput")
    for y in range(8):
        print(throughput[y])
if __name__ == '__main__': main()