import pandas as pd
import math
import numpy as np
import random

data = pd.read_csv('../data/acp_naive.csv')
print(data.head())

# ACTIVE = STABLE && INACTIVE = UNSTABLE
data_act = data[data['Instability'] <= 40] #419
data_inact = data[data['Instability'] > 40] #634
print(len(data_act))
print(len(data_inact))


def CreateDictionaryGap4(sequences):
    d = {}
    i = 0
    while i < len(sequences):
        sequence = sequences.iloc[i]
        j = 0
        while j < len(sequence) - 4:
            if str(sequence[j]) + '----' + str(sequence[j + 4]) in d:
                d[str(sequence[j]) + '----' + str(sequence[j + 4])] += 1
                j += 1
            else:
                d[str(sequence[j]) + '----' + str(sequence[j + 4])] = 1
                j += 1
        i += 1
    return d


d_gap4_total = CreateDictionaryGap4(data['SEQ'])
d_gap4_act = CreateDictionaryGap4(data_act['SEQ'])
d_gap4_inact = CreateDictionaryGap4(data_inact['SEQ'])
print(sum(d_gap4_act.values()))
print(sum(d_gap4_inact.values()))
print(d_gap4_total)


def CreateDictionaryNear(sequences):
    d = {}
    i = 0
    while i < len(sequences):
        sequence = sequences.iloc[i]
        j = 0
        while j < len(sequence) - 1:
            if str(sequence[j]) + str(sequence[j + 1]) in d:
                d[str(sequence[j]) + str(sequence[j + 1])] += 1
                j += 1
            else:
                d[str(sequence[j]) + str(sequence[j + 1])] = 1
                j += 1
        i += 1
    return d


d_near_total = CreateDictionaryNear(data['SEQ'])
d_near_act = CreateDictionaryNear(data_act['SEQ'])
d_near_inact = CreateDictionaryNear(data_inact['SEQ'])
print(d_near_total)


def CreateDictionarySingle(sequences):
    d = {}
    i = 0
    while i < len(sequences):
        sequence = sequences.iloc[i]
        j = 0
        while j < len(sequence):
            if str(sequence[j]) in d:
                d[str(sequence[j])] += 1
                j += 1
            else:
                d[str(sequence[j])] = 1
                j += 1
        i += 1
    return d


d_single_total = CreateDictionarySingle(data['SEQ'])
d_single_act = CreateDictionarySingle(data_act['SEQ'])
d_single_inact = CreateDictionarySingle(data_inact['SEQ'])

print(d_single_total)

def CalculateDscore(dic_act, dic_inact):
    d_score = {}
    for key in dic_act.keys():
        if key in dic_inact:
            d_score[key] = math.log(dic_act[key] / dic_inact[key] * sum(dic_inact.values()) / sum(dic_act.values()))
        else:
            continue
    return d_score


d_score_single = CalculateDscore(d_single_act, d_single_inact)
d_score_gap4 = CalculateDscore(d_gap4_act, d_gap4_inact)
d_score_near = CalculateDscore(d_near_act, d_near_inact)

print(d_score_single)
print(d_score_gap4)
print(d_score_near)


def ExtractDescriptors(sequence):
    i = 0
    j = 0
    k = 0
    d_single = {}
    d_near = {}
    d_gap4 = {}

    while i < len(sequence):
        if str(sequence[i]) in d_single:
            d_single[str(sequence[i])] += 1
            i += 1
        else:
            d_single[str(sequence[i])] = 1
            i += 1

    while j < len(sequence) - 1:
        if str(sequence[j]) + str(sequence[j + 1]) in d_near:
            d_near[str(sequence[j]) + str(sequence[j + 1])] += 1
            j += 1
        else:
            d_near[str(sequence[j]) + str(sequence[j + 1])] = 1
            j += 1

    while k < len(sequence) - 4:
        if str(sequence[k]) + '----' + str(sequence[k + 4]) in d_gap4:
            d_gap4[str(sequence[k]) + '----' + str(sequence[k + 4])] += 1
            k += 1
        else:
            d_gap4[str(sequence[k]) + '----' + str(sequence[k + 4])] = 1
            k += 1
    return d_single, d_near, d_gap4


def CalculateBScore(sequence, d_score_single, d_score_near, d_score_gap4):
    d_single, d_near, d_gap4 = ExtractDescriptors(sequence)
    d_score = 0
    for key in d_single.keys():
        if key in d_score_single:
            d_score += d_single[key] * d_score_single[key]
        else:
            continue

    for key in d_near.keys():
        if key in d_score_near:
            d_score += d_near[key] * d_score_near[key]
        else:
            continue

    for key in d_gap4.keys():
        if key in d_score_gap4:
            d_score += d_gap4[key] * d_score_gap4[key]
        else:
            continue

    return d_score


parents = data_act.sample(50).append(data_inact.sample(50))
parents

score = []
for i in range(0, len(parents)):
    res = CalculateBScore(parents.iloc[i]['SEQ'], d_score_single, d_score_near, d_score_gap4)
    score.append(res)
parents['Score'] = score

int_prob = [int(i + 40) for i in score]
parents['Int_prob'] = int_prob


