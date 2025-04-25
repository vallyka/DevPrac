#!/bin/bash

# Даем доступ к log-файлам
chmod -R go-w /usr/share/filebeat

# Запускаем Filebeat
filebeat -e -strict.perms=false -c /usr/share/filebeat/filebeat.yml