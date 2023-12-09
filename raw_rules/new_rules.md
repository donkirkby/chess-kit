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

## Adrenaline Chess
What if taking your opponent's piece frightened the others so much that they
became more aggressive? Every time you take a piece, you have to choose one of
the remaining pieces to get an adrenaline rush, and adrenaline can make any
piece a king. This game adds a little chaos to chess, and accelerates the end
game.

### Equipment
A standard chess set and a standard set of 24 checkers. The checkers
must be stackable, and you must be able to stack a chess piece on top of the
checkers. Coins or poker chips would also work, as long as they fit inside the
chess board squares.

### Setup
Set up the chess pieces in the standard start position, and randomly choose who
will play white. Place the checkers beside the board.

### Play
All the regular chess rules apply, plus you must give an adrenaline rush after
captures. If you captured one or more pieces, end your turn by placing a
checker under one of your opponent's remaining pieces. The colour of the
checker doesn't matter, and you may stack multiple checkers under a piece.

In the following example, white just captured a pawn with the bishop, and
finishes the turn by adding a checker under the pawn at h7.

    r n b q k b n r
    . p p p p p p p
    B . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . P . . .
    P P P P . P P P
    R N B Q K . N R
    arrow: f1, a6, white
    arrow: h7, h7, gray

To move a piece with checkers under it, you must make a regular move for that
piece, and bring the checkers along. Then you may use up one of the checkers
under that piece to make an extra move like a king. Remove a checker from the
stack, and move the rest one space in any direction. If that piece still has
checkers under it, you may continue making extra king moves until the piece
runs out of checkers.

The extra moves may capture pieces, but you only ever add one checker per turn.
When you capture an opponent's piece, your capturing piece keeps any adrenaline
the captured piece had, and may immediately use the adrenaline.

For example, here is a strange checkmate that uses white's adrenaline to
threaten the white king. Black has just captured a pawn, and has spent the last
few turns pumping a trapped bishop full of adrenaline. Adding a third checker
to the stack at c1 would seem to make the bishop a threat to the black queen,
but it must make a regular move before it can start using the adrenaline. White
has been forced to keep the king retreating, and hasn't been able to move the
pawns that would free the bishop. The black queen on the other hand, will be
able to capture the bishop on the next turn, and then use those three checkers
to capture the king at f2, possibly capturing the pawn at d2 along the way.
Moving the king to e1 or e3 would still be in range for the queen. e2 would be
a direct capture by the queen, f1 and f3 could be captured by the queen or the
black bishop. g3 might give a glimmer of hope, until you notice that the black
pawn at h5 has a checker. It is checkmate.

    r n . . k . n r
    . . . . . p p .
    . . . . p . . .
    . . . . P . . p
    . p q . . . . .
    P . . . . . . .
    . P . P b K P P
    R . B . . . Q .
    arrow: g4, e2, black
    arrow: c1, c1, gray
    corner text: 3, 3, 1
    arrow: e5, e5, gray
    arrow: e6, e6, gray
    arrow: h5, h5, gray
    arrow: g7, g7, gray

After castling, you may use both the king and the rook for extra moves, if they
both have checkers. You may capture a pawn en passant on the second rank at the
usual square after a regular move of two squares. You may not capture en passant
at a square that the pawn left using an extra move, and you may not use an extra
move to capture en passant. A pawn that moves to the back rank immediately
promotes, and may continue making king moves if it still has checkers. You may
not move a piece to reveal a check on your king, even if you then use an extra
move to block the check again.

### Winning
Win by checkmate, as in regular chess, but you may use extra moves to threaten
the king.

## Cooperative Chess
If you don't like battling your friend across the board, you can team up against
the game itself. A hand of cards limits what you can capture, and you work
together to eliminate as many *types* of pieces as you can.

### Equipment
A standard chess set and 32 cards from a standard deck of 52 cards. You will use
cards to match the chess pieces, as shown in appendix A.

### Setup
* One player **stands** the chess pieces in the standard start position.
* Meanwhile, the other player **shuffles** the 32 cards,
* **deals** 3 to each player, and
* **places** the rest of the cards next to the board as a draw pile.
* When the chess pieces are set up, the first player secretly places a white
  pawn in one hand and a black pawn in the other. The other player then
  **chooses** a hand to decide their colour.

### Play
White plays the first turn, and then players alternate. Each turn has four
possible steps, in this order:

1. You may make a **non-capturing** chess move.
2. You must **play a card** from your hand to your discard stack.
3. You may make multiple **capturing** chess moves, if the cards allow.
4. You must **draw a card** to bring your hand back to 3.

As the game progresses, you will move the cards between three face-up,
spread-out stacks of cards: White's discards, Black's discards, and the captured
cards. It's best to spread the cards enough that you can see which cards have
already been played.

The chess pieces make the same moves as in regular chess, but you can only
make a capture if the cards match:

1. The **capturing** piece must be the same piece type as the card that the
   capturing player just played, and
2. the **captured** piece must be the same piece type as the top card on the
   other player's discard stack.

