#!/usr/bin/env python3

import argparse
import argcomplete
import hashlib
import json
import os
import re
import subprocess
from subprocess import PIPE, Popen, STDOUT
import sys
from configparser import ConfigParser
from datetime import datetime, timedelta
from pathlib import Path
import signal

import boto3
import inquirer
from dateutil.parser import parse
from dateutil.tz import UTC, tzlocal

AWS_CONFIG_DIR = f'{Path.home()}/.aws'
AWS_CONFIG_PATH = f'{Path.home()}/.aws/config'
AWS_CREDENTIAL_PATH = f'{Path.home()}/.aws/credentials'
AWS_SSO_CACHE_PATH = f'{Path.home()}/.aws/sso/cache'
AWS_DEFAULT_REGION = 'us-west-1'
CURRENT_REGION = os.getenv('AWS_REGION')

default_config = {
  'sso_start_url': 'https://hireteammate.awsapps.com/start',
  'sso_region': 'us-west-2',
  'sso_account_id': '780323805217',
  'sso_role_name': 'default',
  'region': 'us-west-1',
  'output': 'json'
}

account_map = {
    'HireEz-OPS1': ['ops1', 'us-west-1'],
    'Hiretaul Resold': ['Master', 'us-west-2'],
    'Stage': ['stage', 'us-west-1'],
    'HireEz-PROD2': ['prod2', 'us-west-2'],
    'prod': ['prod', 'us-west-1'],
    'HireEz-TEST': ['test1', 'us-west-1'],
    'HireEz-STAGE': ['stage1', 'us-west-1'],
    'Test': ['test', 'us-west-1'],
    'HireEz-OPS2': ['ops2', 'us-west-2'],
    'HireEz-PROD1': ['prod1', 'us-west-1']
}

if not os.path.exists(AWS_CONFIG_DIR):
    config_dir = Path(AWS_CONFIG_DIR)
    config_dir.mkdir(parents=True)

