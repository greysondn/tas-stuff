Python projects and code related to TAS stuff.

List of Console ids
===================

| id     | console(s)                                             |
| ------ | ------------------------------------------------------ |
| `snes` | Super Nintendo Entertainment System / Super Famicom    |

Conventions
===========

That is to say, conventions used specific to this code and its organization.

Execution
---------

Via `python -m path.to.module` in the same folder as this readme file. Failure to do so may result in broken imports.

Namespaces
----------
The hiearchial tree is a bit deeper than suggested for Python classes
(See [PEP-0423](https://www.python.org/dev/peps/pep-0423/#avoid-deep-nesting)).
This was chosen for clarity's sake, and has a strictly defined limit.

Specifically, tracing the tree should give you:

* `tasstuff` - acting, here, as
  [the ownership namespace](https://www.python.org/dev/peps/pep-0423/#top-level-namespace-relates-to-code-ownership).

  * `consoleid` - the id of the console the code is for. With the exception of
    `any` (used for general and helper classes) and `test` (used for unit tests).

    * `gamename` - the game's name, or an id chosen euphemistically for the
      game. (A mapping of such euphemisms should exist inside the `consoleid` 
      folder.)

      * `project` - if a folder exists here, it represents a specific project's
        code. There may not be any subfolders beyond this level, and this should
        be used sparingly for projects that exceed one or two files - not as
        the main rule.

In general, Python files and a readme describing any that are directly runnable
should exist under `gamename`. Generally, we should only be one level deeper
than the convention for hiearchial trees, and well organized.

`consoleid` and `gamename` are subjected to the following conditions:

* all capitalization is removed (replace by lowercase)

* spaces are replaced by underscores

* all non-alphanumerics characters are removed

* if the game starts with a number, then `no_` is appended to the front.

The cause of these rules have to do with the fact that python packages must be
valid identifiers. Python defines the identifier syntax as:

```ebnf
identifier ::=  (letter|"_") (letter | digit | "_")*
```

However, in practice, starting with an underscore seems largely unwise; that
typically denotes a private package - one not meant to be used or to be
considered not part of the public facing API.

Code Style
----------
Not a clue how to define it. Really need to encode it into a styler sometime.

* Python 3.