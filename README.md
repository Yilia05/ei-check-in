# ci-check-in

Automatic check in tool for eBay Shanghai interns.

## Installation

1. Install [Selenium](https://pypi.python.org/pypi/selenium) 

```
$ pip install selenium
```

2. Dowload [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/)

## Usage

Set `startdate = "2017-08-21"` and `length = 3` in the code and it will call chrome to check in at 21, 22, 23 for you. If any day in these three days is not weekday, the tool will skip but that weekend will also count for one day in `length.
Note that the check in will check both morning and afternoon.

If you have any improvements, welcome to fork, edits and pull requests.