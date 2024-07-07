---
title: New Rules for Chess Kit
subtitle: Experiments in Progress
---
### Introduction
These are new games that aren't ready yet. You can try them out and let me
know what you think.

## Table of Contents
# New Games
These games are in early development or playtesting. The rules might get more
filled out or change based on feedback from players.

## Two Move Chess
Players simultaneously choose two piece types to move, then move their chosen
pieces from least to most valuable. It was inspired by Richard Vickery's
[Nibelungenlied][Nibelungenlied].

[Nibelungenlied]: https://boardgamegeek.com/boardgame/7555/nibelungenlied

### Equipment
A standard chess set and a standard deck of 52 cards.

### Goal
Capture your opponent's king. There's no check or checkmate, because the cards
and simultaneous choices mean that a piece threatening the king might not be
allowed to make the capture.

### Setup
One player takes a pawn of each colour and hides one in each hand. The other
player picks a hand and then plays that colour. Don't worry, though, the
simultaneous play means that White has less advantage.

From the deck of cards, use one card to represent each piece type, as shown in
appendix A. Exclude the pawns, so you should end up with 10 cards: 5 of each
colour.

Put the rest of the cards away, you won't need them. Separate the cards by
colour, and give the black cards and pieces to the Black player and the white
cards and pieces to the White player. Place the chess pieces in the standard
starting position.

Finally, White picks two cards and places them face up in front of them. For
your first game, pick king and rook.

### Play
Each turn has two phases, played by both players at the same time: **choose**
cards, then **move** pieces from least to most valuable.

Both players secretly choose two cards and play them face down. One player will
start with two cards face up, and cannot choose those. Once all four cards are
played, reveal them.

Now players move the pieces that match their cards, in order from least to most
valuable: knight, then bishop, then rook, then queen, then king. Any of the
cards may be used to move a pawn, but they are still played in the order of the
cards. If players chose the same two cards, then both cards are eliminated and
no pieces move. If each player chose one matching card and one different card,
then the matching card is eliminated and the other card makes two moves. You may
make any combination of moves that match the card and pawn moves, but you may
never move the same pawn twice in one turn.

If you play a card, and it's not eliminated, you must make a move with that
piece type or with a pawn. If you have no legal move with that piece type or a
pawn, you don't make a move for that card.

Chess pieces move as in normal chess. Pawns can move two squares from the
second rank. Castling is allowed with a king card, if neither the king nor the
rook have moved and the squares between them are empty. It doesn't matter if an
opponent's piece is threatening the king's square or any of the squares it will
move through. Pawns do not capture en passant, but they do promote when they
reach the back rank.

Once all the moves are finished, the player with four cards face up puts them
all back in their hand. The other player leaves the two cards face up.

## Gravity Chess
This game was inspired by several video games that have pieces dropping down a
well and stacking on the bottom. Its most unusual mechanics are that both
players start on the same side of the board, and you move all your active pieces
every turn.

Design questions:

1. Can the end game be improved?
2. Can we make it easier to keep track of which pieces moved? Go from the bottom
   up?

### Equipment
A standard chess set and a standard deck of 52 cards.

### Setup
Place all the chess pieces beside the board. Put away four pawns of each colour,
you won't need them. One player takes a pawn of each colour and hides one in
each hand. The other player picks a hand and then plays that colour.

From the deck of cards, use one card to represent each piece, as shown in
appendix A. To match the pieces, you'll only need four pawns of each colour, so
you should end up with 24 cards.

Put the rest of the cards away, you won't need them. Separate the cards by
colour, give the black cards and pieces to the white player and the white cards
and pieces to the black player. Each player should shuffle their cards face
down without looking at them.

### Goal
Get more of your pieces stacked at the bottom of the board, and stack them in
higher rows for more points.

### Play
Each turn has three phases:

1. **Flip** a card for your opponent.
2. **Move** all your active pieces, so they end up at least one row closer to
   the bottom. However, you may capture a piece in the same row.
3. **Add** your opponent's piece that matches the card to the top row in any
   column.

