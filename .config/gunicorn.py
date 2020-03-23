daemon = False
chdir = '/srv/daangn-market/app'
bind = 'unix:/run/daangn-market.sock'
accesslog = '/var/log/gunicorn/daangn-market-access.log'
errorlog = '/var/log/gunicorn/daangn-market-error.log'
capture_output = True