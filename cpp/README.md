C++ projects and code related to TAS stuff.

List of Console ids
===================

| id     | console(s)                                             |
| ------ | ------------------------------------------------------ |
| `nds`  | Nintendo DS                                            |
| `snes` | Super Nintendo Entertainment System / Super Famicom    |

Conventions
===========

That is to say, conventions used specific to this code and its organization.

Execution
---------

No clue.

Namespaces
----------
In general, this code is banged out so it's one off and poorly namespaced. My weapon of choice for most projects is python, so typically C++ only is used when someone needs a binary they can understand or something is bogging down in Python in a way that doesn't seem to be due to naive coding practices.

In other words, this is a mess.

Folder Structure
----------------

Similar to Python, to the extent that I'm going to just pull it from there.

Specifically, tracing the tree should give you:

* `consoleid` - the id of the console the code is for. With the exception of
  `any` (used for general and helper classes) and `test` (used for unit tests).

  * `gamename` - the game's name, or an id chosen euphemistically for the
    game. (A mapping of such euphemisms should exist inside the `consoleid` 
      folder.)

  * `project` - if a folder exists here, it represents a specific project's
        code. There may not be any subfolders beyond this level, and this should
        be used sparingly for projects that exceed one or two files - not as
        the main rule.

Code Style
----------
Not a clue how to define it. Really need to encode it into a styler sometime.

* Python 3.