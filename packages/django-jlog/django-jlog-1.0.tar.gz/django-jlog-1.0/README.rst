Jlog
~~~~~~~~~~~

* A simple logging package that helps you save logs by days.

* Package is intended to write logs if you work with requests and responses during integration with third party APIs

* Date and time, log type (request/response), file path are added to every line

Installation
::

 pip install django-jlog

Set folder name in settings.py (by default it is `logs`)
::

 LOG_FOLDER_NAME='daily_logs'

Usage
::

 from jlog.file import Log


 Log.request('write here your request data', ['for', 'example'])

 Log.response('write here your response text message', {"testName": "Javid"})