import csv
import pprint

import numpy as np

P = ["Trump", "Clinton", "Bush"]

V1 = "Trump Clinton Bush"
V2 = "Trump Bush Clinton"
V3 = "Clinton Trump Bush"
V4 = "Clinton Bush Trump"
V5 = "Bush Trump Clinton"
V6 = "Bush Clinton Trump"

global votes_dict


# the top preferred candidate(first in order) gets the votes. Sum up the votes of each first ordered candidate per
# state and store the winner, his/her total votes, number of seats and the loser in a dictionary with key = name of
# the state.
def states_plurality():
    state_winner_dic = {}
    pref_list = [0] * 3  # this list represent the total votes for each candidate per state; index 0 is Trump,
    # index 1 is Clinton and index 2 is Bush

    for key, values in votes_dict.items():
        for info in values:
            column = info.split(" ")
            if len(column) > 2:  # selecting votes columns(V1, V2, V3, V4, V5, V6)
                name = column[0]  # first in order candidate
                pref_list[P.index(name)] += int(values[info])  # sum up the votes for this candidate

        # get the candidate with the highest number of votes(max) per state and store it in a dictionary
        max_vote = max(pref_list)
        index = pref_list.index(max_vote)

        # get the candidate with the lowest number of votes(min) per state and store it in a dictionary
        min_vote = min(pref_list)
        index_min = pref_list.index(min_vote)
        excl_cand = P[index_min]
        state_winner_dic.update(
            {key: {"Winner": P[index], "Seats": votes_dict[key]["Seats"], "Votes": pref_list[index],
                   "Last-candidate": excl_cand}})
        pref_list = [0] * 3  # reset the counter after each state

    return state_winner_dic


# in a plurality with run-off we have to exclude the candidate with the least votes(found in the previous method) and
# recalculate the total votes for the first two candidates per state. If the least voted candidate is the top
# preference for some voters, then their votes go to the next candidate in order(LINE 62). We return a dictionary
# with key = name of the state and its values: the winner, his/her total votes, number of seats.
def states_plur_runoff(states_dict):
    state_winner_runoff_dic = {}
    pref_list = [0] * 3

    for key, values in votes_dict.items():
        for info in values:
            column = info.split(" ")
            if len(column) > 2:
                name = column[0]
                if name == states_dict[key]["Last-candidate"]:
                    name = column[1]
                pref_list[P.index(name)] += int(values[info])

        max_vote = max(pref_list)
        index = pref_list.index(max_vote)
        state_winner_runoff_dic.update(
            {key: {"Winner": P[index], "Seats": votes_dict[key]["Seats"], "Votes": pref_list[index]}})
        pref_list = [0] * 3

    return state_winner_runoff_dic


# when a candidate wins a state, he/she gets the corresponding number of seats. The one that has the most number of
# seats wins the election
def seats_count_state_winner(state_winner_dic):
    result_list = [0] * 3
    # calculate how many seats each candidate received by winning in different states. The one with the
    # most seats wins the election
    for key in state_winner_dic.keys():
        name = state_winner_dic[key]["Winner"]
        result_list[P.index(name)] += int(state_winner_dic[key]["Seats"])

    winner = get_winner_from_votes_list(result_list)
    return result_list, winner


# sum up the votes of the top preferred candidate without taking into consideration the states.
# this function also works for the overall plurality with run-off. When this is activated and the method also gets the
# candidate with the least votes(excl_candidate), it recalculates the votes of the remaining two candidates in the
# following way: If the least voted candidate is the top preference for some voters, then their votes go to the next
# candidate in line.

def overall_plurality(run_off, excl_candidate):
    result_list = [0] * 3
    for key, values in votes_dict.items():
        for info in values:
            column = info.split(" ")
            if len(column) > 2:
                name = column[0]
                # in case we have plurality with run-off and the most preferred candidate is the one excluded, then
                # the next candidate in order takes the votes
                if run_off and name == excl_candidate:
                    name = column[1]
                result_list[P.index(name)] += int(values[info])

    winner = get_winner_from_votes_list(result_list)
    return result_list, winner


def get_winner_from_votes_list(pref_list):
    max_seats = max(pref_list)
    index = pref_list.index(max_seats)
    winner = P[index]
    return winner


def get_prob(popularity_votes):
    prob_per_candidate = [0] * 3
    total_votes = sum(popularity_votes)
    for i in range(0, 3):
        prob_per_candidate[i] = round(popularity_votes[i] / total_votes, 2)
    return prob_per_candidate


# if one of the candidates has the majority: >=50% of the votes then he wins the election. Otherwise, the winner is
# chosen at random considering the probability of each candidate = the portion of their votes. candidates'
# probability is determined by the ratio between the plurality vote and total number of voters
def majority_or_random_voting(prob_list):
    for i in range(0, 3):
        if prob_list[i] >= 0.5:
            winner = P[i]
            return winner
    print("No candidate has a majority, therefore the winner will be drawn randomly according to their portion of the "
          "votes.")
    winner = np.random.choice(P, p=prob_list)
    return winner


#  main
votes_dict = {}
with open('votes.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        votes_dict.update({row["State"]: {"Population": row["Population"], "Seats": row["Seats"], V1: row[V1],
                                          V2: row[V2], V3: row[V3], V4: row[V4], V5: row[V5], V6: row[V6]}})

pretty = pprint.PrettyPrinter()

# EX1
state_winner_dic = states_plurality()
print("Plurality winner per state:")
pretty.pprint(state_winner_dic)

print("Plurality rule per state.")
seats_results, seats_winner = seats_count_state_winner(state_winner_dic)
print("Number of seats for Trump, Clinton, Bush: ", seats_results)
print("The winner of US election: ", seats_winner)

# EX2
print("\nPlurality rule overall US.")
plurality_results, plurality_winner = overall_plurality(False, "")
print("Number of votes for Trump, Clinton, Bush: ", plurality_results)
print("The winner of overall plurality election: ", plurality_winner)

# EX3
print("\nPlurality with run-off overall")
min_votes = min(plurality_results)
index = plurality_results.index(min_votes)
excluded_candidate = P[index]
print("The candidate with the smallest amount of votes(overall): ", excluded_candidate)

plur_runoff_results, plur_runoff_winner = overall_plurality(True, excluded_candidate)
print("Number of votes for Trump, Clinton, Bush: ", plur_runoff_results)
print("The winner of overall plurality with run-off election: ", plur_runoff_winner)

# EX4
print("\nPlurality with run-off per state")
state_winner_runoff_dic = states_plur_runoff(state_winner_dic)
print("Plurality winner with run-off per state:")
pretty.pprint(state_winner_runoff_dic)

seats_results_runoff, seats_winner_runoff = seats_count_state_winner(state_winner_runoff_dic)
print("\nNumber of seats for Trump, Clinton, Bush: ", seats_results_runoff)
print("The winner of plurality with run-off election per state: ", seats_winner_runoff)

# EX5
prob_list = get_prob(plurality_results)
print("\nVotes percentage for Trump, Clinton, Bush: ", prob_list)
winner = majority_or_random_voting(prob_list)
print("The winner is: ", winner)
