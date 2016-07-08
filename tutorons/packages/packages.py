#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from django.db import connection

# List of packages that our Tutoron supports.
# This list is pulled from all packages for which data has been collected in the Search table.

cursor = connection.cursor()
cursor.execute("SELECT DISTINCT(package) FROM search")

results = cursor.fetchall()

# Call str() on each package in the list to convert from unicode string to regular string.
package_list = set()
for package in results:
    if package[0]:
        package_list.add(str(package[0]).lower())

print('Currently supporting the following packages: ' + str(package_list))
