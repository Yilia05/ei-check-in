# ci-check-in

Automatic check in tool for eBay Shanghai interns, written in python 3.

## Installation

1. Install [Selenium](https://pypi.python.org/pypi/selenium) 

```
pip3 install selenium
```

2. Dowload [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/)

3. Fill in your username and password.

```
cp secret.json.template secret.json
```

Then fill in your username and password in `secret.json`.

## Usage

Note that the check in will check both morning and afternoon.

This will check in for today.

```
python3 check-in.py today
```

This will check-in for August 29, 30, 31 in 2017, and if any day in these three days is not a weekday(Monday to Friday), the tool will skip that day.

```
python3 check-in.py mul -d 2017-08-29 -l 3
```

Get help.

```
python3 check-in.py -h
python3 check-in.py mul -h
python3 check-in.py today -h
```

## Auto check in every day (mac)

```
crontab -e
```

Add the following line and replace `/Users/hanhu/Documents/CodeSpace/gitRepository` with the path your `ei-check-in` is at.

```
# m h  dom mon dow   command
  0 10  *   *   *        python3 /Users/hanhu/Documents/CodeSpace/gitRepository/ei-check-in/src/check-in.py today
```

Use `crontab -l` to check your cron job.

If you have any improvements, welcome to fork, edits and pull requests.
