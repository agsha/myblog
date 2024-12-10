Articles for my blog.
hosted on http://paundra.me
This content is deprecated. Please refer to https://github.com/agsha/pelicanblog

# How to use

```bash
python -m venv ~/venv/pelican
source ~/venv/pelican/bin/activate
pip install pelican[Markdown]
git clone git@github.com:agsha/pelicantheme.git
git clone git@github.com:agsha/myblog.git
git clone git@github.com:agsha/agsha.github.io.git
cd ~/code/agsha.github.io
pelican ~/code/myblog/content  -t ~/code/pelicantheme/simple -o .
```

To enable code highlighting, we need to generate a style sheet (that I've already checked in) by

```bash
cd ~/code/pelicantheme
pygmentize -S default -f html -a .highlighttable > simple/static/hilite.css
pygmentize -S default -f html -a .highlight >> simple/static/hilite.css
```

To convert urls in cookbook and generate, use 
````bash
cd ~/code/myblog
python3 converturl.py /code/myblog/content/cookbook.md
````