#### Moving Pieces
Each turn, you must move all your active pieces, unless they are blocked by
another piece or stacked on the bottom. Stacked pieces are explained below. When
you move a piece, gravity pulls it down, so that the only legal moves are ones
that end up at least one row closer to the bottom. There's an exception for
captures: you may capture an opponent's piece with a legal move that ends on the
same row or any row closer to the bottom. You may not capture stacked pieces, as
explained below.

Pawns may either capture one space diagonally downward or move one space
downward to an empty square. On their first move, they may move two spaces
downward if both squares are empty.

White has no active pieces on the first turn, so has nothing to move.

In this example, White has just flipped a black rook card, and has to choose
which order to move their pieces.

    . . . . P . . .
    . . . . B . . .
    r . . . P . . .
    . n . . b . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    margins: 0, 0, 4.5, 0
    card: back, 8.5, 0.5
    card: r, 10.75, 0.5
    card: back, 8.5, 4.5
    card: P, 10.75, 4.5

If they move their bishop first, then the top pawn can also move.

    . . . . . . . .
    . . . . P . . .
    r . . . P B . .
    . n . . b . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    margins: 0, 0, 4.5, 0
    card: back, 8.5, 0.5
    card: r, 10.75, 0.5
    card: back, 8.5, 4.5
    card: P, 10.75, 4.5
    arrow: e8, e7, white
    arrow: e7, f6, white

If they move the top pawn first, they would say "This pawn can't move," and then
move the bishop. Either way, the lower pawn can't move.

#### Stacked Pieces
If a piece reaches the bottom row, it becomes stacked, and can't be moved or
captured. If all possible downward moves for a piece are blocked by stacked
pieces, then that piece is also stacked, and can't be moved or captured.

In this example, the two pieces on the bottom row are obviously stacked, but
the only one stacked in the second row is the rook. The bishop can move down to
h1, and the queen can move down to any of the three squares below it. If the
rook weren't between them, the queen could capture the bishop, because it's not
stacked. However, it can't capture the stacked rook.

    p . . . . . . N
    q . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . B . . . .
    . . Q . . r b .
    . . . . . r n .
    margins: 0, 0, 4.5, 0
    card: back, 8.5, 0.5
    card: p, 10.75, 0.5
    card: back, 8.5, 4.5
    card: N, 10.75, 4.5

### Game End
Turns continue until Black adds the last white piece, then White gets one last
turn without flipping a card or adding a piece.

Count points for each player's stacked and captured pieces. A captured piece
is worth one point. A stacked piece on the bottom row is worth one point, on the
second row is worth two points, and so on. The player with the most points wins.
In case of a tie, look at the highest row with stacked pieces. The player with
the most stacked pieces in that row wins. If still tied, continue looking at the
next row down until you find a difference. If all rows are tied, the game is
tied.

In this example, the unstacked pieces have arrows showing all possible downward
moves.

    . . . . . . . .
    . . . . . . . .
    . . . . . . R .
    . . . . . . . .
    . P . . . . . p
    . b . . k . K N
    N . R . B r . .
    p . n Q q r n b
    margins: 0, 0, 4.5, 0
    card: back, 8.5, 0.5
    card: r, 10.75, 0.5
    card: back, 8.5, 4.5
    card: P, 10.75, 4.5
    arrow: e3, d2, black
    arrow: g3, g2, white
    arrow: g3, h2, white
    arrow: g6, g3, white

To calculate the score, count the pieces. White has 2 captured pieces for 2
points, 1 stacked piece on the bottom row for 1 point, 3 stacked pieces on the
second row for 6 points, 1 stacked piece on the third row for 3 points, and 1
stacked piece on the fourth row for 4 points. Black has 4 captured pieces for 4
points, 6 stacked pieces on the bottom row for 6 points, 1 stacked piece on the
second row for 2 points, 1 stacked piece on the third row for 3 points, and 1
stacked piece on the fourth row for 4 points. That makes a total of 16 for White
and 19 for Black, so Black wins.

## Parade Chess Solitaire
Half the chess pieces are on parade, giving each other orders, and they have to
form up into one connected group. Keep adding pieces until you have enough to
start, but you get more points for fewer pieces making fewer moves.

