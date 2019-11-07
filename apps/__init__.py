from django.apps import AppConfig
from django.conf import settings

import os

class Config:
    exclude_content_type = {'id__gt': 9}
    
    class Directory:
        app          = os.path.dirname(os.path.realpath(__file__))
        certificates = '%s/certs' % settings.BASE_DIR
        cache        = '%s/cache' % settings.BASE_DIR
        logs         = '%s/logs' % settings.BASE_DIR

    class Test:
        search = ['none', '', 0, 'na', 'n/a', '-', '/', '\\', '?', '??', '#n/a', '#value!', 'nc', 'n/c', 'ns',]
        replace = ['_', ';', ',']
        intflt_toreplace = [' ', ',', '€', '$', '%']

    class Crypto:
        BS = 16

    class Log:
        logger = 'logger_{}'
        log_type = 'console'
        log_level = 7
        format_syslog = '[{}] {}'
        format_file = '{}:{}:{}.{} - {} | [{}] {}\n'
        format_console = '{}{}:{}:{}.{} - {} | [{}] {}{}'
        format_user = '{}.{} - {}'
        format_code = '{}_code'
        format_color = '{}_color'
        file_open_method = 'a'
        name_file = '{}/{}_{}_{}_{}.log'
        default_color = '\033[0m'
        emerg_code = 0
        emerg_color = '\033[1;93;5;101m'
        alert_code = 1
        alert_color = '\033[1;30;5;105m'
        crit_code = 2
        crit_color = '\033[1;97;5;101m'
        error_code = 3
        error_color = '\033[1;91;5;107m'
        warning_code = 4
        warning_color = '\033[0;91m'
        notice_code = 5
        notice_color = '\033[0;97m'
        info_code = 6
        info_color = '\033[0;94m'
        debug_code = 7
        debug_color = '\033[0;30;5;100m'

class MightyConfig(AppConfig, Config):
    name = 'mighty'