def main():
    parser = argparse.ArgumentParser(description='Retrieves AWS credentials from SSO for use with CLI/Boto3 apps.')
    subparsers = parser.add_subparsers()

    parser_sso = subparsers.add_parser('sso')
    parser_sso_sub = parser_sso.add_subparsers()
    parser_sso_config = parser_sso_sub.add_parser('config',
                        help='config aws sso.')
    parser_sso_config.set_defaults(func=_sso_config)

    parser_sso_login = parser_sso_sub.add_parser('login',
                        help='ssm login into sso.')
    parser_sso_login.set_defaults(func=_sso_login)

    parser_sso_switch = parser_sso_sub.add_parser('switch',
                        help='switch to another config.')
    parser_sso_switch.set_defaults(func=_sso_switch)

    parser_sso_logout = parser_sso_sub.add_parser('logout',
                        help='logout aws sso.')
    parser_sso_logout.set_defaults(func=_sso_logout)


    parser_tf = subparsers.add_parser('tf')
    parser_tf.add_argument('cmd',
                        nargs='*',
                        help='terraform command, eg: init plan apply destroy')
    parser_tf.set_defaults(func=_tf_cmd)

    parser_ec2 = subparsers.add_parser('ec2')
    parser_ec2_sub = parser_ec2.add_subparsers()
    parser_ec2_search = parser_ec2_sub.add_parser('search')

    parser_ec2_search.add_argument('search',
                        help='search out ec2 instance id by keyword: ip, name')
    parser_ec2_search.set_defaults(func=_ec2_search)

    parser_ec2_login = parser_ec2_sub.add_parser('login')
    parser_ec2_login.add_argument('login',
                        help='ssm login into ec2.')
    parser_ec2_login.set_defaults(func=_ec2_login)


    parser_sm = subparsers.add_parser('sm')
    parser_sm_sub = parser_sm.add_subparsers(help='sub func: search, create, update')
    parser_sm_search = parser_sm_sub.add_parser('search')
    parser_sm_search.add_argument('search',
                        help='search secrets manager')
    parser_sm_search.set_defaults(func=_sm_search)

    parser_sm_create = parser_sm_sub.add_parser('create')
    parser_sm_create.add_argument('create',
                        action='store_true',
                        help='create secrets manager')
    parser_sm_create.set_defaults(func=_sm_create)

    parser_sm_update = parser_sm_sub.add_parser('update')
    parser_sm_update.add_argument('update',
                        help='update secrets manager')
    parser_sm_update.set_defaults(func=_sm_update)

    parser_sm_delete = parser_sm_sub.add_parser('delete')
    parser_sm_delete.add_argument('delete',
                        help='delete secrets manager')
    parser_sm_delete.set_defaults(func=_sm_delete)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if len(sys.argv)==1:
        parser.print_help()
    if len(sys.argv) == 2 and sys.argv[1] in subparsers.choices:
        print(subparsers.choices[sys.argv[1]].format_help())

    # validate aws v2
    try:
        aws_version = subprocess.run(['aws', '--version'], capture_output=True).stdout.decode('utf-8')

        if 'aws-cli/2' not in aws_version:
            print('\n AWS CLI Version 2 not found. Please install. Exiting.')
            exit(1)

    except Exception as e:
        print('\nAn error occured trying to find AWS CLI version. Do you have AWS CLI Version 2 installed?\n{e}')
        exit(1)

    if hasattr(args, 'func'):
        if args.func == _sso_config:
            _sso_config()
        if args.func == _sso_login:
            _sso_login()
        if args.func == _sso_switch:
            _sso_switch()
        if args.func == _sso_logout:
            _sso_logout()
        if args.func == _tf_cmd:
            _tf_cmd(args.cmd)
        if args.func == _ec2_search:
            _ec2_search(args.search)
        if args.func == _ec2_login:
            _ec2_login(args.login)
        if args.func == _sm_search:
            _sm_search(args.search)
        if args.func == _sm_create:
            _sm_create()
        if args.func == _sm_update:
            _sm_update(args.update)
        if args.func == _sm_delete:
            _sm_delete(args.delete)

def _sso_config():
    _spawn_cli_for_config()
    sys.exit()

def _sso_switch():
    profile = _add_prefix(_select_profile())
    profile_opts = _get_aws_profile(profile)
    profile_name = profile.split(' ')[1]
    output = '''
Please execute below commands:

export AWS_ENVS={0}
export AWS_REGION={1}
export AWS_ACCOUNT={2}
export AWS_BUCKET={0}-terraform-state-{2}
export AWS_PROFILE={3}
export TF_VAR_aws_region={1}
export TF_VAR_bucket_name={0}-terraform-state-{2}
export TF_VAR_cluster_name={0}
export AWS_DEFAULT_REGION={1}
export PS1="{0} $ "
aws eks --region {1} update-kubeconfig --name {0}
    '''.format(profile_name.split('_')[0], profile_opts['region'], profile_opts['sso_account_id'], profile_name)
    print(output)
    _set_profile_credentials(profile)

def _sso_logout():
    select_one = True
    profile = _add_prefix(_select_profile(select_one))
    _spawn_cli_for_logout(profile)


def _sso_login():
    select_one = True
    profile = _add_prefix(_select_profile(select_one))
    _spawn_cli_for_auth(profile)
    _set_profile_credentials(profile)

def _tf_cmd(cmd):
    if len(cmd) == 0:
        sys.exit()
    if cmd[0] == 'init':
        subprocess.run(['rm', '-rf', '.terraform'],
                       stderr=sys.stderr,
                       stdout=sys.stdout,
                       check=True)
        subprocess.run(['terraform', 'init', '-backend-config=region={}'.format(os.getenv('AWS_REGION')), '-backend-config=bucket={}'.format(os.getenv('AWS_BUCKET'))],
                       stderr=sys.stderr,
                       stdout=sys.stdout,
                       check=True)
    else:
        subprocess.run(['terraform'] + cmd,
                       stderr=sys.stderr,
                       stdout=sys.stdout,
                       check=True)

