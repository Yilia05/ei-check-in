# ei-check-in

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

The `PATH` apply to all cron job, use `echo $PATH` to get the normal `PATH` in your terminal and paste it here.

```
PATH=/Users/hanhu/.nvm/versions/node/v8.2.1/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Java/JavaVirtualMachines/jdk1.8.0_144.jdk/Contents/Home/bin:/Users/hanhu/Downloads/hadoop-2.6.5/bin:/Users/hanhu/Downloads/hadoop-2.6.5/sbin:/usr/local/Cellar/scala/bin:/Users/hanhu/Downloads/apache-hive-1.2.2-bin/bin:/Users/hanhu/Documents/Programs/spark-1.6.0-bin-hadoop2.6/bin:/Users/hanhu/Documents/Programs/chromedriver:/Users/hanhu/Documents/Programs/phantomjs-2.1.1-macosx/bin:/usr/local/Cellar/python3/3.6.2/bin
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5   *   *   1       tar -zcf /var/backups/home.tgz /home/
# m h  dom mon dow   command
  0 10  *   *   *        python3 /Users/hanhu/Documents/CodeSpace/gitRepository/ei-check-in/src/check-in.py today >/tmp/stdout.log 2>/tmp/stderr.log
```

You can read command execution information in `/tmp/stdout.log` and `/tmp/stderr.log`.

Use `crontab -l` to check your cron job.

If you have any improvements, welcome to fork, edits and pull requests.
