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

## Telepathy Chess
I like the idea of two players working together, and trying to predict what
their partner will do. You can decide how much talking to allow. Definitely none
before your move, but it can be more fun to discuss what you thought your
partner would do after they move and before your opponents move.

### Equipment
* a standard chess set
* a standard deck of 52 cards, or a deck of chess cards
* a coin or checker

### Setup
Place two white pawns and two black pawns in a bag, box, or cupped hands so the
other players can't see them. Have each player draw a pawn without looking to
decide which two will play white and which two will play black. Teams can then
decide which player will predict first and which will move first.

Set up the chess pieces in the standard start position. Both members of the
white team sit on the side of the board with the white pieces, opposite both
members of the black team. Place the coin or checker beside the board, halfway
between the two teams.

If you don't have a deck of chess cards, see Appendix A for how a standard deck
of cards can represent the chess pieces. Give each team a set of seven cards:
pawn, knight, bishop, rook, queen, king, and checker. The predictor for each
team should take the cards in their hand, and play the pawn face up on their
side of the board.

### Play
Players take turns being the mover and the predictor, handing the cards back and
forth to keep track of who will play a prediction card next turn.

On your team's turn, the predictor will play a card face down, next to the
face-up card. The piece cards predict that their partner will play the matching
piece, and the checker card is like a copy of the face-up card. (Think of C for
checker and C for copy.)

Then the mover makes any legal chess move.

The predictor flips the face-down card to show what they predicted. If the mover
moved a piece type to match the card that was face down, push the coin or
checker toward your opponents. If they moved a piece type to match the card that
was face up, do nothing. If they didn't match either piece type, pull the coin
or checker towards you.

The coin or checker can be in three positions: beside the middle of the board,
the white side, or the black side. If you have to push or pull it beyond those
positions, the losing team has to remove one of their pieces, and then place it
back in the middle position. For example, if it was beside the black side of the
board and the black mover didn't match either card, the black team would have to
remove one of their pieces from the board. After removing a piece, put the coin
or checker back beside the middle of the board.

After moving a piece, and resolving the prediction, the mover takes the hand of
cards and picks up one of the cards from the table. If one of them is a checker
card, pick it up. Otherwise, pick up the card that started the turn face up.

### Winning the Game
Capture the opponent's king to win the game. Because a piece is sometimes
removed after the regular move, it may be possible to capture a king when they
weren't in check. You should still say "check," when a piece is threatening the
king.

### Design Questions
Is the catch-up mechanism too strong? Does it become too easy to predict when
you only have pawns and a king?

Alternate end when you have forced six removals? Captured all major pieces?

Make predictions harder when you only have two or three types of pieces? (No
face-up card.)

Would strategy advice be helpful? Forcing king moves is usually good in regular
chess, but here it makes your opponents' prediction much easier. Playing to a
slightly weaker position that has three good responses can be better than the
stronger position with one obvious response. You might sometimes want to predict
incorrectly to remove a piece that frees up a stronger piece, like a rook.

## Split-Brain Chess
This is another chess game for four players, this time more chaotic than Crowded
House. The players each have to contribute half the move, but it gets messy when
they don't agree.

Because chaos is frustrating in a long game, I wanted to base it on a simplified
version of chess that plays more quickly. I chose Los Alamos chess, which is a
simplified set of rules used by the first computer chess program, when computers
weren't powerful enough to play regular chess.

### Design Questions
1. Los Alamos chess, or Tic Tac Chec?
2. Is it more fun for the mover to draw a movement vector, instead of circling a
   target? It's definitely simpler to circle a target.
3. Is it more fun to let the opponents choose whether piece or target is
   flexible?

### Equipment
A standard chess set, a checker or a coin, plus a piece of paper, a pen, and a
pencil for each player.

### Setup
Los Alamos chess is played on a 6x6 board, without bishops, so put the bishops
aside, along with two pawns of each colour. You can use a regular chess board,
just don't use the squares along all four edges. Place the checker or coin in
the black king's corner. The checker reminds players to ignore the outer
squares, and also reminds players about the movement rules, described later.
That leaves you with this starting position:

    . . . . . . . .
    . r n q k n r .
    . p p p p p p .
    . . . . . . . .
    . . . . . . . .
    . P P P P P P .
    . R N Q K N R .
    . . . . . . . .
    arrow: h8, h8, black

