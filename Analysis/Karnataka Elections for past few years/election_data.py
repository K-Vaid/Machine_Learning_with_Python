"""
Import election_data.csv file

Here is the data of Karnataka Elections for few years. Perform analysis based on the problem statement:

Considering the candidates who have contested in more than one Assembly 
elections, Do such candidates contest from the same constituency in all the 
elections? If not, does the change of constituency have any effect on the 
performance of the candidate? Display the performance effect using a pie chart.

Considering the candidates who have contested in more than one Assembly 
elections, Do such candidates contest under the same party in all the 
elections? If not, how does the change in alliance of the candidate affect 
the outcome of the next election? Display the outcome using a pie chart.

Do candidates who contested for multiple elections enjoy higher vote share 
percentages compared to the candidates who have contested only once? Display 
the vote share percentage for both type of candidates using a pie chart.

file_name - "election_data.py"

"""

import pandas as pd

data = pd.read_csv("election_data.csv")

#g = data.groupby(["Name_of_Candidate","Assembly_no"]).groups.keys()

#g.sort()

#g = pd.Series(g).drop_duplicates()

cand_names = data["Name_of_Candidate"].drop_duplicates()

ass_cand_names = []

# check for candidates who have contested from more than 1 assembly election
for i in cand_names:
    ass_no = list(set(data["Assembly_no"][data["Name_of_Candidate"]==i]))
    if len(ass_no) > 1:
        ass_cand_names.append(i)

# check for change in constituency
ppl_lst, freq = [], []

for i in ass_cand_names:
    elec_lst = list(set(data["Constituency_no"][data["Name_of_Candidate"]==i]))
    if len(elec_lst) > 1:
        freq.append(elec_lst)
        ppl_lst.append(i)

# check for votes for each constiteuncy
total = []
for c,f in zip(ppl_lst,freq):
    votes = []
    for const in f:
        votes.append(data["Votes"][(data["Constituency_no"]==const) & (data["Name_of_Candidate"]==c)].mean())
    total.append(votes)

# check for vote increase or decrese
performance = []
for t in total:
    max_no = max(t)
    ind = t.index(max_no)
    if ind == 0:
        performance.append(False)
    else:
        performance.append(True)

dec = performance.count(False)
inc = performance.count(True)

candi_data = [dec,inc]

import matplotlib.pyplot as plt
labels = ["No-Benifit","Benifit"]
plt.pie(candi_data,labels=labels,autopct="%1.2f%%")
plt.title("Candidate Performance after Changing Constitution_no")
plt.axis('equal')
plt.show()


# check for change in party
prty_ppl_lst, prty_freq = [], []

for i in cand_names:
    prty_lst = list(set(data["Party"][data["Name_of_Candidate"]==i]))
    if len(prty_lst) > 1:
        prty_freq.append(prty_lst)
        prty_ppl_lst.append(i)


# check for votes for each party
prty_total_votes = []
for c,p, in zip(prty_ppl_lst,prty_freq):
    votes = []
    for prty in p:
        votes.append(data["Votes"][(data["Party"]==prty) & (data["Name_of_Candidate"]==c)].mean())
    prty_total_votes.append(votes)


# Performance check
performance = []
for t in prty_total_votes:
    max_no = max(t)
    ind = t.index(max_no)
    if ind == 0:
        performance.append(False)
    else:
        performance.append(True)

dec = performance.count(False)
inc = performance.count(True)

candi_prty_data = [dec,inc]

import matplotlib.pyplot as plt
labels = ["No-Benifit","Benifit"]
plt.pie(candi_prty_data,labels=labels,autopct="%1.2f%%")
plt.title("Candidate Performance after Changing Party")
plt.axis('equal')
plt.show()



# Check for single or multiple elections
candi_names = data["Name_of_Candidate"].drop_duplicates()

single_election, multi_election = [], []
for i in candi_names:
    elect = list(set(data["Year"][data["Name_of_Candidate"]==i]))
    if len(elect) > 1:
        multi_election.append(i)
    else:
        single_election.append(i)


# single 
single_vote_share = []
for i in single_election:
    vote = float(data["Vote_share_percentage"][data["Name_of_Candidate"]==i].get_values().mean())
    single_vote_share.append(vote)

single_vote_share = pd.Series(single_vote_share).mean()


multi_vote_share = []
for i in multi_election:
    vote = float(data["Vote_share_percentage"][data["Name_of_Candidate"]==i].get_values().mean())
    multi_vote_share.append(vote)

multi_vote_share = pd.Series(multi_vote_share).mean()

vote_share = [multi_vote_share,single_vote_share]

import matplotlib.pyplot as plt
labels = ["Multi_Party","Single_Party"]
plt.pie(vote_share,labels=labels,autopct="%1.2f%%")
plt.title("Vote Share Percentage Changing Party")
plt.axis('equal')
plt.show()