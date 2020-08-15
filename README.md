Articles for my blog.
hosted on http://paundra.me

# How to use

```
python -m venv ~/venv/pelican
source ~/venv/pelican/bin/activate
pip install pelican[Markdown]
git clone git@github.com:agsha/pelicantheme.git
git clone git@github.com:agsha/myblog.git
git clone git@github.com:agsha/agsha.github.io.git
cd ~/code/agsha.github.io
pelican ~/code/myblog/content  -t ~/code/pelicantheme/simple -o .
```
