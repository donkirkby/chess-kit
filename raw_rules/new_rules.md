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

## Crowded House
Two teams of two play, with each player moving the pieces of their colour
on the left or right half of the board. As usual, white moves first, then
alternates with black. Each king-side player takes the first move for their
team, then alternates with their partner.

In the following example, Walter plays king-side white, Winnie plays queen-side
white, Betty plays king-side black, and Bob plays queen-side black. Then the
play order would be Walter, Betty, Winnie, Bob, Walter, Betty, and so on.

    r n b q k b n r
    p p p p p p p p
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    P P P P P P P P
    R N B Q K B N R
    margins: 3, 0
    text: 1: Walter, 10.5, 1
    text: 2: Betty, 10.5, 8
    text: 3: Winnie, -1.5, 1
    text: 4: Bob, -1.5, 8

### Rule changes
The key rule is that you may only move a piece that either

* **starts** on your side of the board, or
* **ends** on your side of the board.

In this example, Winnie may move any piece that starts or ends on the queen
side of the board, shown by the dashed rectangle. She may move the bishop as
shown by the arrow, because it ends up on the queen side of the board. Winnie
may not move the bishop to e2, because it would start and end on the king side.

    r n b q k b n r
    p p p p . p p p
    . . . . . . . .
    . . . . p . . .
    . . . . P . . .
    . . . . . . . .
    P P P P . P P P
    R N B Q K B N R
    arrow: f1, c4, white
    margins: 3, 0
    text: 1: Walter, 10.5, 1
    text: 2: Betty, 10.5, 8
    text: 3: Winnie, -1.5, 1
    text: 4: Bob, -1.5, 8
    rect: 1, 1, 4, 8

If a player has no pieces on their side and can't move any pieces to their side,
they move nothing on that turn.

The rest of the rule changes flow from whether a piece may be captured
immediately. A king may move into check or castle out of check, if the next
player can't make the capture. En passant capture only works if the pawn is
captured immediately after its first move.

### Winning
Win by check mate, as usual, but remember that the next player on the attacking
team has to be able to make the capture.

### Talking
This game shouldn't be taken too seriously, so feel free to chat with your
partner, but remember that the other team is listening. Any discussion should
be heard by both teams, so no secret codes or second languages! Of course,
players should also feel free to ignore their partner's advice.

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
