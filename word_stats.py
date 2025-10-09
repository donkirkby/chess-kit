# rawWords.csv is assembled by https://github.com/donkirkby/ludiverbia/blob/main/buildWords.mjs
from collections import Counter
from csv import DictReader
from pathlib import Path


def main():
    start_counts: Counter[str] = Counter()
    end_counts: Counter[str] = Counter()
    total_counts: Counter[str] = Counter()
    min_counts: Counter[str] = Counter()
    word_path = Path(__file__).parent.parent / 'ludiverbia' / 'src' / "rawWords.csv"
    with word_path.open() as f:
        reader = DictReader(f)
        if __name__ == '__live_coding__':
            reader = list(reader)[:1000]
        for row in reader:
            word = row['word']
            word_count = int(row['total'])
            start_counts[word[0]] += word_count
            end_counts[word[-1]] += word_count
            total_counts[word[0]] += word_count
            total_counts[word[-1]] += word_count
    for letter in total_counts:
        min_counts[letter] = min(start_counts[letter], end_counts[letter])
    total_squares = 36
    print('Starting letters:')
    display_letters(start_counts, total_squares)

    print()
    print('Ending letters:')
    display_letters(end_counts, total_squares)

    print()
    print('Both letters:')
    display_letters(total_counts, total_squares)

    print()
    print('Min letters:')
    display_letters(min_counts, total_squares)

def display_letters(letter_counts: Counter[str], total_squares: int):
    word_total = letter_counts.total()
    remaining_squares = total_squares
    for letter, letter_count in letter_counts.most_common():
        if not remaining_squares:
            break
        ratio = letter_count / word_total
        goal = min(round(total_squares * ratio), remaining_squares)
        print(f"{letter}: {goal}")
        remaining_squares -= goal


main()
