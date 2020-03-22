daemon = False
chdir = '/srv/daangnMarket/app'
bind = 'unix:/run/daangnMarket.sock'
accesslog = '/var/log/gunicorn/daangnMarket-access.log'
errorlog = '/var/log/gunicorn/daangnMarket-error.log'
capture_output = True
