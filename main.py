"""let us movie theater example to calculate the average wait times of customers  
if the server of theater does not work for some time they will sell food . if the cashier is not available or the ticket checker is not available
then customer have to wait for long time..
"""
#importing necessary modules
import numpy as np
import random as rd
import simpy as sp
import statistics


# let us make the class Theatre necessary
class Theatre:
    def __init__(self, env, cashier, servers, tc_checker):
        self.env = env
        self.cashier = sp.Resource(env, capacity=cashier)
        self.server = sp.Resource(env, capacity=servers)
        self.tc_checker = sp.Resource(env, capacity=tc_checker)
    
    def purchase_tc(self, persons):
        yield self.env.timeout(rd.randint(1, 3)) # hardly requires 3 minutes

    def check_tc(self, persons):
        yield self.env.timeout(3/60) # as it requires 3 seconds

    def sell_food(self, persons):
        yield self.env.timeout(rd.randint(1, 5)) # hardly 5 min

def inside_theatre(env, persons, theatre):
    arrival = env.now # requires to difference at end to find total time of customer inside theatre
    print(f"Person {persons} arrived at {arrival}")

    with theatre.cashier.request() as req: # we use with to check and access resources 
        yield req # similar to return but associated with waiting till resource availability
        yield env.process(theatre.purchase_tc(persons)) # she will purchase tc when cashier will be available

    # similarly for ticket checker 
    with theatre.tc_checker.request() as req:
        yield req
        yield env.process(theatre.check_tc(persons))

    # server can work or may not at that time
    if rd.choice([True, False]):
        with theatre.server.request() as req:
            yield req 
            yield env.process(theatre.sell_food(persons))
    
    total_wait = env.now - arrival
    wait_times.append(total_wait) # total waiting of customer is added to the list
    print(f"Person {persons} total wait time: {total_wait}")

def run_theatre(env, cashier, servers, tc_checker):
    theatre = Theatre(env, cashier, servers, tc_checker) # object of class Theatre
    for persons in range(4): # suppose 4 people enter initially
        env.process(inside_theatre(env, persons, theatre)) # func which actually contain simulation process
    
    while True:
        yield env.timeout(0.20) # for seconds it is 0.20
        persons += 1
        env.process(inside_theatre(env, persons, theatre)) # same will be done to added customers

def get_avg_wait(wait_times):
    return statistics.mean(wait_times) # it calculates mean

def main():
    rd.seed(42)
    cashier, servers, tc_checker = 2, 2, 2 # assume these all are 2
    env = sp.Environment() # the env is our movie theater
    env.process(run_theatre(env, cashier, servers, tc_checker)) # process this func
    env.run(until=90)   # run for 90 min
    print(f"Average wait time is {get_avg_wait(wait_times)} minutes.") 

if __name__ == '__main__':
    wait_times = []
    main()
