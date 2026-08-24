# conv-cards
ACBL Convention cards using GRB CCE

##  See [wiki](https://github.com/mycroftw/conv-cards/wiki) for more details.

This is a fairly complete rewrite of Gordon R. Bower's `grbcce` package for
creating ACBL convention cards with LaTeX.

The ACBL completely rewrote the card for June 2022,
and I completely rewrote the style file and template for the new card.
I kept most of the functionality (with permission):
- `\newcommand`s are used for text lines;
- `\setboolean` for checkboxes;
- how the checkboxes actually work;
- colours and text styles;
- and especially the command that makes the 
  "what card do you lead from this holding" lines.

I have added a few little tweaks and cleanups,
and I think this is much easier to use than the old card.

## Setup

1. Install the `acbl2022cc.sty` in your local texmf and rebuild your library.
2. Copy the template file into your cards library and rename.
3. **Very carefully** read the top comments. 
   It is very easy to break this - it's LaTeX, after all
4. You have three major decisions to make 
   (but of course you can change it at any time with two characters!):
   - Do you want the lines under user-fillable text boxes to be printed?
     I find having them there makes the card look very busy.
   - You can have entered text in the same font as the card itself, or in a serif font.
     I find without the user text lines it can get a bit confusing, so the default is
     "with guidelines on, use the same font, with them hidden, use serif."
   - The card is a bit crowded and the text (especially the serif text) is a bit small.
     So you can force bigger text for your entries if you don't mind a little less space.
5. With a copy of the card to hand, fill out the template - 
   right side first, top to bottom, and then left side:
   - Enter text in the relevant `\newcommand`s (do not delete any!);
   - uncomment the `\setboolean`s for the checkboxes you want checked, and
   - fill in the "lead from" sections with the card you want 'circled' (actually boxed)
6. Make the PDF and look at it for things that need to be tweaked.

Note that you can make a copy of the initial card if you don't have access to one
by simply copying the template and building that.
It's probably best to keep the guidelines on for a "blank card"
whether you're going to just print it out or use it as an example.

If you want to see some examples of how this works, all my cards (LaTeX and PDF) are in 
[my companion project](https://github.com/mycroftw/my_cards). 

## Upgrading your cards

As fixes happen and we get closer to an actual "real release",
the `.sty` file and the templates may have to change.
Sometimes this will not be an issue, everything will just work with the old version;
but sometimes changes happen that *require* changes to your current cards 
for them to rebuild (if you decide to go from NMF to XYZ after 10 years, for instance).
I am providing upgrade scripts for any changes.

I just assume that all people that can handle LaTeX can handle Python at least at a 
user level;
on linux it should already be installed, on Windows, installing is trivial.

Upgrade scripts are run sequentially - there is no "rollup" upgrade.
As far as I know, there isn't an upgrade that will break if a 
previous one hasn't been done, but Just To Be Safe...

All the upgrade scripts have the same run pattern:
- `python upgrade_[old]-[new].py --help` to get usage and "what it does" information;
- `python upgrade_[old]-[new].py [file] ([file] [file]...)` to upgrade one or multiple cards;
- `python upgrade_[old]-[new].py [directory]` to upgrade every card in the directory.

Note that the upgrader is *paranoid* and *fail-early*: 
1. if it thinks the card has already been upgraded, it will bail out;
2. if it is asked to do N operations and less than N report successful, 
   it will make no changes to the card whatsoever;
3. if it fails on one card, it *stops* and does not try the rest of the list/directory.
    - Note that because some cards may have been upgraded before the failure occurred, 
      re-running the complete list or directory will fail (see 1.)
4. it will create a `backup` directory and put the previous version of the card in there,
   even if it thinks it's succeeded.
    - Note: You can copy the backed up originals of any succeeded cards back in, 
      effectively "downgrading" them, to avoid the re-run issue in 3.


## Legal information

Obviously, I'm not the ACBL.  Their card is their copyright.  I've just emulated it.

The intent of the licensing is to ensure that filled-in forms are owned by the pair
that created them and can't legally be modified to claim "this is what they play",
while still having the project available open source.  As such:

- The `acbl2022cc.sty` file and this file are released under the CC-BY-SA licence.
  I would prefer, of course, that you send me a pull request for changes you make,
  or at least a copy of the file.
- The `latex_cc_example.tex` and `latex_cc_template.tex` files are released under the
  CC-BY licence.
  This allows you to fill in the templates and have those filled-in cards not be legally 
  changeable or shareable by others (including me!)
  The PDF files created from those templates can be completely closed, if you wish.
- Everything in the upgrade folder is released under GPL3.
- Everything in the test folder is "use as you see fit,
  but do not distribute a changed file".
  I can't enforce this obviously, but it's test code...
