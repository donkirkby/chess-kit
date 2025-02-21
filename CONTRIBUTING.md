## Contributing
If you like Chess Kit and want to make it better, help out. It could be as
simple as sending [@donkirkby@hachyderm.io] a nice note on Mastodon, you could
report a problem, or pitch in with some playtesting or design work.

### Problems
Found a typo or a problem with the rules? Create a [GitHub issue], and be as
specific as possible.

### New Games
Do you have an idea for another game to include in Chess Kit or a favourite
Chess variant? Create an issue, and describe how it would work.

### Testing GitHub Pages locally
The web site uses the [Bulma Clean theme], which is based on [Bulma]. The
[Bulma colours] can be particularly helpful to learn about.

GitHub generates all the web pages from markdown files, but it can be useful to
test out that process before you commit changes. See the detailed instructions
for setting up [Jekyll], but the main command is this:

    cd docs
    bundle exec jekyll serve

### Writing Rules
The rules are generated based on the markdown in `raw_rules/rules.md`. The text
stays basically unchanged, and you can use bold, italic, bulleted lists, and
numbered lists.

You can also draw the diagrams with code blocks. Diagrams support these
features:

* Chess boards are converted from a text format like this:

      r n b q k b n r
      p b p p p p p p
      . . . . . . . .
      . . . . . . . .
      . . . . . . . .
      . . . . . . . .
      P P P P P P P P
      R N B Q K B N R

* You can add several features after the chess board using a label and
  parameters. An arrow takes the start space, end space, and colour. Draw a
  circle by adding an arrow with the same start and end:

      arrow: h7, h5, black

* Add a playing card with the piece symbol, column, and row of its top left
  corner:

      card: Q, 9, 4
      card: back, 10, 4

* Add a checkers count display with the white count and black count:

      checkers: 4, 5

  Remember that you can put a checker on the board with an arrow that starts and
  ends in the same square, so it's drawn as a circle:

      arrow: h5, h5, black

* Set the margins. Two numbers set the left/right and the top/bottom margins.
  Four numbers set the left, top, right, and bottom margins.

      margins: 3, 1, 0, 0

* Add some text with the text, the column, and the row to write it in.

      text: X, 7, 4

* Corner text is smaller and written in the upper left corner of a square.

      corner text: X, 7, 4
 
* There are also some diagrams without a chess board, that can be chosen with
  a type label at the start. For example, the masquerade grid:

      type: masquerade
      . K Q R B N combo
      K . . . . . _
      Q . . . . . _
      R . . . . . _
      B . . . . . _
      N . . . . . _

* The card grid in Appendix A:

      type: cards
      Piece Cards Gap
      p 2S 3S 4S 5S 2C 3C 4C 5C _
      n  _  _  _ 8S 8C  _  _  _ 1
      b  _  _  _ 9S 9C  _  _  _ 2
      r  _  _ _ 10S 10C _  _  _ 3
      q  _  _  _ QS  _  _  _  _ 5
      k  _  _  _ KS  _  _  _  _ 6
      c  _  _ 6S 7S 6C 7C  _  _ _

[@donkirkby@hachyderm.io]: https://hachyderm.io/@donkirkby
[GitHub issue]: https://github.com/donkirkby/chess-kit/issues
[Bulma Clean theme]: https://github.com/chrisrhymes/bulma-clean-theme
[Bulma]: https://bulma.io/documentation/
[Bulma colours]: https://bulma.io/documentation/overview/colors/
[Jekyll]: https://help.github.com/en/github/working-with-github-pages/testing-your-github-pages-site-locally-with-jekyll
