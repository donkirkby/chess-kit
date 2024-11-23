---
title: Journal
subtitle: How we got here
hero_image: ../images/index_hero.jpg
---
## 2007 - Minor Confusion
Originally, I played Robert Abbott's Confusion several times with Kerry
Handscomb, where you don't know which of your pieces can make which moves. We
loved the idea of having to deduce your own pieces' moves, but we were
frustrated that a lot of the game came down to luck: who happened to find their
most powerful pieces first.

We designed a version with fewer pieces that had more balanced power, and called
it Minor Confusion. We even discussed the idea with Robert Abbott himself, and
got his permission to include it in a book project that was never completed.
Minor Confusion was OK, but a bit dry. We eventually moved on to playing other
games.

### Nov 2022 - Masquerade Chess
15 years after Minor Confusion, I had the idea to give pieces different moves
when capturing. Standard chess pieces would move normally, except when they
capture, and you have to deduce their capture moves. You have to engage with
your opponent to learn anything, and that spreads the deduction over a longer
game.

### May 2023 - Zombie Chess
After several successful playtests, I started thinking about whether I could
make a version of Masquerade Chess to sell. It seemed silly to try and sell the
chess set, so I thought about making the accessories to add to a standard chess
set: a dry-erase screen to secretly record which pieces have which capture
moves.

It seemed like it would be easier to sell, if you could play more than one game
with it, so I tried to think of other chess variants with hidden information
that could use a dry-erase screen. I had the idea to secretly bury the captured
pieces on the board, and Zombie Chess was born.

### Jun 2023 - Chess Kit
After two successful ideas, I decided to turn them into another book project,
similar to [Donimoes], my collection of new domino games and puzzles. I came up
with eight ideas over a couple of weeks.

[Donimoes]: https://donkirkby.github.io/donimoes/

### Oct 2023 - Cooperative Chess
I had a successful playtest of Crowded House, and wrote up its rules, along with
Chess960. I spent the most time, though, testing Cooperative Chess as a
solitaire.

I also converted the scripts for publishing the Donimoes rules as PDF and
website to this project.

### Nov 2023 - Adrenaline Chess
Started with Manna Chess, where manna drops randomly after each capture, and
gives the piece carrying it one extra king move. Players found the random drops
annoying, so we switched to Adrenaline Chess, where you choose which opposing
piece to give an adrenaline boost to after each capture. Made for some
interesting tactics of giving the boost to a piece you could capture it back
from.

### Dec 2023 - Chess Golf
Started with Neighbour Chess Solitaire, where the pieces borrow their
neighbour's move, and then merged it with Ricochet Robots to make Chess Golf.
Struggled with the mechanics of automatically adding pieces back to the board
and what to do when a colour has no neighbouring pairs. Fixed it by adding
special moves that can be done any time, but are expensive, then decided to
add pieces back between rounds, and make a king's move when there are no
neighbouring pairs of a colour.

Breadth-first search could only handle the easy problems, so investigated Monte
Carlo tree search.

### Feb 2024 - Chess Cards
Playtesters consistently complained about having to map regular playing cards
to chess pieces, so I designed a deck of chess cards. The fronts were easy, I
just used the chess symbols from the `python-chess` library, and added pips for
the gaps used in Chess Golf and Parade Chess Solitaire.

[![card-front]][card-front]

The backs, though, went through several ideas. My main idea was to have a
checkerboard pattern with some kind of distortion. I thought that twisting the
pattern more and more as it approached the edge would make the card edge
tolerant to drift when the cards are printed and cut out, and I also made the
black and white both fade to grey. I didn't really like the plain corners, and
I noticed that most card back patterns have a solid border with a plain white
bleed, so I switched to that, and moved the twist to the middle of the pattern.

[![back-fade]][back-fade]
[![back-trimmed]][back-trimmed]

The twist itself used some interesting math. I chose a sigmoid curve that I
came across while studying machine learning. Here's how the checkerboard pattern
is rotated as you move away from the centre of the image. That gives you a
stable region in the centre, a rotation phase, and then another stable region
at the edges. To me, it looks like someone grabbed the centre and twisted it.

[![twist-plot]][twist-plot]

[card-front]: images/card-K.png
[back-fade]: images/back-fade.png
[back-trimmed]: images/back-trimmed.png
[twist-plot]: images/twist-plot.png

### Mar 2024 - Booster Chess
This was an attempt to add the chaos of cards to Adrenaline Chess, but players
would often get good enough cards that they could stomp their opponent in under
ten moves. It also ended up feeling too similar to Adrenaline Chess. I solved
both problems by dropping the boost and keeping only the hobble to make Tar Pit
Chess.

### Apr 2024 - Tar Pit Chess
After extracting it from Booster Chess, I simplified it to only allow one
checker at a time under a piece. I also softened the checkers cards to adjust
hand size.

### Jun 2024 - Two Move Chess
I adapted the same movement mechanic that I previously used in [Blind Hex]. I
think it's a much better fit for Chess than for Hex.

[Blind Hex]: https://donkirkby.github.io/blind-hex/

### Sep 2024 - Synchronous Chess
This was the best simultaneous movement variant that I found, and I didn't
change the rules at all. Hopefully, my rewrite is easier to understand, but the
rules themselves haven't changed. It might appear similar to Two Move Chess,
but that game is simultaneous choice, followed by moves in a defined order. I
think Two Move Chess is less chaotic and more tactical, as you puzzle out which
cards to play.

### Nov 2024 - Player Aid Cards
I think the game rules are stable, so I'm getting playtesters to read the rules
cold and try to play from them. A player aid card for each game makes it easier
to remember the key points while playing.
