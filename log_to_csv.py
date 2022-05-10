import csv
import sys
import random
from itertools import product

HAND_SIZE = 5
N_COLOURS = 5
N_RANKS = 5
N_LIVES = 3
N_SAMPLES = 7

# HAND_SIZE = 2
# N_COLOURS = 2
# N_RANKS = 5
# N_LIVES = 1
# N_SAMPLES = 4

colours = {'R': 0, 'Y': 1, 'G': 2, 'W': 3, 'B': 4}
colours = {c: colours[c] for c in list(colours)[:N_COLOURS]}

cards = ['c%d' % (i+1) for i in range(HAND_SIZE)]

isprims = ['is%s_' % c for c in colours] + ['is%d_' % (i+1) for i in range(N_RANKS)]
psprims = ['ps%s_' % c for c in colours] + ['ps%d_' % (i+1) for i in range(N_RANKS)]
kpsprims = ['Kps%s_' % c for c in colours] + ['Kps%d_' % (i+1) for i in range(N_RANKS)]

kprims  = ['Col_',  'Rnk_' ]
kkprims = ['KCol_', 'KRnk_']

fwcolours = ['fw_%s' % c for c in colours]

dscolours = ['ds_%s' % c for c in colours]
dsranks = [str(i+1) for i in range(N_RANKS)]

copies = {'1': 3, '2': 2, '3': 2, '4': 2, '5': 1}

move_types = {'COLOR': 0, 'RANK': 1, 'DISCARD': 2, 'PLAY': 3, 'NONE': 4}

random.seed(2022)

def list_product(lists):
    return [''.join(x[::-1]) for x in product(*lists)]

def parse_file(output, target_players=(0,1)):
    N_PROPERTIES = N_COLOURS + N_RANKS
    states = []
    with open(output, 'w') as out:
        booleans = (list_product([cards, isprims]) +
                    list_product([cards, psprims]) +
                    list_product([cards, kprims]) +
                    list_product([cards, kpsprims]) +
                    list_product([cards, kkprims]))
        writer = csv.writer(out, delimiter='\t')
        writer.writerow(booleans +
                fwcolours +
                list_product([dsranks, dscolours]) +
                list(move_types.keys()) +
                list_product([cards, ['isCritical_']]) +
                list_product([cards, ['wasTouched_']]) +
                ['life', 'info', 'class'])
        game = 0
        for line in sys.stdin:
            if len(line) > 4 and line[3:5] == '||':
                if player:
                    k_data[card * 2] = line[6]
                    k_data[card * 2 + 1] = line[7]
                    for c in line[9:-1]:
                        if c.isdigit():
                            ps_data[card * N_PROPERTIES + int(c)-1 + N_COLOURS] = 'T'
                        else:
                            ps_data[card * N_PROPERTIES + colours[c]] = 'T'
                else:
                    kk_data[card * 2] = line[6]
                    kk_data[card * 2 + 1] = line[7]
                    for c in line[9:-1]:
                        if c.isdigit():
                            kps_data[card * N_PROPERTIES + int(c)-1 + N_COLOURS] = 'T'
                        else:
                            kps_data[card * N_PROPERTIES + colours[c]] = 'T'
                    is_data[card * N_PROPERTIES + colours[line[0]]] = 'T'
                    is_data[card * N_PROPERTIES + int(line[1])-1 + N_COLOURS] = 'T'
                    is_crit[card] = 'T' if copies[line[1]] - discards[(int(line[1])-1) * N_COLOURS + colours[line[0]]] == 1 else 'F'
                card += 1
            elif line.startswith('Hanabi game created'):
                if states:
                    game += 1
                    # writer.writerows(states)
                    writer.writerows(random.sample(states, N_SAMPLES))
                if game % 100 == 0:
                    print('game %d' % game)
                del states[:]
                fireworks = ['F'] * (N_COLOURS * N_RANKS) # unused
                discards = [0] * (N_COLOURS * N_RANKS)
                move = 'NONE'
                # track discards
                discarded = False
                lives = N_LIVES
            elif line.startswith('STATE'):
                is_data = ['F'] * (HAND_SIZE * N_PROPERTIES)
                ps_data = ['F'] * (HAND_SIZE * N_PROPERTIES)
                kps_data = ['F'] * (HAND_SIZE * N_PROPERTIES)
                k_data  = ['X'] * (HAND_SIZE * 2)
                kk_data = ['X'] * (HAND_SIZE * 2)
                is_crit = ['F'] * HAND_SIZE
            elif line.startswith('Current player:'):
                curr_player = int(line[16:])
            elif line.startswith('Life tokens:'):
                prev_lives = lives
                lives = int(line[13:])
                if prev_lives > lives: # life lost -> discard
                    discarded = True
            elif line.startswith('Info tokens:'):
                infos = int(line[13:])
            elif line.startswith('Fireworks:'):
                fws = [int(line[x]) for x in range(12, 12 + N_COLOURS * 3, 3)]
                for colour, rank in enumerate(fws):
                    if rank > 0:
                        fireworks[colour * N_RANKS + rank-1] = 'T'
            elif line.startswith('Hands:'):
                player = (curr_player == 0)
                card = 0
            elif line.startswith('Cur player'):
                assert(player)
            elif line.startswith('-----'):
                player = not player
                card = 0
            elif line.startswith('Discards:') and discarded:
                discards[(int(line[-2])-1) * N_COLOURS + colours[line[-3]]] += 1
                discarded = False
            elif line.startswith('MOVE:'):
                prev = ['F'] * len(move_types)
                prev[move_types[move.split('_', 1)[0]]] = 'T'
                
                touched = ['F'] * HAND_SIZE
                if move[0] == 'C' or move[0] == 'R': # record touched cards
                    clue = move.split('_', 1)[1]
                    if move[0] == 'C':
                        for card in range(HAND_SIZE):
                            if k_data[card * 2] == clue:
                                touched[card] = 'T'
                    else:
                        for card in range(HAND_SIZE):
                            if k_data[card * 2 + 1] == clue:
                                touched[card] = 'T'
                
                move = line[6:-1][1:-1].replace('Reveal player +1 ', '').replace(' ', '_').upper()
                if move[0] == 'P' or move[0] == 'D': # change card ids -> 1-5
                    if move[0] == 'D': # track discards
                        discarded = True # deck[hand[int(move[-1])]] -= 1
                    move = move[:-1] + str(int(move[-1]) + 1)
                states.append(is_data + ps_data + k_data + kps_data + kk_data + fws + discards + prev + is_crit + touched + [lives, infos, move])
        # writer.writerows(states)
        writer.writerows(random.sample(states, N_SAMPLES))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit('Usage: %s output.txt' % sys.argv[0])
    print('Hand size: %d\nColours: %d\nRanks: %d\nLives: %d\nSamples: %d' % (HAND_SIZE, N_COLOURS, N_RANKS, N_LIVES, N_SAMPLES))
    parse_file(sys.argv[1])