Pieces may match cards of either colour. On each turn, all moves must be made
with one piece.

When you capture a piece, remove the piece from the board, and move the captured
piece's card from your partner's discard stack to the captured cards stack. If
you can make another capture move that matches the next card in your partner's
stack, you may continue.

There are two types of **wild** cards that can match any piece type. They may
match different piece types when they capture and when they are captured.

1. If you no longer have any pieces of a certain type, then that type of card is
   wild on your discard stack. For example, if you have no queen, then a queen
   card on your stack lets you capture with any piece and lets your partner
   capture any of your pieces.
2. A double colour match makes the next capture wild. If both the capturing
   piece and the captured piece match the colour of their cards, then the next
   captured card becomes wild, as long as you can capture it in the same turn.
   White pieces match red cards.

Castling is allowed. En passant capture is allowed. You may promote a pawn on
the last rank to any other piece. It can be an effective way to get rid of your
last pawn. You may move a king into check or leave it in check.

### Winning
The game ends immediately when you capture a king. You then get a point for each
piece type that was completely removed from the board, both colours. For
example, if you captured both queens, all four bishops, and a king, but still
had at least one pawn, one knight, one rook, and the other king still on the
board, then you would score 2 points.

If the draw pile is empty, continue playing until you run out of cards in your
hands. If you run out of cards without capturing a king, you lose.

### Talking
The game works best if players know something about each other's cards, but not
everything. They should feel free to ask each other yes or no questions about
their hands and to discuss general strategy, but shouldn't just reveal their
hands.

## Half Alice Chess
Alice Chess is a popular variant invented by Vernon Parton in 1953, usually
played with one set on two boards. Since I wanted all the games in this
collection to be playable with one chess set, I found a way to play it on one
board by placing the mirror pieces on checkers. I'm not the first to suggest
this idea, but I think it makes it easier to see the connections between the two
sets of pieces.

The main idea is that pieces switch back and forth between the two sides of a
mirror, as in Lewis Carroll's "Alice Through the Looking Glass". This causes
many surprising positions and interactions, well worth exploring.

### Equipment
A standard chess set and a standard checkers set. For full compatibility with
the original rules, you'd need 16 checkers of each colour, but I think it's
unlikely you'd ever need more than the standard 12.

### Setup
Place the chess pieces in their standard opening position, give the light
checkers to White and the dark checkers to Black.

### Play
Pieces not on checkers are on one side of the mirror, pieces on checkers are on
the other side of the mirror. Rules are as in orthodox chess, with these
changes:

* The move must be legal under orthodox chess rules.
* Switch the moved piece to the other side of the mirror after it moves. (Add or
  remove a checker.)
* Pieces cannot capture pieces on the other side of the mirror, but they can
  move through squares that are occupied by pieces on the other side of the
  mirror.
* If you're playing with 12 checkers each, then you must have a free checker in
  order to move piece without a checker.

### Winning
Place the opponent's king in checkmate. A king may not evade check by switching
to the other side of the mirror, because the move must be legal before the
switch.

In this example, the king cannot move to a8, because it would still be in check
by the queen before switching. It can't move to b7, because it would be in check
by the rook after switching. The only legal move is to a7.

    . k . Q . . . .
    . . . . . . . .
    . R . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . K
    arrow: b6,b6,white

## Chess Golf
Pairs of chess pieces caddy for each other, while all the players try to work
out the most efficient path to deliver a golf ball across the board.

### Equipment
A standard chess set and a standard deck of 52 cards. You'll also need a pencil
and paper for keeping score, a timer, and some coins. 4 coins are probably
enough, and you can even play without them. A one-minute timer works well,
although anything from 30 seconds to two minutes would be fine.

### Setup
Place all the chess pieces except the pawns beside the board. Put the pawns
away, you won't need them.

From the deck of cards, use one card to represent each piece, as shown in
appendix A. You don't need the pawn cards, so you should end up with 16 cards.

Put the rest of the cards away, you won't need them. Then shuffle the cards and
place them next to the board. Draw one card at a time, placing the matching
piece on the board. Starting in the top left corner, leave the following numbers
of empty squares before each piece:

* Kings - 6 empty squares
* Queens - 5 empty squares
* Rooks - 3 empty squares
* Bishops - 2 empty squares
* Knights - 1 empty square

Shuffle the cards again, and place them next to the board as a draw pile.

Choose a scorekeeper, and get them to write everyone's initials at the top of
the paper, leaving enough room for 9 scores and a course total. Leave room for
18 scores, if you're playing a full round.

### Play
Each turn, **draw** two cards and place them face up next to the board where all
players can see them. Check appendix A if you need to, and **announce** the two
chosen piece types for this turn. Then **start** the timer.

All players now plan how to get one of the two pieces to hit a golf ball at the
other in the fewest strokes. While planning, no one actually moves the pieces.
For each stroke, choose a piece to hit a golf ball. They can hit a golf ball
to land one chess move away. However, they don't use their own type of move.
Instead, they pick one of their neighbouring pieces as a caddy and use the
caddy's golf club to move the ball with the caddy's chess move.