Put the two extra pawns of each colour in a bag or box, and let each player take
a pawn without looking to choose the colour they will play.

Each player should take a piece of paper, and write a 6x6 grid on it in pen.
Label one side with a W for White and the opposite with a B for Black.

### Play
The rules of standard chess apply, with these changes:

* Partners make a move together, as described in the next section.
* Pawns cannot move two squares on their first move.
* No castling.
* Pawns cannot promote to bishops.

### Making a Move
To make a move, one partner is the **chooser**, who chooses which piece to move.
The other is the **mover**, who decides where to move it. Each team has one
partner on the king side of the board and one on the queen side of the board.
The partner on the same side as the **ch**ecker is the **ch**ooser.

Starting with the two white players, they both shield their paper grids from
each other with a hand or a book, and circle a square in pencil. The chooser is
circling the piece they choose to move, and the mover is circling the target
square they want to move it to. Once they've both circled a square, they reveal
their grids.

If the chosen piece can legally move to the target square, the white mover makes
that move. If not, the black chooser chooses whether white must use the chosen
piece or the target square. If they choose the piece, then the white mover must
make a legal move with that piece. If that piece has more than one legal move,
they must make the one that ends closest to the target square. If the black
chooser chooses the target square, then the white chooser must choose a piece
that can legally move to that square and move it there. If more than one piece
can legally move to that square, they must choose the one that is closest to the
one they originally chose.

When choosing the closest square or the closest piece, use "Manhattan distance",
or the number of steps between squares without making any diagonal steps. If
more than one choice is the same distance, players may use whichever they
prefer.

While writing down their moves, players must follow these rules:

* They may not say anything or look at their partner's paper.
* The chooser must circle a square that has one of their pieces on it, and that
  piece must have a legal move.
* The mover must circle a square that at least one piece can legally move to.
* If either player circles an invalid square, they must circle the nearest valid
  square instead. If more than one valid square is the same distance, the
  opponents' chooser may choose which one to use.

After the white team finishes their move, the black team uses the same steps to
make a move. After the black team finishes their move, they slide the checker
from the king's corner to the queen's corner, or vice versa. Then the steps
repeat.

### Winning the Game
As in regular chess, put the opponent's king in checkmate to win the game.

## Cooperative Chess 2
If you don't like battling your friend across the board, you can team up against
the game itself. A line of cards limits what you can capture, and you work
together to capture as many pieces as you can, with bonus points for each *type*
of piece you eliminate.

### Equipment
A standard chess set and a deck of chess cards. (See how to turn standard
playing cards into chess cards in appendix A.)

### Setup
* One player **stands** the chess pieces in the standard start position.
* Meanwhile, the other player **shuffles** the 32 cards,
* **deals** 2 to each player, and
* **places** the rest of the cards next to the board as a draw pile.
* When the chess pieces are set up, the first player secretly places a white
  pawn in one hand and a black pawn in the other. The other player then
  **chooses** a hand to decide their colour.

    r n b q k b n r
    p p p p p p p p
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    P P P P P P P P
    R N B Q K B N R
    margins: 0, 0, 6, 0
    card: back, 11.5, 0
    card: back, 12, .25
    card: back, 8.5, 2.5
    card: back, 11.5, 5
    card: back, 12, 4.75

### Play
White plays the first turn, and then players alternate. Each turn has four
possible steps, in this order:

1. You must **play a card** from your hand to a face-up line beside the draw
   pile. Add to the end away from the draw pile.
2. You may make a **non-capturing** chess move.
3. You may make multiple **capturing** chess moves, if the cards allow.
4. You must **draw a card** to bring your hand back to 2, unless the draw pile
   is empty.

If you ever draw or deal a **king** card, immediately add it to the face-up line
and draw a replacement card.