def _set_profile_credentials(profile_name, use_default=False):
    profile_opts = _get_aws_profile(profile_name)
    cache_login = _get_sso_cached_login(profile_opts)
    credentials = _get_sso_role_credentials(profile_opts, cache_login)

    _store_aws_credentials('default', profile_opts, credentials)
    _copy_to_default_profile(profile_name)


def _get_aws_profile(profile_name):
    config = _read_config(AWS_CONFIG_PATH)
    profile_opts = config.items(profile_name)
    profile = dict(profile_opts)
    return profile


def _get_sso_cached_login(profile):

    cache = hashlib.sha1(profile["sso_start_url"].encode("utf-8")).hexdigest()
    sso_cache_file = f'{AWS_SSO_CACHE_PATH}/{cache}.json'

    if not Path(sso_cache_file).is_file():
        print('Current cached SSO login is invalid/missing. Login with the AWS CLI tool or use --login')

    else:
        data = _load_json(sso_cache_file)
        now = datetime.now().astimezone(UTC)
        expires_at = parse(data['expiresAt']).astimezone(UTC)

        if data.get('region') != profile['sso_region']:
            print('SSO authentication region in cache does not match region defined in profile')

        if now > expires_at:
            print('SSO credentials have expired. Please re-validate with the AWS CLI tool or --login option.')

        if (now + timedelta(minutes=15)) >= expires_at:
            print('Your current SSO credentials will expire in less than 15 minutes!')

        print('Found credentials. Valid until {}'.format(expires_at.astimezone(tzlocal())))
        return data


def _get_sso_role_credentials(profile, login):

    client = boto3.client('sso', region_name=profile['sso_region'])
    response = client.get_role_credentials(
        roleName=profile['sso_role_name'],
        accountId=profile['sso_account_id'],
        accessToken=login['accessToken'],
    )

    expires = datetime.utcfromtimestamp(response['roleCredentials']['expiration'] / 1000.0).astimezone(UTC)
    print('Got session token. Valid until {}'.format(expires.astimezone(tzlocal())))

    return response["roleCredentials"]


def _store_aws_credentials(profile_name, profile_opts, credentials):

    region = profile_opts.get("region", AWS_DEFAULT_REGION)
    config = _read_config(AWS_CREDENTIAL_PATH)

    if config.has_section(profile_name):
        config.remove_section(profile_name)

    config.add_section(profile_name)
    config.set(profile_name, "region", region)
    config.set(profile_name, "aws_access_key_id", credentials["accessKeyId"])
    config.set(profile_name, "aws_secret_access_key ", credentials["secretAccessKey"])
    config.set(profile_name, "aws_session_token", credentials["sessionToken"])

    _write_config(AWS_CREDENTIAL_PATH, config)


def _copy_to_default_profile(profile_name):

    config = _read_config(AWS_CONFIG_PATH)

    if config.has_section('default'):
        config.remove_section('default')

    config.add_section('default')

    for key, value in config.items(profile_name):
        config.set('default', key, value)

    _write_config(AWS_CONFIG_PATH, config)


def _select_profile(select_one=False):
    config = _read_config(AWS_CONFIG_PATH)

    profiles = []
    for section in config.sections():
        profiles.append(str(section).replace('profile ', ''))
    profiles.sort()
    if select_one is True:
        return profiles.pop()
    try:
        profiles.pop(profiles.index('default'))
    except:
        pass

    questions = [
        inquirer.List(
            'name',
            message='Please select an AWS config profile',
            choices=profiles
        ),
    ]
    answer = inquirer.prompt(questions)
    return answer['name'] if answer else sys.exit(1)

