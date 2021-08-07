import copy
import functools

stats = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
combinations = [
    ['A', 'B', 'C'],
    ['A', 'D', 'E'],
    ['A', 'D', 'G'],
    ['A', 'B'],
    ['A', 'D'],
    ['A', 'F'],
    ['B', 'F'],
    ['D', 'G'],
    ['A', 'G'],
    ['A'],
    ['B'],
    ['C'],
    ['D'],
    ['E'],
    ['F'],
    ['G']
]

def removeElementsFromStats (combination, copy_stats):
    for stat in combination:
        copy_stats.remove(stat)
        
possibleCombinations = {}
def removeStats(starting_combination, copy_stats, copy_combinations, stats_number):
    wasCombinationAdded = False
    j = 0
    while j < len(copy_combinations) and len(copy_stats) > 0:
        for stat in starting_combination:
            #print("TESTING ", stat)
            #print(copy_combinations[j])
            if stat in copy_combinations[j]:
                if stat in copy_stats:
                    removeElementsFromStats(starting_combination, copy_stats)
                    if wasCombinationAdded == False:
                        stats_number.append(len(starting_combination))
                        wasCombinationAdded = True
                copy_combinations[j].remove(stat)
        #print("AFTER REMOVING: ", copy_combinations[j])
        j = j + 1



for i in range(len(combinations)):
    copy_stats = stats.copy()
    copy_combinations = copy.deepcopy(combinations)
    #print("COPY COMBINATION before:\t", copy_combinations)
    copy_combinations = copy_combinations[i+1::]

    if len(copy_combinations) > 0:
        #print("COPY COMBINATION after :\t", copy_combinations)

        stats_number = []

        starting_combination = combinations[i]
        while len(starting_combination) > 0 and len(copy_stats) > 0:
            removeStats(starting_combination, copy_stats, copy_combinations, stats_number)
            copy_combinations = sorted(copy_combinations, key=len, reverse=True)
            #print("REMAINING STATS: ", copy_stats)
            #print("COMBINATIONS: ", copy_combinations)
            starting_combination = copy_combinations[0]
        if len(copy_stats) == 0:
            #print("--------COMBINATION ", i, "--------")
            #print(stats_number)
            total = 0
            for n in stats_number:
                total += n * 10 + (n - 1) * 10
            #print(total)
            if total not in possibleCombinations:
                possibleCombinations[total] = stats_number
print(possibleCombinations)

