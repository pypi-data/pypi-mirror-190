# ScreenRun

Process management done simple. You can keep a process running forever just by adding a single cron job.


# Install

```bash
pip install screenrun
```


# Usage

```bash
> screenrun execute --name nap sleep 60
> screenrun list
nap
> screenrun kill --name nap
> screenrun persist --name nap sleep 60
> screenrun persist --name nap sleep 60
```

## Add to cron
```bash
* * * * * screenrun cron sleep 60
```

## Python
```python3
from screenrun import ScreenRun

screenrun = ScreenRun()

screenrun.execute('sleep 60')
```

