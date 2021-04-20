Spanish For Everyone - Word Search Solver
-----------------------------------------

It is customary on TasVideos.org's website to do joke submissions or submissions
of games that would normally not pass the site's standards on April Fool's Day.
In 2019, I somehow got involved with TheEnglishMan's playthrough of Spanish for
Everyone, a Nintendo DS game infamous for its undertones and rushed development.

You can find his submission here:

http://tasvideos.org/6344S.html

His commentary on my involvement reads:

> Before I start my submission notes, extra special thanks to **greysondn**, who
> wrote a brute-force script for solving the minigames and saved me hours, if
> not days, of agony. This TAS could not have been submitted in time for April
> Fool's Day if not for him!

(Small disclosure: TheEnglishMan was not aware of my gender identity or
pronouns, and was not trying to offend anyone. Do not harass them on my behalf.)

The game features minigames which are word searches with a known dictionary. If
memory serves, TheEnglishMan was able to retrieve the table from memory, but had
no concrete assurance of which words were in it outside a word list the game
would pull from. That was where I came in.

Given the dictionary and the knowledge that a fixed size existed for the search
grid, it becomes possible to just brute force search for all words in the grid.
In python, this would likely take quite some time (being a brute force task); in
C++, this takes virtually no time. But more to the point, TheEnglishMan, if
memory serves, was not a programmer, and had not worked with the Python (or any)
interpreter. C++ gave me the ability to quickly and fairly reliably create a
binary that they could just take and run. Minimizing friction, +1 programmer
twinkie get.

I am not sure what files exactly are necessary for this to run, so I've included
in this folder:

* an example board, which I have no clue whatsoever what it says or has, because
  I don't really speak Spanish well at all.

* the word list that was provided when this project was done, which, again, I
  have to hope isn't offensive because I don't speak Spanish well at all.

* two batch files I shipped with the binary, evidently. No clue why.

* the source CPP file. And I have no clue how it was compiled, because that's
  what people love to hear, I'm sure.

I don't know why anyone in their right mind would want this, but good luck, all
the same, if you have some use for it.