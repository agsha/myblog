Date: 2016-02-21 10:20
Tags: regex
Authors: Sharath Gururaj
Title: Regex recipes
disqus_identifier: regex_recipes

I find myself always having to google around a lot for common regex recipes. Surprisingly, the most common cases cannot be easily found without extensive grokking.

### Python examples

#### Common special characters:
`\d`: only digit, 


Search for occurences of a regex string and replace it with something that depends on the actual value of the string.

````
import re
p = re.compile(r"(blue|red)")
print p.sub(lambda m: str(len(m.group())), "blue socks and red shoes")
````

output: `4 socks and 3 shoes`

