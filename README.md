## What is this?
> log_ship can be configured to retrieve files older than N days from multiple folders
> and possibly ship these to S3 and/or delete found files.

## How to get started?
> create a virtualenv  `virtualenv --python=python3 /home/user_name/.virtualenv/log_ship`

> switch to virtualenv  `source /home/user_name/.virtualenv/log_ship/bin/activate`

> install required modules `pip install -r requirements.txt`

> run application `python log_ship.py`

**Note:** Most likely you want to tweak some configuration params in `settings.py` before running

## How to configure?
> `settings.py` provides configuration options to configure -

>> folders to watch `CONST_DIRECTORIES_TO_WATCH`

>> How old files must be to consider for actions `CONST_NUM_DAYS_CUTOFF`

>> AWS configuration `AWS_CONFIG`

>> log_ship log file path `SELF_LOG_FILE_PATH`

*and much more*

**Note:** If you see permission errors if is most likely that folders are you accessing need sudo for access

## Can we run this every few hours on a linux machine?
> Glad that you asked. You could use cron or systemd. You can take following steps for performing via systemd

>To use systemd timers, we must first create a .service file for the command we want to run:

```
# /etc/systemd/system/log-ship.service
# assumes log_ship.py is present in /opt/log_ship

[Unit]
Description=Runs log_ship.py

[Service]
Type=oneshot
ExecStart=/home/mahorir/.virtualenvs/log_ship/bin/python log_ship.py
WorkingDirectory=/opt/log_ship/
StandardOutput=inherit
StandardError=inherit
User=root

[Install]
WantedBy=default.target
Alias=log-ship.service
```

>Now we create the matching .timer file - note that the timer and service files must have the same name:

```
# /etc/systemd/system/log-ship.timer
[Unit]
Description=Run log_ship every day at 06:00

[Timer]
OnCalendar=*-*-* 06:00:00
Persistent=True

[Install]
WantedBy=timers.target
```

> Now, tell systemctl about the changes

```
$ systemctl daemon-reload
```

> Enable the timer. This is how, every boot timer is activated.

```
$ systemctl enable log_ship.timer
```

> Start timer right away (if you want) [Optional]

```
$ systemctl start log_ship.timer
```

> At this point you may want to do a manual run to make sure it works.[Optional]

```
$ systemctl start log_ship.service
```