def _gen_config_file():
    config = ConfigParser()
    dir = os.path.expanduser(AWS_SSO_CACHE_PATH)
    json_files = [pos_json for pos_json in os.listdir(dir) if pos_json.endswith('.json')]

    for json_file in json_files :
        path = dir + '/' + json_file
        with open(path) as file :
            data = json.load(file)
            if 'accessToken' in data:
                accessToken = data['accessToken']

    client = boto3.client('sso',region_name='us-west-2')
    r = client.list_accounts(accessToken=accessToken)
    if r.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        for account in r.get('accountList'):
            accountId = account.get('accountId')
            account_name = account.get('accountName')
            profile_name = account_map.get(account_name)[0]
            region = account_map.get(account_name)[1]
            r1 = client.list_account_roles(
                accessToken=accessToken,
                accountId=accountId)
            if r1.get('ResponseMetadata').get('HTTPStatusCode') == 200:
                n = 1
                for role in r1.get('roleList'):
                    role = role.get('roleName')
                    p_name = 'profile {}'.format(profile_name)
                    if not re.match('^[A-Z].*', role):
                        p_name = '{}{}'.format(p_name, role)
                    if n == 1 and config.has_section(p_name):
                        config.remove_section(p_name)
                    elif n > 1 and config.has_section(p_name):
                        p_name = '{}{}'.format(p_name, role)
                    config.add_section(p_name)
                    config.set(p_name, 'sso_start_url', 'https://hireteammate.awsapps.com/start')
                    config.set(p_name, 'sso_region', 'us-west-2')
                    config.set(p_name, 'sso_account_id', accountId)
                    config.set(p_name, 'sso_role_name', role)
                    config.set(p_name, 'region', region)
                    config.set(p_name, 'output', 'json')
                    n += 1
            else:
                print('auth error, please check your aws sso config file')
                return False
        _write_config(AWS_CONFIG_PATH, config)
    else:
        print('auth error, please check your aws sso config file')
        return False

def _spawn_cli_for_config():
    config = _read_config(AWS_CONFIG_PATH)

    if not config.has_section('default'):
        config.add_section('default')

    if os.getenv('AWS_PROFILE'):
        os_section = 'profile ' + os.getenv('AWS_PROFILE')
        try:
            config.add_section(os_section)
        except:
            pass

    for key, value in default_config.items():
        for section in config.sections():
            config.set(section, key, value)

    _write_config(AWS_CONFIG_PATH, config)
    p = subprocess.run(['aws', 'configure', 'sso'],
                   stdin=sys.stderr, stdout=sys.stdout, check=True)
    _gen_config_file()

def _spawn_cli_for_auth(profile):
    subprocess.run(['aws', 'sso', 'login', '--profile', str(profile).replace('profile ', '')],
                   stderr=sys.stderr,
                   stdout=sys.stdout,
                   check=True)

def _spawn_cli_for_logout(profile):
    subprocess.run(['aws', 'sso', 'logout', '--profile', str(profile).replace('profile ', '')],
                   stderr=sys.stderr,
                   stdout=sys.stdout,
                   check=True)


def _add_prefix(name):
    return f'profile {name}' if name != 'default' else 'default'


def _read_config(path):
    config = ConfigParser()
    config.read(path)
    return config


def _write_config(path, config):
    with open(path, 'w') as destination:
        config.write(destination)


def _load_json(path):
    try:
        with open(path) as context:
            return json.load(context)
    except ValueError:
        pass  # skip invalid json

