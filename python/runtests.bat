@echo off
REM This assumes that nose is inside the Python 37 location.
REM Linux try $(where nosetests)
REM Windows, good luck, maybe start with $: where nosetests

REM destroy coverage data so it's built ground up
del .coverage

coverage                                                                       ^
    run                                                                        ^
--omit="./tasstuff/test/*","*/__init__.py"                                     ^
        "C:\Program Files\Python37\lib\site-packages\nose\core.py"             ^
            --all-modules                                                      ^
            .                                                                  ^
            

REM issue coverage report at command line
echo.
coverage report

REM destroy coverage html so it's built ground up
rmdir /Q /S coverage

coverage                                                                       ^
    html                                                                       ^
        --directory=coverage                                                   ^