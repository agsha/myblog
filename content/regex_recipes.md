Date: 2016-02-21 10:20
Tags: regex
Authors: Sharath Gururaj
Title: Regex recipes
disqus_identifier: regex_recipes

I find myself always having to google around a lot for common regex recipes. Surprisingly, the most common cases cannot be easily found without extensive grokking.

### Python examples

#### Common special characters:
`\d`: only digit, 

#### Search and replace
Search for occurences of a regex string and replace it with something that depends on the actual value of the string.

````python
import re
p = re.compile(r"(blue|red)")
print p.sub(lambda m: str(len(m.group())), "blue socks and red shoes")
````

    :::python
    print("The triple-colon syntax will *not* show line numbers.")



output: `4 socks and 3 shoes`

#### Find all ip addresses in a text

````
p = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[^0-9]")
s = "Runbook:blah blah  IP:10.34.249.124 blah blah IP:10.33.157.166"
print p.findall(s)
````