The chess pieces make the same moves as in regular chess, but you can only
make a capturing move if a card like the **capturing** piece is beside a card
like the **captured** piece in the face-up line.

When you capture a piece, remove the piece from the board, and move the captured
piece's card from the face-up line to the discard pile. If you can make another
capturing move that also follows the rule above, you may continue, even by
moving a different piece.

As an example, imagine that Black has a black knight card and a white pawn card
in hand with the following position:

    r n b q k b n r
    p p p . p p p p
    . . . . . . . .
    . . . P . . . .
    . . . . P . . .
    . . . . . . . .
    P P . P . P P P
    R N B Q K B N R
    margins: 0, 0, 6, 0
    card: back, 8.5, 2.5
    card: p, 11, 2.5
    card: P, 11.5, 2.5
    card: b, 12, 2.5

They can play their pawn card, move the bishop to e6, and then capture both
pawns. The bishop card is able to capture using the pawn card to its left and
the pawn card to its right. It could not continue to capture the pawn at g2,
because the remaining pawn card is black.

    r n . q k b n r
    p p p . p p p p
    . . . . . . . .
    . . . . . . . .
    . . . . b . . .
    . . . . . . . .
    P P . P . P P P
    R N B Q K B N R
    margins: 0, 0, 6, 0
    card: back, 8.5, 2.5
    card: p, 11, 2.5
    card: P, 11.5, 2.5
    card: b, 12, 2.5
    card: P, 12.5, 2.5
    arrow: c8, e6, black
    arrow: e6, d5, black
    arrow: d5, e4, black

After the captured cards are removed, only the black pawn and bishop cards are
left in the face-up line.

    r n . q k b n r
    p p p . p p p p
    . . . . . . . .
    . . . . . . . .
    . . . . b . . .
    . . . . . . . .
    P P . P . P P P
    R N B Q K B N R
    margins: 0, 0, 6, 0
    card: back, 8.5, 2.5
    card: p, 11, 2.5
    card: b, 12, 2.5

If White now has a white pawn, knight, bishop, or queen card, they can play that
and capture the black bishop. Otherwise, they can try to set up a future
capture.

You may only move a pawn to the last rank if it has a matching card in the
face-up line. Promote the pawn to any other piece type that has already been
captured. Move the pawn's card from the face-up line to the discard pile, then
find the promoted piece's card in the discard pile, and place it anywhere in the
face-up line. That can be an effective way to capture cards that are stuck
behind a king's card. If a pawn captures a piece as it moves to the back rank,
discard the captured piece's card as normal, then deal with the promotion.

Castling is allowed. En passant capture is allowed. All individual moves must
be legal chess moves, so you may not move a king into check or leave it in
check.

### Winning
The game ends immediately when you capture a king. You then get a point for each
piece that you captured, plus ten points for each piece type that was completely
removed from the board, both colours. For example, if you captured 23 pieces,
including both queens, all four bishops, and a king, but still had at least one
pawn, one knight, one rook, and the other king still on the board, then you
would score 43 points.

Anything lower than 32 points is a loss, anything higher than 50 points is
great!

If the draw pile is empty, continue playing until you run out of cards in your
hands. If you run out of cards without capturing a king, you lose.

### Talking
The game works best if players know something about each other's cards, but not
everything. They should feel free to ask each other yes or no questions about
their hands and to discuss general strategy, but shouldn't just reveal their
hands.

### Solitaire
To play solitaire, don't have any cards in your hand. At the beginning of each
turn, draw a card and add it to the face-up line.

### Design Questions
Should you have to play the kings immediately? Too fiddly and hard to remember?
Does the rule add tension?

Should you be allowed to move into check and leave a king in check? Is it easier
to just say all moves must be legal chess moves? Is it too easy to set up a king
capture and just work on capturing as many pieces as you can before you run out
of cards?

Should you be forced to capture a king if you can? Too fiddly and hard to
remember? Definitely don't want to force a noncapturing move that sets up a
capturing move, so is it easier to not force captures at all?


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

This is another game with a similar mechanic to Chess Golf, and it's a bit dry.

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
