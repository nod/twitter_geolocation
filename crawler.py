#!/usr/bin/env python

import sys
import commands
import re
from BeautifulSoup import BeautifulSoup
from location import loc,ltweet
from optparse import OptionParser

def tattrs(tweet):
#    print "  tweet: %s" % unicode(tweet.string)
    i = re.compile("\d+")
    id = i.findall(tweet.parent.parent.parent['id'])[0].encode('ASCII')
    t = re.compile("title=\"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})")
    time = tweet.next.next.next.next.next
    time = t.findall(unicode(time).encode('ASCII'))[0]
#    print "    id: %s; time: %s" % (id,time)
#    print [id,time]
    return [id,time]
    

def main():
    (options, args) = parser.parse_args()
    if options.f:
        ufile = open(options.u,'w')
        print >>ufile,options.f
        ufile.close()
    else:
        statout = commands.getstatusoutput('ls '+options.d+' > '+options.u)
    users = open(options.u,'r')         #user listing
    out = open(options.o,'w')           #output file
    if options.s: #if no output file
        out = sys.stdout #print to stdout
    numusers = 0.0                      #number of users
    locusers = 0.0                      #number of users with location
    coordusers = 0.0                    #number of users with coordinates
    twtusers = 0.0                      #number of users using l:____
    for line in users: #for each user in listing
        numusers += 1
        user = options.d+line[0:-1] #absolute path to user page
        username = user[user.rfind('/')+1:user.rfind('.')] #isolate username
        print username #TEMPORARY
        if options.v: #verbose option
            print >>out,"username: %s" % username
        page = open(user,'r')
        contents = page.read()          #user page contents (html)
        page.close()
        location = loc(contents)
        if options.v: #verbose option
            print >>out,location[0]
        if location[1]: #coordinates specified
            print >>out,"%s : %s : %s" % (username,location[0],location[1])
            locusers += 1
            coordusers += 1
        elif location[0]: #location (no coordinates) specified
            print >>out,"%s : %s" % (username,location[0])
            locusers += 1
        tweets = ltweet(contents)
        if tweets: #l:___ found
            print >>out,"%s" % tweets
            twtusers += 1
        soup = BeautifulSoup(contents)
        tweets = soup.findAll("span", "entry-content")
        for tweet in tweets:
            if ltweet(unicode(tweet.string)):
                print "  tweet: %s" % unicode(tweet.string)
                pair = tattrs(tweet)
                print "    id: %s; time: %s" % (pair[0],pair[1])

    percent = locusers/numusers         # % users with location 
    pcoord = coordusers/numusers        # % users with coordinates
    plcoord = coordusers/locusers       # % locations that have coordinates
    ptweet = twtusers/numusers          # % users using l:____
    print >>out,"\n"
    print >>out,"number of users: %d" % numusers
    print >>out,"number of users with location: %d" % locusers
    print >>out,"percentage users with location: %f" % percent
    print >>out,"number of users with coordinates: %d" % coordusers
    print >>out,"percentage users with coordinates: %f" % pcoord
    print >>out,"percentage location users with coordinates: %f" % plcoord
    print >>out,"number of users using l:____: %d" % twtusers
    print >>out,"percentage users using l:____: %f" % ptweet
    users.close()

parser = OptionParser()
parser.add_option(                      #verbose
    "-v",
    "--verbose",
    action="store_true",
    dest="v",
    default=False,
    help="turn on verbose mode" )
parser.add_option(                      #directory with user pages
    "-d",
    "--directory",
    dest="d",
    metavar="DIR",
    default="/project/wdim/crawlData/good_sample/",
    help="directory to find user pages in" )
parser.add_option(                      #one file in directory
    "-f",
    "--file",
    dest="f",
    metavar="ONLY_FILE",
    default=False,
    help="single file in directory to run")
parser.add_option(                      #file for user listing
    "-u",
    "--ufile",
    dest="u",
    metavar="USER_FILE",
    default="users.txt",
    help="file to write user page names to")
parser.add_option(                      #use stdout for output
    "-s",
    "--stdout",
    action="store_true",
    dest="s",
    default=False,
    help="use standard output instead of output file")
parser.add_option(                      #output file
    "-o",
    "--outfile",
    dest="o",
    metavar="OUTPUT_FILE",
    default="cData.txt",
    help="file to write output of location data extracted by crawl")

if __name__ == "__main__":
    main()
