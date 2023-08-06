# py2hlog (Python to HTML log)
https://github.com/houshmand-2005/py2hlog

Python logs to HTML formatter

simple useage :
```bash
from py2hlog import logger
import time
obj1 = logger.py2hlog()  # create an object from py2hlog
obj1.file_name = "new_log_file.txt"  # here write the log detail
try:
    if a == 2:
        print("Iam working!")
except:
    obj1.error("I dont have any 'a' variable")
print("print obj1: ", obj1)
time.sleep(5)  # to see time changing
obj1.debug("Add a variable before the 'if' like a = 3")
obj1.makehtml("py2hlog.html")  # enter the name of output file
# you can also use these statuses :
# _____________________________
# obj1.critical("your message")
# obj1.debug("your message")
# obj1.info("your message")
# obj1.warning("your message")
# obj1.error("your message")
# _____________________________

```
<br>
Also you can mark a part of your code for each status like this:

```bash
from py2hlog import logger
object_of_py2hlog = logger.py2hlog()
object_of_py2hlog.file_name = "Py2hlog.txt"
object_of_py2hlog.warning("you can also mark a part of code for this status like -->", 1, 5)
# ("msg", start line, end line)
object_of_py2hlog.makehtml("Py2hlog.html")
```

**https://houshmand-2005.github.io/**
houshmand2005
