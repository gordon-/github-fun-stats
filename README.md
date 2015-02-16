# Github commits graph analyzer

This simple tool parses Github's commit graph that is shown on every user
profile, and then creates stat graphs in order to retro-engineer their algo.

## Installation

If you're using `virtualenv`, type:

    pip install -r requirements.txt

If you're not, you should change your habits. However, you can install
dependencies with:

    pip install --user -r requirements.txt

## Usage

You first have to gather some data. Use the following command to fetch an user's
commit graph stat.

    python3 get_stats.py <username>

Where `<username>` is a Github's username. A stat file is written in a `data`
directory.

After some stats are gathered, you can display the summary with:

    python3 parse_stats.py

That's it! The output shows a line for every file, and the maximum percentage of
the maximum commit count that renders that color. The second value of each
column is the maximum number of commits compared to the total commit number.

I honestly don't know if those values can be useful, this script is just a test.
