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
    opponents pieces. (2 players, chess set, and checkers set)
* [Chess 960][chess-960] is a game designed by Bobby Fischer to mix up
    the game opening by randomly choosing your starting position. (Chess
    set and deck of cards)

[crowded-house]: #crowded-house
[cloak-and-dagger-chess]: #cloak-and-dagger-chess
[chess-960]: #chess-960

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
yourself three queens!) You also have to place your king somewhere between your
two rooks. Write a circle for each piece you know, and an X for each piece you
know is impossible. You might want to write X's for your own pieces as your
opponent learns which of your combinations are impossible.

At the start of your turn, you may guess the identity of one of your opponent's
checkers. If you guess correctly, you make two moves in the current turn.
If you guess incorrectly, your turn is over.

If one of your checkers is captured, tell your opponent which piece they
captured.

At the end of your turn, you may replace any number of your checkers with their
uncloaked chess pieces.

### Winning
Win by capturing a cloaked king or putting an uncloaked king in check mate.

A cloaked king may move into check, stay in check, or castle out of check,
because the opponent doesn't know it's in check. Castling is the same as in
Chess 960: the king and rook end up on the same squares they do in standard
chess. All spaces between their start position and their end position must be
empty, except for the king and the castling rook. All spaces between the king's
start and end positions must not be under attack, if the king is uncloaked.

## Chess 960
A variant invented by Bobby Fischer to [generate][generate] random starting
positions. You can also generate random starting positions with a
[deck of cards][deck of cards]. Castling rules use standard ending locations.

[generate]: https://www.mark-weeks.com/cfaa/chess960/c960strt.htm
[deck of cards]: https://en.wikipedia.org/wiki/Fischer_random_chess#Creating_starting_positions

[![cc-logo]][cc-by-sa]

[cc-logo]: images/cc-by-sa.png
[cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
