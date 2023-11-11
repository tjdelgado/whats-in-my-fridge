# python/package/library versions at a glance
| Library   | Version | Notes                        |
|-----------|---------|------------------------------|
| python    | 3.9.17  |                              |
| SQLite    | 3.40+   | Any recent version should do |
| Flask     | 3.0.0   |                              |
| pytest    | 7.4.3   |                              |
| bootstrap | 5.3.2   |                              |

# Quick reference links:
Flask documentation: https://flask.palletsprojects.com/en/3.0.x/

Flask Tutorial: https://flask.palletsprojects.com/en/3.0.x/tutorial/

SQLite documentation: https://www.sqlite.org/docs.html

sqlite3 python library documentation: https://docs.python.org/3/library/sqlite3.html

pytest documentation: https://docs.pytest.org/en/7.4.x/getting-started.html#get-started

Unit testing Flask apps using pytest: https://flask.palletsprojects.com/en/3.0.x/tutorial/tests/

And more on testing Flask apps using pytest: https://flask.palletsprojects.com/en/3.0.x/testing/

# How to run the flask app locally
1. Ensure that you are in the project directory, and that the venv has been activated, as by, e.g., on Linux,
    $ . .venv/bin/activate
2. Run:
    `flask --app wimf run --debug`

Flask will monitor the project directory (mostly .py files I think) for changes and will reload the flask app
when it detects such changes.

3. If you need to re-init the db, try
    `flask --app wimf init-db`

# Database schema notes

`items` table:

table corresponding to current contents of fridge

| colname       | constraints          | notes                                   |
|---------------|----------------------|-----------------------------------------|
| "id"          | INTEGER PRIMARY KEY  | synthetic PK                            |
| "name"        | TEXT NOT NULL        | item name                               |
| "expiry_time" | INTEGER NOT NULL     | # days for item to go bad, -1 for indef |
| "date_added"  | TEXT NOT NULL        | stored as YYYY-MM-DD                    |
| "expiry_date" | NUMERIC DEFAULT NULL | also YYYY-MM-DD                         |
|               |                      |                                         |

TODO: add details on trigger to compute expiry date

`stored_items` table:

table for items user has chosen to store for future reference

| colname       | constraints         | notes                             |
|---------------|---------------------|-----------------------------------|
| "id"          | INTEGER PRIMARY KEY | synthetic PK                      |
| "name"        | TEXT NOT NULL       | item name                         |
| "expiry_time" | NUMERIC NOT NULL    | how long takes for item to go bad |


`recipes` table:

mostly keeps track of recipe names

| colname | constraints         | notes        |
|---------|---------------------|--------------|
| "id"    | INTEGER PRIMARY KEY | synthetic PK |
| "name"  | TEXT NOT NULL       | item name    |

`recipes_ingredients` table:

keeps track of what recipes take which ingredients and v.v.

The tuple (r,i) is in this table iff food item i is an ingredient of
recipe r.

| colname     | constraints                  | notes               |
|-------------|------------------------------|---------------------|
| "id"        | INTEGER PRIMARY KEY          | synthetic pk        |
| "recipe_id" | INTEGER FOREIGN KEY NOT NULL | ref: `recipes`      |
| "ingr_id"   | INTEGER FOREIGN KEY NOT NULL | ref: `stored_items` |
| "ingr_qty"  | NUMERIC NOT NULL             |                     |


# Setting up your dev environment

## Step 0: Create a directory for your project
Pick a directory you want to use for your code files. I'll call it
${PROJECTPATH} for this doc. (For example, on Linux, my project lives
in /home/tdelgado/projects/wimf/)


## Step 1: Setting up your python dev environment

It's important to set up a separate /python environment/ to keep the
specific version of python and supporting (python) libraries we're
using separate from whatever version of python your
OS/distribution/other apps have installed.

Otherwise very strange and very difficult to debug behavior may occur,
up to and including breaking other programs on your OS that expect
different versions of the interpreter or python libraries.

### Prerequisites

You'll probably want `git` installed before you proceed. If you don't
know how to install it, or if you have it installed, check out
instructions here: https://github.com/git-guides/install-git

Linux users probably want `curl` installed as well --- installing via
your package manager, as by `apt install curl` on Debian-derived
distros (e.g. Ubunut, Linux Mint) should suffice.


### Setting up pyenv

