import configparser
config_writer = configparser.ConfigParser()

def create_ini(aws_access_key_id, aws_secret_access_key, region_name):
    config_writer['Account'] = {}
    config_writer['Account']['aws_access_key_id'] = aws_access_key_id
    config_writer['Account']['aws_secret_access_key'] = aws_secret_access_key
    config_writer['Account']['region_name'] = region_name

    with open('account.ini', 'w') as configfile:
        config_writer.write(configfile)