#!/usr/bin/env python3.6

def ageTeller (event, context):
    birtdateResponse = print("name was born on " + event.birthdate)
    ageResponse = print("Half of you age is " + (event.age / 2))
    return birthdateResponse
    return ageResponse
