#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Damien Nicolas <damien@gordon.re>
#
# Distributed under terms of the MIT license.

"""
This script makes some stats for a Github user's commit count and stores them
in a flat file
"""

import os
import sys
from datetime import datetime
import csv
from operator import itemgetter
import clize
from pyquery import PyQuery


@clize.clize()
def main(username):
    """
    Parses the Github account page for the given username, and stores the
    maximum commit count value, the percentage of max commits and the color for
    every color in a file in the data dir, named <username>-<date>
    """

    # throwing away bad usernames
    if '/' in username:
        raise ValueError('The username can\'t contain slashes')

    if not os.path.isdir('data'):
        os.mkdir('data')

    print('Fetching and parsing Github page')

    url = 'https://github.com/%s/' % username

    doc = PyQuery(url=url)

    rects = doc('svg rect')
    if not len(rects):
        raise Exception('No commits graph found.')

    print('%d days found. Processing data.' % len(rects))

    colors = []
    max_commits = 0
    total_commits = 0
    # initial fetch
    for rect in rects:
        count = int(rect.attrib['data-count'])
        if count:  # we don't want to track empty days
            if count > max_commits:
                max_commits = count
            total_commits += count

            colors.append({'count': count, 'color': rect.attrib['fill']})

    # second loop, cause we now have total number of commits, and max commits
    # count
    for color_data in colors:
        total_percentage = round(color_data['count'] / total_commits, 2)
        relative_percentage = round(color_data['count'] / max_commits, 2)
        color_data['total_percentage'] = total_percentage
        color_data['relative_percentage'] = relative_percentage

    # sorting the colors by commits count
    colors = sorted(colors, key=itemgetter('count'))

    filename = '%s-%s' % (username, datetime.now().strftime('%Y%m%d'))
    filepath = os.path.join('data', filename)

    with open(filepath, 'w') as csvfile:
        fieldnames = colors[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                dialect=csv.unix_dialect)
        writer.writeheader()
        writer.writerows(colors)

    print('Done. Data is saved in %s' % filepath)


if __name__ == '__main__':
    try:
        clize.run(main)
    except Exception as e:
        print(e)
        sys.exit(1)
