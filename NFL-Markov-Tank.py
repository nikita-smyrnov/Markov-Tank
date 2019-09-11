#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


# In[2]:


def weighted_random(initial, probs):
    new_rand = random.uniform(0, 1)
    temp_sum = 0
    
    for i in range(len(probs[0])):
        temp_sum += probs[initial - 1][i]
        
        if new_rand < temp_sum:
            return i + 1
    
    return -1


# In[3]:


SIMULATIONS = 100000
TEAMS = 32
DRAFTS = 18
TENURE = 5
states_tested = [4, 5, 7]
teams_list = ["Cardinals", "Falcons", "Ravens", "Bills", "Panthers", "Bears", 
              "Bengals", "Browns", "Cowboys", "Broncos", "Lions", "Packers", "Texans", 
              "Colts", "Jaguars", "Chiefs", "Dolphins", "Vikings", "Patriots", "Saints", 
              "Giants", "Jets", "Raiders", "Eagles", "Steelers", "Rams", "Chargers", 
              "49ers", "Seahawks", "Buccaneers", "Titans", "Redskins"]


# In[4]:


data = pd.read_csv("NFL Draft Order, 2002-2019.csv")


# In[5]:


def label_teams(data, teams_list, analysis_num):
    team_groups = np.zeros(shape = (TEAMS, DRAFTS))
    
    for i in range(DRAFTS):
        for j in range(TEAMS):
            team_name = data.iloc[j, i + 1]
            
            if analysis_num == 4:
                if j < 5:
                    team_groups[teams_list.index(team_name)][i] = 1
                elif j < 10:
                    team_groups[teams_list.index(team_name)][i] = 2
                elif j < 30:
                    team_groups[teams_list.index(team_name)][i] = 3
                else:
                    team_groups[teams_list.index(team_name)][i] = 4
            elif analysis_num == 5:
                if j < 5:
                    team_groups[teams_list.index(team_name)][i] = 1
                elif j < 10:
                    team_groups[teams_list.index(team_name)][i] = 2
                elif j < 20:
                    team_groups[teams_list.index(team_name)][i] = 3
                elif j < 30:
                    team_groups[teams_list.index(team_name)][i] = 4
                else:
                    team_groups[teams_list.index(team_name)][i] = 5
            else:
                if j < 5:
                    team_groups[teams_list.index(team_name)][i] = 1
                elif j < 10:
                    team_groups[teams_list.index(team_name)][i] = 2
                elif j < 15:
                    team_groups[teams_list.index(team_name)][i] = 3
                elif j < 20:
                    team_groups[teams_list.index(team_name)][i] = 4
                elif j < 28:
                    team_groups[teams_list.index(team_name)][i] = 5    
                elif j < 30:
                    team_groups[teams_list.index(team_name)][i] = 6
                else:
                    team_groups[teams_list.index(team_name)][i] = 7
    
    return team_groups


# In[6]:


total_data = []

for markov_num in states_tested:
    markov_groups = label_teams(data, teams_list, markov_num)
    markov_probs = np.zeros(shape = (markov_num, markov_num))

    for i in range(TEAMS):
        for j in range(1, DRAFTS):
            curr_state = markov_groups[i][j - 1] - 1
            next_state = markov_groups[i][j] - 1
            markov_probs[int(curr_state)][int(next_state)] += 1
            
    total = markov_probs.sum(0)

    for i in range(markov_num):
        for j in range(markov_num):
            markov_probs[i][j] /= total[i]
            
    graph_data = np.zeros(shape = (markov_num, TENURE))

    for i in range(TENURE):
        for state in range(markov_num):
            super_bowl = 0

            for sims in range(SIMULATIONS):
                initial = state + 1
                flag = False

                for years in range(i + 1):
                    initial = weighted_random(initial, markov_probs)

                    if initial > markov_num - 1:
                        flag = True

                if flag:
                    super_bowl += 1

            super_bowl /= (SIMULATIONS / 100)
            graph_data[state][i] = super_bowl
    
    total_data.append(graph_data)


# In[7]:


ticks = []
years = []

for i in range(TENURE):
    ticks.append(i)
    years.append("Year " + str(i + 1))


# In[8]:


for i in range(len(total_data)):
    for j in range(states_tested[i]):
        state_name = 'State ' + str(j + 1)
        plt.plot(total_data[i][j], label = state_name)
        
    plt.legend()
    plt.xticks(ticks, years)
    plt.ylabel("(%)")
    plt.title("Probability of making Super Bowl")
    
    path_name = str(states_tested[i]) + "states.png"
    plt.savefig(path_name)
    plt.clf()


# In[11]:


for i in range(len(total_data)):
    print("Year 1 Difference: " + str(total_data[i][int(states_tested[i] / 2)][0] - total_data[i][0][0]))
    print("Year 5 Difference: " + str(total_data[i][int(states_tested[i] / 2)][4] - total_data[i][0][4]))


# In[ ]:




