---
title: The Rules of Chess Kit
---

### Introduction
I am not a strong chess player - it's always seemed to me more like study than
play. However, I do like the ideas in chess: a ragtag army of pieces with
different moves, battling to protect their king. I wondered if I could take
those ideas that many players are already familiar with, and mix them together
with some newer game mechanics from the last 500 years of board game design.
This collection contains chess games I've designed with hidden information,
bluffing, deduction, role selection, and yes, zombies. They can all be played
with a standard chess set and common items like pencil and paper, coins, and
playing cards.

Hopefully, serious chess players can enjoy these as a light break between
regular chess games, and new chess players can use them as a gentler
introduction to the classic game. Players of different chess abilities that
might find a game of regular chess frustrating may enjoy exploring these games
together.

## Table of Contents

## Zombie Chess
Just because you've captured a piece doesn't mean you can stop worrying about
it. In Zombie Chess, it can come back from the dead and shamble across the board
until you destroy it permanently.

### Setup
Set up the chess board normally, and gather a few coins. Four is usually enough.
Each player will also need paper and pencil to draw an 8x8 grid to record where
you secretly bury your opponent's pieces. Make it big enough to write a single
letter on each square. You can also draw a second grid, if you want to track
where your own pieces might be buried. The grids will be empty at the start of
the game.

Place the coins on one side of the board to mark the graveyard of zombie pieces.
The other side is the dust bin for destroyed pieces.

### Play
All the normal rules of Chess apply, until you capture a piece. In addition to
moving the captured piece to the graveyard of zombie pieces beside the board,
you have to secretly bury it under one of your pieces. Choose one of your
pieces, then find its matching square on your paper grid. Write the first letter
of the buried piece there, or N for kNight. Don't let your opponent see where
you buried the piece.

In this example game, Black has just captured a pawn at d4 and buried it under
the knight at c6.

    r . b q k b n r
    p p p p . p p p
    . . n . . . . .
    . . . . . . . .
    . . . p P . . .
    . . . . . N . .
    P P P . . P P P
    R N B Q K B . R
    arrow: e5, d4, black
    arrow: d4, c6, grey

At the end of your turn, check to see whether there was a piece buried under the
piece you moved. If not, say "no zombie" and say the coordinate you checked. If
there is a piece buried there, bring it back from the zombie graveyard to the
square on the board where it was buried. Place a coin under it to mark it as a
zombie, and erase it from your grid.

The next turn in the example game, White uses the knight at f3 to capture the
pawn at d4. First, they check for zombies. There are no black pieces in the
graveyard, so they say "no zombies anywhere". Then, they choose where to bury
the pawn. They decide to bury it under the pawn at b2, so they write a P in
their hidden grid at b2.

Black responds by capturing the knight at d4 with their knight at c6. First,
they check for zombies. There is a white pawn in the graveyard, so they check
their secret grid for the square they just left: c6. They see the P there, so
they put the white pawn back on the board with a coin under it and erase it from
the grid. Then they decide to bury the knight under the pawn at g7 and write
an N in that square in their hidden grid.

    r . b q k b n r
    p p p p . p p p
    . . P . . . . .
    . . . . . . . .
    . . . n P . . .
    . . . . . . . .
    P P P . . P P P
    R N B Q K B . R
    arrow: c6, d4, black
    arrow: c6, c6, grey
    arrow: d4, g7, grey

Also at the end of your turn, check if you have any zombie pieces that you
didn't move. If so, they are permanently destroyed, and moved to the dust bin
side of the board.

If you have more than one zombie piece on the board, they form a zombie horde.
You can move all of them on one turn, although each piece can only move once per
turn. Any that you don't move will be destroyed at the end of your turn.

You probably don't want to bury pawns on your back rank, because they can
immediately be promoted when they come back and then moved on that turn. As with
regular chess, you can promote to extra queens. Either use a queen from another
set, or just keep track of which pawns have been promoted.

You can't bury more than one of your opponent's zombie pieces under one of your
pieces. However, you can leave that piece buried if your opponent captures your
piece on top of it. When they move off the space, first ask them if they
revealed one of your buried pieces. If so, it comes back, and you don't yet have
to reveal the piece you have buried there.

In the very unlikely event that you capture a piece and already have a piece
buried under each of your pieces, move it directly to the dust bin and say, "I
cannot bury this piece."

### Game End
As usual, the goal is to checkmate your opponent's king. If moving a piece would
put your king in check by revealing a zombie, you may not move that piece. When
castling, complete the move before revealing any zombies.

## Masquerade Chess
Masquerade Chess is regular chess, but all the pieces above pawns have a secret
identity. They use their standard moves, except when capturing. Each player
knows the capture moves of their opponent's pieces, but not their own. Who can
deduce their way to victory first?

### Setup
Players each draw two copies of this table:

    type: masquerade
    . K Q R B N combo
    K . . . . . _
    Q . . . . . _
    R . . . . . _
    B . . . . . _
    N . . . . . _

They write their opponent's name above one table and their own name above the
other. They then fill in the table for their opponent's pieces without letting
their opponent see. Circle one square in each row and column to record which of
their opponent's pieces captures using which moves. Each row must have one
circle and each column must have one circle. A piece may be given its normal
capture or the capture from a different piece.

Players will fill in the other copy as they learn about their own pieces.

The combo column can be helpful to fill in with the move and capture letters
together, so players don't have to keep looking at the rows and columns of the
rest of the table.

Here's an example set up where Bob has filled in the table for Alice's pieces
and left his own blank.

#### Alice
    type: masquerade
    . K Q R B N combo
    K . . O . . KR
    Q O . . . . QK
    R . . . . O RN
    B . . . O . BB
    N . O . . . NQ

#### Bob
    type: masquerade
    . K Q R B N combo
    K . . . . . _
    Q . . . . . _
    R . . . . . _
    B . . . . . _
    N . . . . . _

### Play
On each turn, the player may either make a standard move without capturing, or
attempt a capture. To attempt a capture, point to the piece you want to move,
then to the piece you want to capture, and ask your opponent, "Capture?" If your
opponent says the move is legal, perform the capture as normal. If not, you
don't move anything, and your turn is over. Either way, record what you learned
in your table by writing X's for combinations that you know are impossible and
O's for combinations that you know are correct. Remember that pawns always
capture with their standard capture moves.

### Game End
The game ends when one of the players captures the other's king. Because players
don't always know their pieces' abilities, they don't have to call "Check", and
a threatened king doesn't have to evade capture. The king may choose to bluff by
staying where it is or even move into an attacked square. A king may castle out
of check. There is no stalemate between kings: one king can capture another to
win the game.

### Strategy
A key part of strategy is which capture moves to assign to which pieces. It
seems like it would be a big advantage to give your opponent two queens, so
perhaps the queen capture should always be assigned to the king or the queen. It
seems like giving it to the king makes it harder to use, because a long range
capture will likely leave the king exposed. However, a king with a queen capture
can defend itself very effectively.

The Queen can quickly get into position to attack, so it's probably wise to give
it a less powerful attack like the knight or king. However, even these can be
surprisingly effective.

When assigning capture moves to the bishop, knight, and rook, look at which
pawns they can defend. If you can make one of the pawns undefended and then try
to attack it with a knight, that can be a quick, safe way to learn about some of
your pieces.

As an example, KQ, QN, RB, NR, BK seems nicely balanced, and leaves the rook
pawns undefended. However, assigning the same moves every game would be too
predictable.

Another part of strategy is the effective use of bluffing. Keep track of what
your opponent knows about their own capture moves, and put your pieces in danger
if the risk is worth learning something valuable or attacking the king. Try to
learn faster than your opponent and strike before they know enough to defend
themselves. Move fast and break things!

### History
This game was inspired by Robert Abbott's Confusion, which Kerry Handscomb and
I originally adapted as Minor Confusion by creating a more balanced set of moves
and playing with a chess set. That was playable but uninspiring, so I abandoned
it for 15 years. Masquerade Chess returns to the standard Chess moves, and
players only learn about their pieces during capture, which slows the pace of
the game.

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

    r n b q k b n r
    p p p p p p p p
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    P P P P P P P P
    R N B Q K B N R
    margins: 0, 1, 6, 1
    card: back, 11, -1
    card: back, 11.5, -0.75
    card: back, 12, -0.5
    card: back, 9, 2.5
    card: back, 11, 6
    card: back, 11.5, 5.75
    card: back, 12, 5.5

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

    b n r q k b n r
    p p p p p p p p
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    . . . . . . . .
    P P P P P P P P
    B N R Q K B N R
    card: AS, 8.5, 0
    card: 6S, 11, 0
    card: 8H, 8.5, 5
    card: 10H, 9, 5
    card: QH, 9.5, 5
    card: 10C, 10, 5
    card: 8D, 10.5, 5
    card: 10D, 11, 5
    margins: 0, 0, 5, 0

### Castling
The other change that Bobby Fischer made was to the castling rules. As usual,
the king may castle with the rook to his right or his left. However, the two
pieces' end positions after castling are the same as for standard chess. So to
castle with the a-side rook, white's king would end on c1 and the rook on d1, no
matter where they started. In the example above, white's third move could be to
castle.

    b n r q k b n r
    p p p p . . p p
    . . . . . p . .
    . . . . p . . .
    . . . . P . . .
    . . . . . . . .
    P P P P Q P P P
    B N K R . B N R
    margins: 0, 0, 0, 1
    arrow: e0, c0, grey
    arrow: c1, d1, grey

As in regular chess, there are several restrictions
before you can castle:

* The king and the rook must not have moved.
* The king's starting square, ending square, and all the squares he moves
  through must not be under attack.
* All the squares the two pieces move through must be empty, except for the two
  pieces themselves.

The rest of the standard chess rules apply unchanged.

[weeks]: https://www.mark-weeks.com/cfaa/chess960/c960strt.htm

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

### Contributing
Know some other lighthearted chess variants? Ideas to share? Get in touch at
[https://donkirkby.github.io/chess-kit][github].

Zombie Chess, Masquerade Chess, Crowded House, and Cooperative Chess are
original games designed by [Don Kirkby][don].

[github]: https://donkirkby.github.io/chess-kit
[don]: https://donkirkby.github.io/
