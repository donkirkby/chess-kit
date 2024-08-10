from collections import Counter
from random import shuffle

PIECE_LIMIT = 1  # Bust when count is higher than this.
PAWN_LIMIT = 5
# Results: Pawns at 4: 0.354 : 0.215, Pawns at 5: 0.210 : 0.263


def main():
    cause_counts = Counter()
    pieces = list('PPPPPPPPNNBBRRQK')
    while True:
        shuffle(pieces)
        piece_counts = Counter()
        for piece in pieces:
            new_piece_count = piece_counts[piece] + 1
            piece_counts[piece] = new_piece_count
            if piece == 'P':
                is_busted = new_piece_count > PAWN_LIMIT
            else:
                is_busted = new_piece_count > PIECE_LIMIT
            if is_busted:
                cause_counts[piece] += 1
                break
        min_cause_count = min(cause_counts.values())
        if min_cause_count >= 100000:
            break
    test_count = sum(cause_counts.values())
    print(sorted(((cause_count / test_count, piece)
                  for piece, cause_count in cause_counts.items())))


main()