### Equipment
A standard chess set and a standard deck of 52 cards.

### Setup
Place all the chess pieces except the pawns beside the board. Put the pawns
away, you won't need them.

From the deck of cards, use one card to represent each piece, as shown in
appendix A. You don't need the pawn cards, so you should end up with 16 cards.

Put the rest of the cards away, you won't need them. Then shuffle the cards and
deal them into two piles of eight next to the board. From one of the piles, draw
one card at a time, placing the matching piece on the board. Starting at a1
through h1, then a2 through h2, and so on until you've placed eight pieces on
the board. The table in appendix A shows how big a gap to leave before each
piece. That is, how many empty squares to leave before placing each piece.

Here's an example with all the cards laid out in the order they were drawn, from
the 9 and 10 of hearts to the 9 of spades. Check to make sure you agree with
where the pieces were placed.

    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . r . . b . . .
    . r . n . N . .
    . . . . . k . .
    . . B . . . R .
    margins: 0, 0, 4, 0
    card: B, 8.5, 0
    card: R, 9, 0
    card: k, 9.5, 0
    card: r, 10, 0
    card: n, 8.5, 1
    card: N, 9, 1
    card: r, 9.5, 1
    card: b, 10, 1

### Play
Take the remaining stack of eight cards, and spend them on actions to bring the
chess pieces together. Each card can be spent on one of two actions:

1. **Move** a piece. Take the top card from your deck and play it face down next
   to the discard pile from the setup phase. Then use one of the pieces on the
   board to move another piece. A piece can move any piece of the opposite
   colour from a square that it could attack in regular chess. Pick up the piece
   that you want to move, and then place it in another square that piece moving
   it could attack. For example, black knight at d3 could move the white bishop
   from c1 to b2, e1, f4, e5, or c5. The king could move either of the white
   pieces next to it to any of the other spaces next to it.
2. **Add** a piece. Take the top card from your deck and play it face up onto
   the discard pile from the setup phase. Add the piece as in the setup phase,
   leaving the regular gap after the piece that is in the occupied rank farthest
   from 1 and in the rightmost file of that rank. In the example above, if you
   played the 8 of diamonds, you would play a white knight at g7 to leave a
   one-square gap after the black bishop.

Here's an example of using the black bishop at e4 to move the white knight from
f3 to g2:

    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . r . . b . . .
    . r . n . . . .
    . . . . . k N .
    . . B . . . R .
    margins: 0, 0, 4, 0
    arrow: e4, f3, black
    arrow: e4, g2, black

### Winning
If you can get from any piece to any other piece on the board only stepping on
neighbouring pieces, then you have formed one connected group and you win.
Diagonal neighbours don't count. Count how many cards you have left in your
hand, and that's how many points you win.

If you run out of cards before you form one connected group, pick up all 16
cards, and use them to count negative points until you form a connected group.
You may only move pieces and not add any.

# Broken Games
These ideas seemed promising, but didn't work at the table. Maybe I'll come back
to them, if I get inspired. Masquerade Chess seemed broken for 15 years, before
I had the idea to hide only the capture moves.

## Booster Chess
Start every game with a booster pack of cards to make your pieces better or
hobble your opponent's pieces.

This was an attempt to add the chaos of cards to Adrenaline Chess, but players
would often get good enough cards that they could stomp their opponent in under
ten moves. It also ended up feeling too similar to Adrenaline Chess. I solved
both problems by dropping the boost and keeping only the hobble to make Tar Pit
Chess.

### Equipment
A standard chess set, a standard checkers set, and a standard deck of cards.

The checkers must be stackable, and you must be able to stack a chess piece on
top of the checkers. Coins or poker chips would also work, as long as they fit
inside the chess board squares. You need 6 each of 2 colours.

From the deck of cards, use one card to represent each piece, as shown in
appendix A. You also need two cards of each colour to represent checkers, so add
the sixes to the deck. That should make 36 cards in total, put the rest of the
deck aside.

