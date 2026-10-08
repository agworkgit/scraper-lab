# News Trends Dashboard

Replace `PROJECT` with your project folder (the output of `pwd`). Your scraper file is called `step9.py`.

**One-time setup (only if starting from scratch)**

```
cd PROJECT
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 feedparser vaderSentiment pandas streamlit
```

**Start everything**

Run the scraper once by hand, to check it works:

```
cd PROJECT
source .venv/bin/activate
python step9.py
```

Start the schedule (the scraper then runs every 3 hours on its own):

```
systemctl --user daemon-reload
systemctl --user enable --now news-scraper.timer
```

Open the dashboard:

```
cd PROJECT
source .venv/bin/activate
streamlit run app.py
```

**Check on it**

```
systemctl --user list-timers          # when the next run is due
systemctl --user status news-scraper.service   # result of the last run
cat PROJECT/scraper.log               # what the scraper printed
tail -f PROJECT/scraper.log           # watch the log live (Ctrl+C to leave)
```

To trigger a run right now without waiting for the timer:

```
systemctl --user start news-scraper.service
```

**Stop everything**

Stop the dashboard by pressing `Ctrl+C` in the terminal where it's running.
Stop the schedule (this also keeps it from starting again at login):

```
systemctl --user disable --now news-scraper.timer
```

Leave the virtual environment:

```
deactivate
```

**Remove the schedule completely**

```
systemctl --user disable --now news-scraper.timer
rm ~/.config/systemd/user/news-scraper.service ~/.config/systemd/user/news-scraper.timer
systemctl --user daemon-reload
```

Your data stays in `books.db`, and none of these commands touch it. To wipe the data, delete that file yourself.
