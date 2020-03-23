daemon = False
chdir = '/srv/daangn-market/app'
bind = 'unix:/run/daangnMarket.sock'
accesslog = '/var/log/gunicorn/daangn-market-access.log'
errorlog = '/var/log/gunicorn/daangn-market-error.log'
capture_output = True
