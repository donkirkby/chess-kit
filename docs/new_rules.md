---
title: New Rules for Chess Kit
subtitle: Experiments in Progress
---
### Introduction
These are new games that aren't ready yet. You can try them out and let me
know what you think.

## Table of Contents
* [Crowded House][crowded-house] is the only four-player game I know
    of on a standard set. (4 players and chess set)
* [Cloak and Dagger Chess][cloak-and-dagger-chess] is a game where you
    disguise your chess pieces as checkers, then try to identify your
    opponent's pieces. (2 players, chess set, checkers set, pen, and tape)
* [Chess960][chess960] is a game designed by Bobby Fischer to mix up
    the game opening by randomly choosing your starting position. (2
    players, chess set, and deck of cards)

[crowded-house]: #crowded-house
[cloak-and-dagger-chess]: #cloak-and-dagger-chess
[chess960]: #chess960

## Crowded House
Two teams of two play, with each player moving the pieces of their colour
on the left or right half of the board. As usual, white moves first, then
alternates with black. Each king-side player takes the first move for their
team, then alternates with their partner. As an example, imagine Walter plays
king-side white, Winnie plays queen-side white, Betty plays king-side black, and
Bob plays queen-side black. Then the play order would be Walter, Betty, Winnie,
Bob, Walter, Betty, and so on.

### Rule changes
The key rule is that you can only move a piece that either starts or ends on
your side of the board. In this example, queen-side white may move the bishop as
shown, because it ends up on the queen side of the board. Moving the bishop to
e2 would not be allowed, because it would start and end on the king side.

![Diagram](images/new_rules/diagram1.png)

### Winning
Win by check mate, as usual, but remember that the next player on the attacking
team has to be able to make the capture.

The rest of the rule changes flow from whether a piece may be captured
immediately. A king may move into check or castle out of check, if the next
player can't make the capture. En passant capture only works if the pawn is
captured immediately after its first move.

### Talking
This is a silly game, so feel free to chat with your partner, but remember that
the other team is listening. Any discussion should be heard by both teams, so
no secret codes or second languages! Of course, players should also feel free to
ignore their partner's advice.

If partners are giving too much advice or want a more challenging game, add a
chess clock. Decide on an overall time, then decide on a time cost for talking.
As an example, you might play with a start time of 30 minutes and a 2-minute
bonus for each time your opponents talk. It's probably easiest to put a handful
of coins next to the board. Whenever your team discusses a move, either move a
coin from the centre to your opponents' pile or from your pile to the centre. If
a team runs out of time, they can add 2 minutes for each coin in their pile and
put their pile back in the centre. Once a team pays a coin, they can discuss as
much as they want until they make a move.

## Cloak and Dagger Chess
Pawns are played as usual, but all other pieces are replaced by numbered
checkers. Players have to deduce which of their opponent's pieces are which, and
then capture the king.

### Setup
Place all the pawns in their regular position, then use tape or stickers to
write the numbers 1 to 8 on checkers for each player. Put the black checkers on
black's back row and the light checkers on white's back row. Finally, write two
grids like this to secretly record your pieces and deduce your opponent's:

![Diagram](images/new_rules/diagram2.png)

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

![Diagram](images/new_rules/diagram3.png)

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

## Chess960
This is probably the least silly game in the collection; people organize
Chess960 tournaments! It's still a bit silly, because it takes away the standard
"opening book". One of the challenges to learning chess is that strong players
have spent a lot of time studying standard openings. That can also make the
early game feel like you're following a script. Randomizing the starting
position should make the standard openings much less important and make the play
feel more creative.

### Starting Position
The idea of randomizing the starting position has been around since the 1790s,
but Bobby Fischer added some restrictions in the 1990s to avoid positions that
strongly advantage one player:

* Pawns start in their regular position.
* The two bishops must be on different colours.
* The king must be between the two rooks.
* As in the standard starting position, black's pieces are a mirror reflection
  of white's.

With those restrictions, there are 960 possible starting positions. You can
generate a random number and look up the position in a table, or use a website
like [mark-weeks.com][weeks] to generate a position. You can also generate a
random starting position with a standard deck of playing cards. Create three
piles of cards with the following ranks, ignoring suit:

* A, 3, 5, 7
* 2, 4, 6, 8
* 8, 8, 10, 10, 10, Q

Shuffle each of the piles separately, then turn over one card from each of the
first two piles. Using the ace through 8 to represent the squares a1 through h1,
place the two white bishops on the squares that match the two cards. Confirm
that they are on opposite-coloured squares. Now turn over one card at a time
from the last pile, and use the identified white pieces to fill in the empty
squares from left to right. Place a knight for an 8, a queen for a queen, and a
rook or king for a 10. Place a rook for the first and third 10, and a king for
the middle 10. Finally, place the pawns in their regular positions and place the
black pieces to mirror the white pieces.

As an example, imagine you turned over an ace and a 6 from the first two piles,
then 8, 10, Q, 10, 8, 10 from the third pile. The starting position would look
like this:

![Diagram](images/new_rules/diagram4.png)

### Castling
The other change that Bobby Fischer made was to the castling rules. As usual,
the king may castle with the rook to his right or his left. However, the two
pieces' end positions after castling are the same as for standard chess. So to
castle with the h-side rook, white's king would end on g1 and the rook on f1, no
matter where they started. As in regular chess, there are several restrictions
before you can castle:

* The king and the rook must not have moved.
* The king's starting square, ending square, and all the squares he moves
  through must not be under attack.
* All the squares the two pieces move through must be empty, except for the two
  pieces themselves.

The rest of the standard chess rules apply unchanged.

[weeks]: https://www.mark-weeks.com/cfaa/chess960/c960strt.htm

[![cc-logo]][cc-by-sa]

[cc-logo]: images/cc-by-sa.png
[cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