### Setup
Set up the chess pieces in the standard start position, and randomly choose who
will play white. Place 6 light checkers in front of White and 6 dark checkers in
front of Black. You won't need the rest of the checkers, so put them aside.

Shuffle the deck and deal 6 cards to each player. Look at your cards, but don't
show them to your opponent. Place the rest of the cards in a draw stack.

### Play
Your turn has up to four parts:

* You must **move** a chess piece.
* If you moved a boosted piece, you may **spend** checkers to also move it like a
  king.
* You may **add** a checker, by playing a card.
* Finally, **draw** cards until you have one card for every checker in front of
  you.

Chess pieces move normally, unless they are stacked on checkers. Pieces on
checkers are modified as follows:

* Your piece on your checker is boosted: after moving it normally, you may move
  it like a king, one space in any direction. If you make the king's move,
  remove the checker and place it in front of you. If the piece is on more than
  one checker, you may continue spending checkers to make more king's moves on
  the same turn.
* Your piece on your opponent's checker is hobbled: pawns cannot move at all,
  and other pieces move like pawns. If it is on more than one checker, it's
  still hobbled, but no worse.

If one of your pieces is on a black and a white checker, immediately remove one
checker of each colour and return them to their owners. Keep removing pairs of
black and white checkers, if there are more.

When you move a piece, it brings any checkers along with it, except a spent
booster.

#### Adding and Capturing Checkers
After you finish moving, you may play one of your cards to add a checker. You
may only add checkers of your own colour, and you may add one to a piece that
matches the card.

Checkers cards match any piece of that colour, so you may use a black checker
card to add one of your checkers to any black piece or use a white checker card
to add one of your checkers to any white piece. If there are no pieces left on
the board to match a card, you may use it to add one of your checkers to any
piece of the card's colour, just like a checkers card.

Play your card to a discard pile next to the draw pile, and shuffle the discard
pile to make a new draw pile if it runs out.

When you capture a piece, your piece keeps any checkers that the captured piece
was stacked on. Capturing a boosted piece leaves you hobbled, but capturing a
hobbled piece leaves you boosted! Don't forget that opposite colour checkers
immediately cancel each other and get returned to their owners.

Besides neutralizing a hobble checker by adding one of your own, there is
another way to remove it: get it to the back rank of the board. If you do, just
remove the hobble checker and return it to your opponent.

#### Drawing Cards
After moving a piece and possibly playing a card, draw cards until you have the
same number of cards as checkers off the board. In practice, this means that
you only draw if you spent a booster checker or received a hobble checker from
your opponent.

#### Special Cases
You may not castle, if either the king or the rook is boosted. During castling,
you may not move your king through squares that could be attacked by booster
moves. You may not move a piece to reveal a check on your king, even if you then
use a booster move to block the check again.

Hobbled pieces move like pawns, but do not move two spaces on their first move.
You may capture a pawn en passant at the usual square after a regular move of
two squares. You may not capture en passant if the pawn used a booster move, and
you may not use a booster move to capture en passant. A pawn that moves to the
back rank immediately promotes, and may continue making booster moves if it is
still boosted.

### Winning
Win by checkmate, as in regular chess, but you may use booster moves to threaten
the king.

### Variants
Make the game more predictable by using fewer checkers cards in the deck or
fewer checkers during setup. Make it less predictable by using more. Handicap a
player by giving them fewer checkers than their opponent. During setup, always
deal one card for each checker.

## Neighbour Chess Solitaire
Pairs of chess pieces help each other across the board until you gather them all
into one connected group. Keep adding pieces until you have enough to start, but
you get more points for fewer pieces making fewer moves.

This game might not be broken, but it inspired Chess Golf, and they're too
similar to keep both.

### Equipment
A standard chess set and a standard deck of 52 cards.

### Setup
Place all the chess pieces except the pawns beside the board. Put the pawns
away, you won't need them.

From the deck of cards, create two smaller decks. The first is a deck of 16
cards for the chess pieces, as shown in appendix A. You don't need the pawn
cards.

The second is a deck for the positions on the board: 2 - 6 of Hearts, Diamonds,
Spades, and Clubs.

