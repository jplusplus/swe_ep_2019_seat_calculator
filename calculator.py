from collections import defaultdict
import operator

def calculate_seats_swe_ep(party_votes, available_seats=20):
    """ 
    Source: https://www.val.se/download/18.574dd8aa1610997fea4280/1516712867457/Mandatfordelning%20785-4.pdf p. 8-9
    
    The method basically works as follows:
    
        1. Divide all party votes by the first divisor (1,2 as of 2018)
        2. Party with highest value gets the seat
        3. Votes for the party that received the previous seat is divided by number of seats * 2 + 1
        4. Repeat 3-4 until no more seats
        
    Below this is translated to the following:
    
        1. Divide all party votes by the first divisor
        2. While there are more seats:
            a. Give the party with the highest value a seat
            b. Divide party that received the seat by number of seats * 2 + 1
        3. If party did not receive any seats, add to result with "no seats"
               
    Usage:
        calculate_seats([
            ("M", 12345),
            ("S", 23456),
            ...
        ], seats=20)

        =>

        [
            ("M", 4),
            ("S", 6),
            ...
        ]
    """
    # Set up data structures
    n_seats = defaultdict(int)
    result = defaultdict(int)

    # 1. Divide all party votes by the first divisor
    first_divisor = 1.2
    comparative_quotas = {p: v / first_divisor for p, v in party_votes}
    
    # 2. While there are more seats
    party_votes = dict(party_votes)
    while available_seats:
        # a. Party with the highest value gets the seat
        top_party = max(comparative_quotas.items(), key=operator.itemgetter(1))[0]
        
        n_seats[top_party] += 1
        result[top_party] += 1
        
        available_seats -= 1
        
        # b. Votes for the party that received the previous seat is divided by number of seats * 2 + 1
        new_divisor = n_seats[top_party] * 2 + 1
        comparative_quotas[top_party] = party_votes[top_party] / new_divisor
    
    # 3. If party did not receive any votes, add text
    for p in party_votes.keys():
        if p not in result.keys():
            result[p] = 'no seats'
    
    return [(k, v) for k, v in result.items()]

