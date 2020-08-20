#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import re
import urllib

whitespace = re.compile(r"\s+")
def get_googletime(location):
   query = 'https://www.google.co.nz/search?' + urllib.parse.urlencode({'q': 'time ' + location})
   response = requests.get(query, headers={
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'})
   soup = BeautifulSoup(response.text, 'html.parser')
   result = soup.find('h2').parent.find('div').get_text()
   if result.find('Time in ') > -1:
      # Tidy it up
      result = whitespace.sub(" ", result).strip().replace('Time in ', "")
      parts = re.split('^(\d{1,2}):(\d{1,2}) ((a|p)m)(.*)', result)
      if len(parts) != 7:
         result = "Unknown input format \"{}\"".format(result)
      else:
         hour = int(parts[1])
         minute = parts[2]
         tod = parts[3]
         rest = parts[5]
         if tod == 'pm':
            hour = hour + 12
         result = "{:02d}:{}{}".format(hour, minute, rest)
   else:
      result = "Couldn't find time for \"{}\"".format(location)
   return result

try:
   import sopel.module
except ImportError:
   pass
else:
   @sopel.module.commands('time')
   @sopel.module.example('.time location')
   def f_etymology(bot, trigger):
      """Look up the time at a location"""
      if trigger.group(2):
         result = get_googletime(trigger.group(2))
      bot.say(result, trigger.sender, len(result)*2)
      return sopel.module.NOLIMIT

if __name__ == '__main__':
   import sys
   query = 'London'
   if len(sys.argv) > 1:
      query = ' '.join(sys.argv[1:])
   print('Looking up time for "{}"'.format(query))
   print(get_googletime(query))
