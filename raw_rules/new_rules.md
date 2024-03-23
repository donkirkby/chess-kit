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