[pyenv](https://github.com/pyenv/pyenv) simplifies the process of
installing and isolating multiple versions of python on your system
for development purposes.

Unless you have a compelling reason to do otherwise, you probably want
to install pyenv in the default location used by the installer; on
UNIX-like systems, this is usually `~/.pyenv`.

#### Linux:

Run: `curl https://pyenv.run | bash` at your terminal (assuming your
shell is bash, which it probably is unless you changed it).

**Make sure you follow the post-installation instructions that the
installer gives you, and make sure to restart your shell after
installation!**


#### Windows:

If you're working within WSL, follow the linux instructions within
your WSL environment. If you'd rather not work under WSL, then you'll
want to use
[`pyenv-win`](https://github.com/pyenv-win/pyenv-win#quick-start)
instead.


#### OSX:

Follow instructions at: (https://github.com/pyenv/pyenv#homebrew-in-macos).

#### Post-installation [OSX and Linux]:

First, make sure you have configured your shell using the instructions
that the installer emits after installation, or as can be found
[here](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv).

Second, follow these instructions to make sure you have the necessary
utilities and libraries necessary to compile/install different
versions of python:
(https://github.com/pyenv/pyenv/wiki#suggested-build-environment)

Now, make sure that the following commands produce sane output
(output from my setup provided below the commands; should vary
slightly depending on your platform/machine).

    $ which pyenv
    /home/tdelgado/.pyenv/bin/pyenv

    $ echo $PATH | grep --color=auto "$(pyenv root)/shims"
    < a directory like /home/tdelgado/.pyenv/shims should be present
    and highligted in red in the output >

See this
[link](https://github.com/pyenv/pyenv/wiki#how-to-verify-that-i-have-set-up-pyenv-correctly)
for details.

### Installing python 3.9.17 with pyenv

At the command line, run:

     $ pyenv install 3.9.17
### Setting default python version in the project directory

At the command line, first change directory to the directory you made
for the project. For me, this is:

    $ cd /home/tdelgado/projects/wimf

Then, **in this directory**, execute:

    $ pyenv local 3.9.17

We have now setup pyenv to route all calls to the `python` executable
in the project directory to the python 3.9.17 distribution that pyenv
installed. Run this command to make sure the changes held:

    $ pyenv versions

You should get output like:

    system (set by /home/tdelgado/.pyenv/version)
    * 3.9.17

### TODO: setup your IDE to work with the python environment

This depends on your IDE. For now, try googling "pyenv <name of your
IDE>" to see how to tell your IDE to talk to the version of python we
installed with `pyenv`.

## Step 2: Install Flask and pytest

### Setup the venv (Linux/OSX)

Modified from (https://flask.palletsprojects.com/en/3.0.x/installation/)

    $ cd ${PROJECTDIR} # i.e., the project directory you made earlier
    $ python3 -m venv .venv
    $ . .venv/bin/activate

Now your command prompt probably looks something like:

    (.venv) tdelgado@detachment:~/projects/wimf $

### Setup the venv (Windows)

    > cd ${PROJECTDIR}
    > py -3 -m venv .venv
    > .venv\Scripts\activate

### Update pip and install Flask and pytest

Now, run:

    $ pip install --upgrade pip

To bring pip to the latest version, and then:

    $ pip install Flask==3.0.0 pytest==7.4.3

to install the specific versions of Flask and pytest we're using into
the venv we have created in the project directory.

### Notes

Don't forget to deactivate the venv by running the command
`deactivate` when you're done working with the project files! (Should
be the same across OSes.)

Note that this is a minimal install intended to get you started with
Flask using a venv (virtual environment), which segregates installed
versions of python libraries like pytest and flask and their
dependencies from the rest of your os and other projects.

If you're not using an IDE or other extensions like pyenv-virtualenv,
you will need to manually activate and deactiveate your venv every
time you change directories into the project directory.

### TODO: add how to reinstall using requirements.txt
### Test out your Flask install!

Follow the instructions
[here](https://flask.palletsprojects.com/en/3.0.x/quickstart/).

See if you can't get a basic page going!
## Step 3: Install sqlite3

We'll be using sqlite3 for our database. We're not going to be using
any particularly fancy features, so SQLite 3.40 or later [the version
on the current Ubuntu release] should do. Install from:
(https://www.sqlite.org/download.html)
