# -*- coding: utf-8 -*-

print "Loading event handler..."
def handler(event, context):
    print "Hello world"
    print event
    # Your code goes here!
    e = event.get('e')
    pi = event.get('pi')
    return "OK"
