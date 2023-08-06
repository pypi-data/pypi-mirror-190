import configloaders

# network
host = '0.0.0.0'
port = 5207

# aligo
login_timeout = 120.
cooldown_time = 5.
create_folder_if_remote_exist = True
sync_interval = 10*60.

# log
log_level = 'INFO'


configloaders.load_ini(globals())