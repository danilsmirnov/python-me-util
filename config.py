import os


class Config:

    PD_URL = 'https://my.pingdom.com'
    PD_LOGIN = os.environ['PD_LOGIN']
    PD_PASSWORD = os.environ['PD_PASSWORD']

    NR_URL = 'https://login.newrelic.com/login'
    NR_LOGIN = os.environ['NR_LOGIN']
    NR_PASSWORD = os.environ['NR_PASSWORD']

    SLACK_URL = 'https://phypartners.slack.com/ssb/redirect'