def _ec2_search(keyword):
    ec2 = boto3.resource('ec2', region_name=CURRENT_REGION)
    filters = [{'Name':'tag:Name', 'Values': ['*{}*'.format(keyword)]}]
    instances = ec2.instances.filter(Filters=filters)
    i_list = []
    for i in instances:
        for tag in i.tags:
            if tag['Key'] == 'Name':
                instanceName = tag['Value']
                i_list.append('{} {:<35} {:<15} {}'.format(i.instance_id, instanceName, i.instance_type, i.private_ip_address))

    if len(i_list) == 0:
        print('Did not find any ec2 instances.')
        sys.exit()
    questions = [
        inquirer.List(
            'name',
            message='Please select EC2 to login',
            choices=i_list
        ),
    ]
    answer = inquirer.prompt(questions)
    instance_id = answer['name'].split(' ')[0]

    print('Will login instance:  {}'.format(answer['name']))
    os.system('aws ssm start-session --target {} --region {}'.format(instance_id, CURRENT_REGION))

def _ec2_login(keyword):
    if keyword.startswith('i-'):
        instance_id = keyword
    elif keyword.startswith('1'):
        ip = keyword
    else:
        ec2_name = keyword
    if 'ip' in locals() or 'ec2_name' in locals():
        ec2 = boto3.resource('ec2', region_name=CURRENT_REGION)
        if locals().get('ip'):
            filters = [{'Name':'private-ip-address', 'Values': [ip]}]
        if locals().get('ec2_name'):
            filters = [{'Name':'tag:Name', 'Values': [ec2_name]}]
        instances = ec2.instances.filter(Filters=filters)
        for i in instances:
            instance_id = i.instance_id
            break
    os.system('aws ssm start-session --target {} --region {}'.format(instance_id, CURRENT_REGION))

def _sm_search(keyword):
    client = boto3.client('secretsmanager', region_name=CURRENT_REGION)
    ret = client.list_secrets(MaxResults=100)
    _ret_list = ret['SecretList']
    _next = ret.get('NextToken')
    while _next:
        ret_tmp = client.list_secrets(MaxResults=100, NextToken=_next)
        _ret_list.extend(ret_tmp['SecretList'])
        _next = ret_tmp.get('NextToken')
    ret_list = []
    for i in _ret_list:
        if i['Name'].find(keyword) != -1:
            ret_list.append(i['Name'])

    if len(ret_list) == 0:
        print('Did not find any secrets manager.')
        sys.exit()
    questions = [
        inquirer.List(
            'name',
            message='Please select secrets manager',
            choices=ret_list
        ),
    ]
    answer = inquirer.prompt(questions)
    ret = client.get_secret_value(SecretId=answer['name'])
    print(ret['SecretString'])

def _sm_create():
    client = boto3.client('secretsmanager', region_name=CURRENT_REGION)
    sm_name = input('Please enter the secrets manager:\n')
    sm_value = input('Please enter the sm value:\n')
    try:
        jsonify_data = json.loads(sm_value)
    except:
        print('The data format is not json, update failed')
        sys.exit()

    ret = client.create_secret(Name=sm_name, SecretString=json.dumps(jsonify_data))
    print(ret)

def _sm_update(keyword):
    client = boto3.client('secretsmanager', region_name=CURRENT_REGION)
    ret = client.get_secret_value(SecretId=keyword)
    print('Current value is:\n{}'.format(ret['SecretString']))
    data = input('Please enter the new value:\n')
    try:
        jsonify_data = json.loads(data)
    except:
        print('The data format is not json, update failed')
        sys.exit()

    ret = client.update_secret(SecretId=keyword, SecretString=json.dumps(jsonify_data))
    print(ret)

def _sm_delete(keyword):
    client = boto3.client('secretsmanager', region_name=CURRENT_REGION)
    data = input('Please confirm this deletion[y/n]: ')
    if data.strip().lower() == 'y':
        print('The sm: {} will be deleted'.format(keyword))
        ret = client.delete_secret(
            SecretId=keyword,
            #RecoveryWindowInDays=7,
            ForceDeleteWithoutRecovery=True
        )
        print(ret)
    else:
        print('The sm: {} will not be deleted'.format(keyword))
        sys.exit()


if __name__ == "__main__":
    main()