Put the rest of the cards away, you won't need them. Then shuffle each deck and
place them next to the board as the two draw piles.

### Play
In the first part of the game, you add pieces to the board, as directed by the
two decks of cards.

1. Flip over the top card of the pieces deck and place it on a discard pile.
2. Take the piece that matches that card, and hold it above the board. If it's
   the first piece, hold it above the bottom left corner. Otherwise, hold it
   above the last piece you added. (Check the discard pile, if you forget which
   piece you added last.)
3. Flip over the top card of the positions deck and place it on a second discard
   pile.
4. Now move the piece from the square it's above to a new square and add it to
   the board. If the position card is a red card, move the piece that many
   squares to the right, otherwise move the piece that many squares up. If you
   move off the edge of the board, loop around to the opposite side and keep
   counting.
5. If the space you move to is occupied, you may move to any of the 8 neighbour
   spaces. If all of them are occupied, you may move to any of their neighbours,
   and so on. You may not wrap around the edge of the board in this case, so
   edges and corners have fewer than 8 neighbours.

After adding any piece, you may choose to stop adding and try to move the pieces
into one connected group.

1. Before each move, spend a card from one of the draw piles to a discard pile.
2. Then move one of the chess pieces. However, it doesn't use its usual move.
   Instead, use the move of one of its neighbours of the same colour in the 8
   squares around it. If a piece has no neighbours of the same colour, it cannot
   move.

### Winning
If you can get from any piece to any other piece on the board only stepping on
neighbouring pieces, then you have formed one connected group and you win. Count
how many cards you have left in the two draw piles, and that's how many points
you win.

## Cloak and Dagger Chess
Pawns are played as usual, but all other pieces are replaced by numbered
checkers. Players have to deduce which of their opponent's pieces are which, and
then capture the king.

### Setup
Place all the pawns in their regular position, then use tape or stickers to
write the numbers 1 to 8 on checkers for each player. Put the black checkers on
black's back row and the light checkers on white's back row. Finally, write two
grids like this to secretly record your pieces and deduce your opponent's:

    type: cloak
    . 1 2 3 4 5 6 7 8
    K
    Q
    R
    B
    N

Obviously, you don't have to put the pieces in their standard starting
positions, but you do have to have a standard set of pieces. (You can't give
yourself three queens!) You also have to follow the same restrictions that
Chess960 puts on its random starting positions:

* Place your king somewhere between your two rooks.
* Place one of your bishops on a light square and one on a dark square.
 
Write a circle for each piece you know, and an X for each piece you
know is impossible. You might want to write X's for your own pieces as your
opponent learns which of your combinations are impossible.

Here's one possible way to fill in your grid at the start of the game:

    type: cloak
    . 1 2 3 4 5 6 7 8
    K . . O
    Q . O
    R O . . O
    B . . . . O O
    N . . . . . . O O

At the start of your turn, you may guess the identity of one of your opponent's
checkers. If you guess correctly, you may make a bonus move after your regular
move. Your bonus move may be either a regular pawn move or to take back a pawn
that your opponent captured and drop it on an empty square in your second rank.
If you guess incorrectly, your opponent may make the same kind of bonus move
before their next turn.

At the end of your turn, you may replace any number of your checkers with their
uncloaked chess pieces.

If one of your checkers is captured, tell your opponent which piece they
captured.

### Winning
Win by capturing a cloaked king or putting an uncloaked king in checkmate. You
might have to uncloak some of your pieces to show the checkmate.

A cloaked king may move into check, stay in check, or castle out of check,
because the opponent doesn't know it's in check. Castling is the same as in
Chess 960: the king and rook end up on the same squares they do in standard
chess. All spaces between their start position and their end position must be
empty, except for the king and the castling rook. All spaces between the king's
start and end positions must not be under attack, if the king is uncloaked.

### Design Problems
Because you don't know how your opponent's pieces capture, you never know if
you're safe. You're not even safe from the pawns, because your opponent can
sometimes make two pawn moves.

Maybe it's too similar to Masquerade Chess to begin with.
