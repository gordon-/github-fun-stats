#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Damien Nicolas <damien@gordon.re>
#
# Distributed under terms of the MIT license.

"""
Parses all files in the data folder, and generates a cool table showing
thresholds for commits counts.
"""

import os
import sys
from datetime import datetime
import csv
import clize
from prettytable import PrettyTable


@clize.clize()
def main():
    """
    Parses the commits stats in the data folder, and shows thresholds for every
    color found.
    """

    if not os.path.isdir('data'):
        raise OSError('No data directory found')

    table = PrettyTable(['User', 'Date', '#1', '#2', '#3', '#4'])
    table.padding_width = 1

    files = os.listdir('data')
    for filename in files:
        with open(os.path.join('data', filename)) as csvfile:
            user_stats = csv.DictReader(csvfile)
            dashpos = filename.rfind('-')

            user_data = []
            user_data.append(filename[0:dashpos])
            user_data.append(datetime.strptime(filename[dashpos+1:],
                                               '%Y%m%d')
                                     .strftime('%d/%m/%Y'))
            cur_color = '#d6e685'  # the first color
            old_data = {'relative': 0.0, 'total': 0.0}
            for data in user_stats:
                if data['color'] != cur_color:
                    # we have a threshold!
                    user_data.append('%d%% %d%%' % (old_data['relative'],
                                                    old_data['total']))
                    cur_color = data['color']
                old_data = {'relative': float(data['relative_percentage'])
                            * 100,
                            'total': float(data['total_percentage']) * 100}

        user_data.append('%d%% %d%%' % (old_data['relative'],
                                        old_data['total']))
        table.add_row(user_data)

    print(table)


if __name__ == '__main__':
    try:
        clize.run(main)
    except Exception as e:
        print(e)
        sys.exit(1)
