# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 22:01:24 2016

@author: Daniel_2
"""

from sys import argv
import random
import math
import matplotlib.pyplot as plt

#used these as global vars before adding them as inline args.
'''
X_MIN = -2.5
X_MAX = 2.5
Y_MIN = -2.5
Y_MAX = 2.5
STEP_SIZE = 0.05
NUM_RESTARTS = 10
SIM_TEMP = 90
'''

#to analyze a different function, this function must be edited.
def analyze_2var_function(x, y):
    #determines answer to function given in class
    #unsure of why r is sqrt(x^2 + y^2), since r is always squared,
    #   but i just went with how it was written. it may produce slightly odd results
    #   due to how python handles floats
    r = math.sqrt(x**2 + y**2)
    finalOne = math.sin(x**2 + 3 * y**2)
    finalTwo = (0.1 + r**2)
    finalThree = (x**2 + 5 * y**2)
    finalFour = (math.exp(1 - r**2) / 2)
    final = finalOne / finalTwo + finalThree * finalFour
    return float(final)

def main():
    
    #uses inline arguments
    try:
        #inline arguments
        X_MIN = float(argv[1])
        X_MAX = float(argv[2])
        Y_MIN = float(argv[3])
        Y_MAX = float(argv[4])
        STEP_SIZE = float(argv[5])
        NUM_RESTARTS = int(argv[6])
        SIM_TEMP = int(argv[7])
    #if the inline arguments are invalid, then it uses thes ones instead
    except:
        X_MIN = -2.5
        X_MAX = 2.5
        Y_MIN = -2.5
        Y_MAX = 2.5
        STEP_SIZE = 0.05
        NUM_RESTARTS = 10
        SIM_TEMP = 90
    
    #inline arguments
    hillClimbGraph = hill_climb(analyze_2var_function, STEP_SIZE, X_MIN, X_MAX, Y_MIN, Y_MAX)
    
    #prints the "global minimums" found by each search type
    print("=============================================================")
    print("Global Min for Hill Climb:")
    print("   z = " + str(hillClimbGraph[2][-1]))
    print("-------------------------------------------------------------")
    print("Global Min for Hill Climb with Random Restarts:")
    randHillClimbGraph = hill_climb_random_restart(analyze_2var_function, STEP_SIZE, NUM_RESTARTS, X_MIN, X_MAX, Y_MIN, Y_MAX)
    print("   z = " + str(randHillClimbGraph[2][-1]))
    print("-------------------------------------------------------------")
    print("Global Min for Simulated Annealing:")
    simAnnealGraph = simulated_annealing(analyze_2var_function, STEP_SIZE, SIM_TEMP, X_MIN, X_MAX, Y_MIN, Y_MAX)
    print("   z = " + str(simAnnealGraph[2][-1]))
    print("=============================================================")
    
    #prints a graph of all three searches
    comparative_graph_of_searches(hillClimbGraph, randHillClimbGraph, simAnnealGraph)

def hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax):
    
    #uses a random value as the start value
    currX = random.uniform(xmin, xmax)
    currY = random.uniform(xmin, ymax)
    currZ = function_to_optimize(currX, currY)
    hillClimbGraph = [[currX],[currY],[currZ]]
    
    #runs until the same Z value occurs twice in a row
    flag = True
    while(flag):
        #options will contain all the possible jump direction options
        options = []
        xDif = -1
        yDif = -1
        #uses step_size to create 9 different jump options to make
        while(yDif < 2):
            newX = currX + (xDif * step_size)
            newY = currY + (yDif * step_size)
            if(newX >= xmin and newX <= xmax and newY >= ymin and newY <= ymax):
                   newZ = function_to_optimize(newX, newY)
                   options.append([newX, newY, newZ])
            if(xDif == 1):
                xDif = -1
                yDif += 1
            else:
                xDif += 1
        newVals = [currX, currY, currZ]
        #chooses the option with the lowest z value
        for opt in options:
            if(opt[2] <= newVals[2]):
                newVals = opt
        #for plotting graph, appends data to a vector for the graph here
        hillClimbGraph[0].append(newVals[0])
        hillClimbGraph[1].append(newVals[1])
        hillClimbGraph[2].append(newVals[2])
        
        #if it is the same Z value (meaning it didnt move up), the loop ends
        if(currZ == newVals[2]):
            flag = False
        currX = newVals[0]
        currY = newVals[1]
        currZ = newVals[2]
    #returns the graph of moves
    return hillClimbGraph
            
     
def hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin, ymax):
    
    #runs hill climb 1+num_restarts
    restart = 0
    currHillClimbGraph = hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax)
    while(restart < num_restarts):
        newHillClimbGraph = hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax)
        #takes the best valued graph as the actual graph
        if(currHillClimbGraph[2][-1] > newHillClimbGraph[2][-1]):
            currHillClimbGraph = newHillClimbGraph
        restart += 1
    return currHillClimbGraph
    
def simulated_annealing(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax):
    
    #uses a random value as the start value
    currX = random.uniform(xmin, xmax)
    currY = random.uniform(xmin, ymax)
    currZ = function_to_optimize(currX, currY)
    simAnnealGraph = [[currX],[currY],[currZ]]
    
    #sets a miniature temp and the value temp decreases by (percentage)
    temp = max_temp
    tempMin = 0.0001
    alpha = 0.95
    while(temp > tempMin):

        xDif = 0
        yDif = 0
        #generates either -1 (decrease), 0 (no change), or 1 (increase) for xDif and yDif
        while(xDif == 0 and yDif == 0):
            xDif = random.randint(-1,1)
            yDif = random.randint(-1,1)
            
        #gets what values the currX and currY will jump to
        jumpX = genNextJump(step_size, max_temp, temp, xmax, xmin, currX, xDif)
        jumpY = genNextJump(step_size, max_temp, temp, ymax, ymin, currY, yDif)
        
        #add the jump values to the corresponding coordinate values
        newX = currX + jumpX
        newY = currY + jumpY
        newZ = function_to_optimize(newX, newY)

        #if the new Z value is less than the old one, accepts new coords
        if(newZ < currZ):
            currX = newX
            currY = newY
            currZ = newZ
            simAnnealGraph[0].append(currX)
            simAnnealGraph[1].append(currY)
            simAnnealGraph[2].append(currZ)
        #if not:
        else:
            #determines probability of accepting new coords
            switchProb = math.e**(-(newZ-currZ)/temp)
            #if value > random number from 0 to 1, then new coords accepted
            rand = random.uniform(0, 1)
            if(switchProb > rand):
                currX = newX
                currY = newY
                currZ = newZ
                simAnnealGraph[0].append(currX)
                simAnnealGraph[1].append(currY)
                simAnnealGraph[2].append(currZ)
        #decreases temp by given percentage (alpha)
        temp = temp*alpha
    return simAnnealGraph
    
#creates the jump for the x or y coordinate
def genNextJump(stepSize, maxTemp, currTemp, maxVal, minVal, currVal, direction):
    
    #if there is no change, there is no jump
    if(direction == 0):
        return 0
    #determines max value that jump can be (based on step size)
    perc = currTemp/maxTemp
    maxInt = (((maxVal-minVal)/2)/stepSize)*perc
    if(int(maxInt) == 0):
        maxInt = 1
    #assigns maxInt the greater value between itself and the difference between
    #the current value and the axis towards which the value will jump
    if(direction == 1):
        if(maxInt > ((maxVal - currVal)/stepSize)):
            maxInt = (maxVal-currVal)/stepSize
    elif(direction == -1):
        if(maxInt > ((currVal - minVal)/stepSize)):
            maxInt = (currVal-minVal)/stepSize
    #maxInt is "rounded down" to nearest int
    maxInt = int(maxInt)
    jump = 0
    if(maxInt != 0):
        #if maxInt isnt 0, creates the jump value
        jump = stepSize * random.randint(1, maxInt)
        jump = jump*direction
        #if the jump value is outside the bounds, dont jump
        if(((jump + currVal) < minVal) and (direction == -1)):
            jump = 0
        elif(((jump + currVal) > maxVal) and (direction == 1)):
            jump = 0
    return jump
    
def comparative_graph_of_searches(hillClimbGraph, randHillClimbGraph, simAnnealGraph):
    
    #creates a plot with 3 axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ##plots the hill climb graph
    ax.plot([hillClimbGraph[0][0]], [hillClimbGraph[1][0]], [hillClimbGraph[2][0]], c='r', marker='s')
    ax.plot(hillClimbGraph[0], hillClimbGraph[1], hillClimbGraph[2], c='r')
    ax.plot([hillClimbGraph[0][-1]], [hillClimbGraph[1][-1]], [hillClimbGraph[2][-1]], c='r', marker='o')
    #plots the best graph from hill climb with random restarts
    ax.plot([randHillClimbGraph[0][0]], [randHillClimbGraph[1][0]], [randHillClimbGraph[2][0]], c='b', marker='s')
    ax.plot(randHillClimbGraph[0], randHillClimbGraph[1], randHillClimbGraph[2], c='b')
    ax.plot([randHillClimbGraph[0][-1]], [randHillClimbGraph[1][-1]], [randHillClimbGraph[2][-1]], c='b', marker='o')
    #plots the simulated annealing graph
    ax.plot([simAnnealGraph[0][0]], [simAnnealGraph[1][0]], [simAnnealGraph[2][0]], c='g', marker='s')
    ax.plot(simAnnealGraph[0], simAnnealGraph[1], simAnnealGraph[2], c='g')
    ax.plot([simAnnealGraph[0][-1]], [simAnnealGraph[1][-1]], [simAnnealGraph[2][-1]], c='g', marker='o')
    #Sets limits on the graph so it is consistent each time
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_zlim(-0.5, 2)
    plt.show()
    
    
main()