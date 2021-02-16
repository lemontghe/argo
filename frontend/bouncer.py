#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Profile

with open("frontend/user_id", 'r') as f:
    a = int(f.readline())
if a != Profile.objects.all().count()+9999:
    f.write(str(Profile.objects.all().count()+9999))