def ParentsSelection(parents):
    total_prob = int(max(parents['Score']) * 2)
    prob_total = np.random.randint(0, total_prob, size=[1, 4])[[0][0]].tolist()
    seq_int = []
    for i in range(0, len(parents)):
        parents_prob = np.random.randint(0, total_prob, size=[1, parents.iloc[i, -1]])[[0][0]].tolist()
        for random_int in prob_total:
            if random_int in parents_prob:
                seq_int.append(parents.iloc[i, 1])
            else:
                continue
        i += 1
    return list(set(seq_int))


initial_parents = ParentsSelection(parents)


def CrossOver(parents_sequences):
    kids = []
    if len(parents_sequences) % 2 == 0:
        while len(parents_sequences) > 0:

            # Select Mom and Dad
            parents1 = random.choice(parents_sequences)
            parents_sequences.remove(parents1)
            parents2 = random.choice(parents_sequences)
            parents_sequences.remove(parents2)

            # Cross over and 8 kids will be given birth
            i = 0
            while i < 2:
                cut_point1 = np.random.randint(1, len(parents1))
                cut_point2 = np.random.randint(1, len(parents2))
                chrome1_1 = str(parents1)[0:cut_point1]
                chrome1_2 = str(parents1)[cut_point1:len(parents1)]
                chrome2_1 = str(parents2)[0:cut_point2]
                chrome2_2 = str(parents2)[cut_point2:len(parents2)]
                kids = kids + [chrome1_1 + chrome2_1, chrome1_1 + chrome2_2, chrome1_2 + chrome2_1,
                               chrome1_2 + chrome2_2]
                i += 1
    else:
        parents_sequences.remove(random.choice(parents_sequences))
        while len(parents_sequences) > 0:
            parents1 = random.choice(parents_sequences)
            parents_sequences.remove(parents1)
            parents2 = random.choice(parents_sequences)
            parents_sequences.remove(parents2)
            j = 0
            while j < 2:
                cut_point1 = np.random.randint(1, len(parents1))
                cut_point2 = np.random.randint(1, len(parents2))
                chrome1_1 = str(parents1)[0:cut_point1]
                chrome1_2 = str(parents1)[cut_point1:len(parents1)]
                chrome2_1 = str(parents2)[0:cut_point2]
                chrome2_2 = str(parents2)[cut_point2:len(parents2)]
                kids = kids + [chrome1_1 + chrome2_1, chrome1_1 + chrome2_2, chrome1_2 + chrome2_1,
                               chrome1_2 + chrome2_2]
                j += 1
    return kids


def Mutation(sequences):
    all_aa = ['A', 'C', 'E', 'D', 'F', 'I', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    mutation_rate = 1 / 1000
    after_mutation = []
    for sequence in sequences:
        new_sequence = ''
        for aa in str(sequence):
            numb = random.uniform(0, 1)
            if numb <= mutation_rate:
                aa = random.choice(all_aa)
                new_sequence += aa
            else:
                new_sequence += aa
        after_mutation.append(new_sequence)
    return after_mutation


# '''def ParentsSelectionDic(parents):
#     score_prob = []
#     for key in parents.keys():
#         parents[key] = int(10 +  + abs(min(parents[key])))
#         score_prob.append(i)
#     parents.values() = score_prob
#     total_prob = int(max(parents.values()) * 2)
#     prob_total = np.random.randint(0, total_prob, size=[1,4])[[0][0]].tolist()
#     seq_int = []
#     for i in range(0,len(parents.keys())):
#         parents_prob = np.random.randint(0,total_prob, size=[1,parents.values()[i]])[[0][0]].tolist()
#         for random_int in prob_total:
#             if random_int in parents_prob:
#                 seq_int.append(parents.keys()[i])
#             else:
#                 continue
#         i += 1
#     return list(set(seq_int))
# '''


def NaturalSelection(parents):
    fluctuate = np.random.randint(-5, 5)
    length_threshold = 25
    thresh_real = length_threshold + fluctuate
    new_parents = []
    for seq in parents:
        if len(seq) <= thresh_real:
            # if helicity > 0.5 and <0.8:
            new_parents.append(seq)

    return new_parents


def ReproductionCycle(initial_parents, d_score_single, d_score_near, d_score_gap4, cyclenumber):
    parents = initial_parents  # list
    i = 0
    while i <= cyclenumber:
        kids = CrossOver(parents)  # list
        real_kids = Mutation(kids)  # list
        all_score = []
        for j in range(0, len(real_kids)):
            score = CalculateBScore(real_kids[j], d_score_single, d_score_near, d_score_gap4)
            all_score.append(score)
        int_prob = [int(10 + k + abs(min(all_score))) for k in all_score]
        seq_score = pd.DataFrame({'SEQ1': real_kids, 'SEQ': real_kids,
                                  'Score': all_score})
        seq_score['Int_prob'] = int_prob
        naive_parents = ParentsSelection(seq_score)  # dictionary given, output a list
        parents = NaturalSelection(naive_parents)
        i += 1
    return seq_score.sort_values(by='Score')['Score'].mean(), seq_score.sort_values(by='Score').tail()['SEQ']


final_seq = ReproductionCycle(initial_parents, d_score_single, d_score_near, d_score_gap4, 5)
print('The final sequence is ' + str(final_seq))

