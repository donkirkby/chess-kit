# rawWords.csv is assembled by https://github.com/donkirkby/ludiverbia/blob/main/buildWords.mjs
from collections import Counter
from csv import DictReader
from pathlib import Path


class WordCounter:
    def __init__(self) -> None:
        self.start_counts: Counter[str] = Counter()
        self.end_counts: Counter[str] = Counter()
        self.total_counts: Counter[str] = Counter()
        self.min_counts: Counter[str] = Counter()

    def count(self, word_path: Path) -> None:
        with word_path.open() as f:
            reader = DictReader(f)
            if __name__ == '__live_coding__':
                reader = list(reader)[:1000]
            for row in reader:
                word = row['word']
                word_count = int(row['total'])
                self.start_counts[word[0]] += word_count
                self.end_counts[word[-1]] += word_count
                self.total_counts[word[0]] += word_count
                self.total_counts[word[-1]] += word_count
        for letter in self.total_counts:
            self.min_counts[letter] = min(self.start_counts[letter],
                                          self.end_counts[letter])

    def choose_letters(self,
                       collection_name: str,
                       total_squares: int) -> Counter[str]:
        letter_counts = getattr(self, collection_name + '_counts')
        chosen_counts: Counter[str] = Counter()
        word_total = letter_counts.total()
        remaining_squares = total_squares
        for letter, letter_count in letter_counts.most_common():
            if not remaining_squares:
                break
            ratio = letter_count / word_total
            goal = max(1, min(round(total_squares * ratio), remaining_squares))
            chosen_counts[letter] = goal
            remaining_squares -= goal
        return chosen_counts


def main():
    word_counter = WordCounter()
    word_path = Path(__file__).parent.parent / 'ludiverbia' / 'src' / "rawWords.csv"
    word_counter.count(word_path)
    total_squares = 36
    print('Starting letters:')
    display_letters(word_counter.choose_letters('start',
                                                total_squares))

    print()
    print('Ending letters:')
    display_letters(word_counter.choose_letters('end',
                                                total_squares))

    print()
    print('Both letters:')
    display_letters(word_counter.choose_letters('total',
                                                total_squares))

    print()
    print('Min letters:')
    display_letters(word_counter.choose_letters('min',
                                                total_squares))


def display_letters(letter_counts: Counter[str]):
    for letter, letter_count in letter_counts.most_common():
        print(f"{letter}: {letter_count}")


if __name__ in ('__main__', '__live_coding__'):
    main()
