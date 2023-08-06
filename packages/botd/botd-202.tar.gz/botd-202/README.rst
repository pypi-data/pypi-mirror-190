

**NAME**

**BOTD** - 24/7 channel daemon


**SYNOPSIS**


``botctl <cmd> [key=value] [key==value]``


**DESCRIPTION**

**BOTD** is a solid, non hackable bot, that runs under systemd as a 24/7
background service and starts the bot after reboot, intended to be
programmable in a static, only code, no popen, no imports and no reading
modules from a directory.

**BOTD** is programmable, to program the bot you have to have the code
available as employing your own code requires that you install your own bot as
the system bot. This is to not have a directory to read modules from to add
commands to the bot but include the own programmed modules directly into the
python code, so only trusted code (your own written code) is included and
runnable. Reading random code from a directory is what gets avoided. As
experience tells os.popen and __import__, importlib are also avoided. 

**BOTD** stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence more chance.
Paths carry the type in the path name what makes reconstruction from filename
easier then reading type from the object.


**Only include your own written code should be the path to "secure".**


**INSTALL**

| ``sudo python3 -m pip install botd``
| ``sudo systemctl enable /usr/local//botd/botd.service --now``
|
| default channel/server is #botd on localhost
|

**CONFIGURATION**

| configuration is done by calling the ``icfg`` command of the bot.
| 

*irc*

| ``botctl icfg server=<server> channel=<channel> nick=<nick>``
| 

*sasl*

| ``botctl pwd <nickservnick> <nickservpass>``
| ``botctl icfg password=<outputfrompwd>``
|

*users*

| ``botctl icfg users=True``
| ``botctl met <userhost>``
|

*rss*

| ``botctl rss <url>``
|


| **COMMANDS**
|

the bot has the following commands:

| ``$ botctl cmd``
| ``cmd,dlt,dne,dpl,flt,fnd,ftc,icfg,met,mre,nme,pwd,rem,rss,thr,upt,ver``
|

here is a short description of the commands:

| ``cmd`` - shows all commands
| ``dlt`` - removes a user from bot
| ``dne`` - flag todo as done
| ``dpl`` - sets display items for a rss feed
| ``flt`` - shows a list of bot registered to the bus
| ``fnd`` - allows you to display objects on the datastore, read-only json files on disk 
| ``ftc`` - runs a rss feed fetching batch
| ``icfg`` - shows the irc configuration, also edits the config
| ``log`` - logs some text
| ``met`` - adds a users with there irc userhost
| ``mre`` - displays cached output, channel wise.
| ``nme`` - set name of a rss feed
| ``pwd`` - combines a nickserv name/password into a sasl password
| ``rem`` - removes a rss feed by matching is to its url
| ``rss`` - adds a feed to fetch, fetcher runs every 5 minutes
| ``thr`` - show the running threads
| ``tdo`` - adds a todo item, no options returns list of todo's
| ``upt`` - show uptime
| ``ver`` - show version
|


**AUTHOR**


| Bart Thate
| 

**COPYRIGHT**


| **BOTD** is placed in the Public Domain.
|
