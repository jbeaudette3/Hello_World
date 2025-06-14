# **<font color="White">Introduction</font>**

Welcome to **Hello_World**, a Python project created as an introduction into long-term automation.

Start:
 - I enjoy automation and data collection, as well as art.

Question:
 - How can I write out 'Hello World' in the GitHub contribution chart?

---

## **<font color=0x00ff00>Goals</font>**

The goal of this project is:

- Learn how to automate projects and data collection to run on a long-term, non-sequential/customized basis.

- Future Goal: create artwork using various shades.

---
## _<font color="orange">Components/ considerations</font>_

- YAML file  
  - This file is used by GitHub Actions to control the automation process.
  - Using Crontab, Schedule python script to run.  
  - To ensure the contribution chart color is dark enough, once a day is not enough; this was scheduled to run 3x/ day for a total of 6 commits.
   - I discovered Github's crontab functions differently than Linux; multiple runs per day require separate cron entries in Github actions, writing the hours as '8,12,16' would not be considered valid.

- Timezones
  - Github actions runs on UTC time, however the specific timing of the data I wanted to collect needs to be convered to a different timezone. Additionally, I need to ensure the timezone used by Github doesn't bleed into the following day in my local time, thus messing up the final result.
  - Additionally, scheduling at 9:00 am, for example, the script may not run until 9:30 am. Consider this delay in data collection.  

- Data to collect
   - Options:
     - Random data could be used.
     - If this project is going to be run over a long time period, I might as well have the data be useful to some extent.
   - Currently using the City of Chicago's Data portal (https://data.cityofchicago.org/)


- API key
  - API key to connect to Github can be indefinite or active for a set length.
  - I wanted to ensure the key would be valid throughout the run-time of the script but remove access after final commit is made.

---
## Steps
In a spreadsheet:
- Create pattern mimicking Github's layout.  

In a separate program *(listed as format_pattern.py)*:
- Convert the pattern into days of the month; pattern to be a list of dates.

**VALIDATE**  
**VALIDATE**  
**VALIDATE**  

- Ensure the dates in the list are correct, in as many different ways as possible.
  - Is each date listed 3 times?
  - Are all the dates in the list correct?
  - In choosing random dates in the list, spot-check to ensure it belongs.
  - Re-creatd Github's format in a spreadsheet and use conditional formatting. If date in list, highlight.

In main program:
- Check if list of dates file exists. If not, assume it's the end and exit the program.
- If the list of dates file exists BUT it's empty, delete it.
- Get today's date. If today is in the list:
  - Remove date from the list. Commit.
  - Get SHA and path from current Github-hosted data file; used in commit.
  - Get data from Chicago's data website.
    - if there's no current data file on Github, create one.
    - Else, update existing file. Commit.
- Let run for the next 10 months.

---
## Initial issues:
- I originally tried to run this on a raspberry pi, however the main issue came about with potential power loss. If the computer restarted, what happens if the main program is interrupted, how do I keep track of where I am in the sequence, etc.