If one of the two chosen piece types can hit a ball to the other chosen piece
type, then that's the final stroke and no pieces move. Otherwise, the ball has
to land in an empty square, and the piece that hit it moves to the empty square.
The caddy doesn't move. Remember, though, don't actually move any pieces while
planning. Just visualize how the pieces will move and count how many strokes you
need to deliver the ball.

One extra restriction: all white pieces are right handed, and can only use
right-handed, white caddies. All black pieces are left handed, and can only use
left-handed, black caddies. Caddies must be in one of the 8 squares directly
surrounding the piece.

If no black pieces have caddies or no white pieces have caddies at the start of
the game, start at the kings and work your way down to the knights. If swapping
a black and a white piece would make it so that there is at least one caddy pair
of each colour, then make the swap and stop.

You may move other pieces besides the two chosen piece types. This is often
helpful if the chosen pieces have no neighbours.

When you have found a path and counted the strokes, put your fist on the table
to show that you're ready. When all the players have a fist on the table or
when the timer runs out, the planning phase ends.

Now, everyone reveals their stroke count at the same time. Bang your fist on the
table as you count "one, two, three." As you say "three," everyone puts out a
number of fingers to show how many strokes they need. The scorekeeper writes
down everyone's strokes. If you think it's impossible, put out zero fingers.

The player with the fewest strokes must now demonstrate the path. If some
players are tied for fewest, start with the scorekeeper and go around to the
left until you reach one of the tied players. That player must demonstrate. It
can be helpful to start by placing coins under all the pieces that you're going
to move, so you can reset if you get confused.

Players should not be allowed to hesitate more than a few seconds while
demonstrating. Be kind, especially to younger players, but you can't sit and
try to solve it at this point.

If the player can't demonstrate their path, then they get the maximum of all the
other players' strokes, plus a one-stroke penalty. Reset the pieces to where
they started and get the player with the next lowest strokes to demonstrate.

If some players put out zero fingers, let the lowest nonzero player demonstrate.
If they are successful, then all the zero players get the maximum strokes plus
a one-stroke penalty.

After a successful demonstration, leave the pieces in their final positions, but
remember that the last stroke only delivers the ball without moving the piece.
Remove the coins, if you used them. Choose a new scorekeeper by passing the
pencil and paper one player to the left.

### Game End
Continue drawing two cards each turn until the deck runs out. For the ninth
hole, use the two kings. If you want to play a full round, shuffle the cards and
play the back nine holes. You don't need to lay out the pieces again.

Add up the scores for all 9 or 18 holes, and award the game to the player with
the lowest score. A tie goes to the best dressed player.

## Neighbour Chess Solitaire
Pairs of chess pieces help each other across the board until you gather them all
into one connected group. Keep adding pieces until you have enough to start, but
you get more points for fewer pieces making fewer moves.

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

# Broken Games
These ideas seemed promising, but didn't work at the table. Maybe I'll come back
to them, if I get inspired. Masquerade Chess seemed broken for 15 years, before
I had the idea to hide only the capture moves.

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

## Appendix A
These diagrams show which playing cards represent each chess piece in several
games. Red cards represent white pieces, and black cards represent black pieces.
If you don't mind defacing a deck of cards, you can add the letter or symbol for
the pieces just below the suit symbol in the corners, pressing lightly to avoid
marking the back of the cards. Otherwise, remember how the numbers correspond to
the pieces in this appendix. To start with, the pawns match the small numbers:
2 to 5.

    P P . . . . p p
    P P . . . . p p
    P P . . . . p p
    P P . . . . p p
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    card: 2H, 2, 0
    card: 2D, 2.5, 0
    card: 2S, 3.5, 0
    card: 2C, 4, 0
    card: 3H, 2, 1
    card: 3D, 2.5, 1
    card: 3S, 3.5, 1
    card: 3C, 4, 1
    card: 4H, 2, 2
    card: 4D, 2.5, 2
    card: 4S, 3.5, 2
    card: 4C, 4, 2
    card: 5H, 2, 3
    card: 5D, 2.5, 3
    card: 5S, 3.5, 3
    card: 5C, 4, 3

The non-royal pieces match the high numbers, ordered by strength. The knights
match 8s and the bishops match 9s.

    N N . . . . n n
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    B B . . . . b b
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    card: 8H, 2, 0
    card: 8D, 2.5, 0
    card: 8S, 3.5, 0
    card: 8C, 4, 0
    card: 9H, 2, 4
    card: 9D, 2.5, 4
    card: 9S, 3.5, 4
    card: 9C, 4, 4

The rooks match 10s, and the royal cards match the obvious queens and kings of
hearts and spades.

    R R . . . . r r
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    Q . . . . . . q
    K . . . . . . k
    . . . . . . . .
    . . . . . . . .
    card: 10H, 2, 0
    card: 10D, 2.5, 0
    card: 10S, 3.5, 0
    card: 10C, 4, 0
    card: QH, 2, 4
    card: QS, 4, 4
    card: KH, 2, 5
    card: KS, 4, 5
