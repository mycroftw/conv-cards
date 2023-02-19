# conv-cards
ACBL Convention cards using GRB CCE

##  See [wiki](https://github.com/mycroftw/conv-cards/wiki) for more details.

This is a fairly complete rewrite of Gordon R. Bower's `grbcce` package for creating ACBL convention cards with LaTeX.

The ACBL completely rewrote the card for June 2022, and I completely rewrote the style file and template for the new card.
I kept most of the functionality (with permission):
- `\newcommand`s are used for text lines;
- `\setboolean` for checkboxes;
- how the checkboxes actually work;
- colours and text styles;
- and especially the command that makes the "what card do you lead from this holding" lines.

I have added a few little tweaks and cleanups, and I think this is much easier to use than the old card.

## Setup

1. Install the `acbl2022cc.sty` in your local texmf and rebuild your library.
2. Copy the template file into your cards library and rename.
3. **Very carefully** read the top comments.  It is very easy to break this - it's LaTeX, after all
4. You have three major decisions to make (but of course you can change it at any time with two characters!):
   - Do you want the lines under user-fillable text boxes to be printed?  I find having them there makes the card look very busy.
   - You can have entered text in the same font as the card itself, or in a serif font.  I find without the user text lines it can get a bit confusing, 
     so the default is "with guidelines on, use the same font, with them hidden, use serif."
   - The card is a bit crowded and the text (especially the serif text) is a bit small.  So you can force bigger text for your entries if you don't mind 
     a little less space.
5. With a copy of the card to hand, fill out the template - right side first, top to bottom, and then left side:
   - Enter text in the relevant `\newcommand`s (do not delete any!);
   - uncomment the `\setboolean`s for the checkboxes you want checked, and
   - fill in the "lead from" sections with the card you want 'circled' (actually boxed)
6. Make the pdf and look at it for things that need to be tweaked.

Note that you can make a copy of the initial card if you don't have access to one by simply copying the template and building that.
It's probably best to keep the guidelines on for a "blank card" whether you're going to just print it out or use it as an example.

## Legal information

Obviously, I'm not the ACBL.  Their card is their copyright.  I've just emulated it.

The intent of the licensing is to ensure that filled-in forms are owned by the pair that created them and can't legally be modified to claim "this is what they play", while still having the project available open source.  As such:

- The `acbl2022cc.sty` file and this file are released under CC-BY-SA license.  I would prefer, of course, that you send me a pull request for changes you make, or at least a copy of the file.
- The `latex_cc_example.tex` and `latex_cc_template.tex` files are released under CC-BY license.  This allows you to fill in the templates and have those filled-in cards not be released.  And the PDF files created from those templates can be completely closed, if you wish.
- Everything in mycards (if anything) is CC-BY-NC-ND.  They're my cards.  You get to look at them, that's the point, but yeah, no changes.
- Everything in the test folder is "use as you see fit, but do not distribute a changed file".  I can't enforce this obviously, but it's test code...
