[program:car_command_server]
directory = {{ source_path }}
user = {{ app_user }}
command = {{ virt_env_path }}/bin/python {{ source_path }}/command_server.py
stdout_logfile = /var/log/command_server.log
stderr_logfile = /var/log/command_server.error