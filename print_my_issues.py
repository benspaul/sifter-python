#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       print_my_issues.py
#       
#       Copyright 2012 Mark Mikofski <marko@bwanamaro@yahoo.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

import account
import time
from time import mktime
from datetime import datetime, timedelta, date

def get_date(d):
   return datetime.fromtimestamp(mktime(time.strptime(d, '%Y-%m-%dT%H:%M:%SZ'))).date()

### customize with your information ###

account_name = ''
token = ''
opener_name = ''
start_date = date(2013, 7, 20)
include_archived = True

#######################################

a = account.Account(account_name, token, include_archived)

f = open('index.html', 'w')
f.write('<html><body><ol>')

projs = a.projects()

for proj in projs:
   issues = proj.issues()
   for i in issues:
     if i.opener_name.lower() != opener_name.lower(): continue
     if get_date(i.created_at) < start_date: continue
     if i.priority.lower() == 'trivial': continue
     if i.category_name:
        if i.category_name.lower() == 'not an issue': continue
        if i.category_name.lower() == 'unsure if it\'s an issue': continue
    
     printable_subject = i.subject.encode('ascii', 'ignore')
     f.write('<li><a href="%s">%s</a> - %s, %s, %s, %s</li>' % (i.url, printable_subject, proj.name, i.priority, i.category_name, i.created_at))

f.write('</ol></body></html>')
f.close()
