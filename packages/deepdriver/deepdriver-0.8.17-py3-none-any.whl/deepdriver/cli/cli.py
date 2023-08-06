import argparse
import os

import deepdriver
import click
import re
import configparser
import pipes
import pickle

base_dir = os.getcwd()
config_base_dir = os.path.join(base_dir, "deepdriver", "settings")
config_file = os.path.join(config_base_dir, "config.ini")
properties = configparser.ConfigParser()
properties.optionxform = str  # for uppercase
properties.read(config_file)


@click.group()
@click.pass_context
def cli(ctx):
    os.makedirs(os.path.dirname(config_file), exist_ok=True)  # config.ini 파일이 없으면 생성


@click.command('setting', short_help='Initialize the Deepdriver Host Setting')
@click.option('--http_host', help='REST API Server URI', )
@click.option('--grpc_host', help='GRPC Server URI', )
def setting(http_host, grpc_host):
    click.echo('Initializing the Deepdriver Host Setting')

    if os.path.exists(config_file) and properties.has_option("DEFAULT", "HTTP_HOST"):
        click.echo(click.style('Deepdriver Setting file already exists', fg='red'))
        click.confirm('Do you want to overwrite?', abort=True)

    if http_host is None:
        http_host = click.prompt(
            f"Please HTTP API Server URI",
            default="15.164.104.132:9011"
        )

    if grpc_host is None:
        grpc_host = click.prompt(
            f"Please enter GRPC Server URI",
            default="15.164.104.132:19051"
        )

    default = properties["DEFAULT"]
    default["HTTP_HOST"] = http_host
    default["GRPC_HOST"] = grpc_host

    with open(config_file, "w") as f:
        properties.write(f)


@click.command('login', short_help='Login to The Deepdriver')
@click.option('--key', help='Login Key')
@click.option('--jwt_token', envvar="DEEPDRIVER_JWT_TOKEN")
@click.pass_context
def login(ctx, key, jwt_token):
    if not os.path.exists(config_file) or not properties.has_option("DEFAULT", "HTTP_HOST"):
        click.echo(click.style("Deepdriver Setting not exists. Set Deepdriver HTTP server and GRPC Server", fg='red'))
        ctx.invoke(setting)

    if properties.has_option("USER", "KEY"):
        click.echo(click.style('Deepdriver login token already exists', fg='red'))
        click.confirm('Do you want to overwrite?', abort=True)

    default_prop = properties["DEFAULT"]
    deepdriver.setting(default_prop['HTTP_HOST'], default_prop['GRPC_HOST'])

    if key is None:
        key = click.prompt(
            f"Please enter Login Key",
            show_default=False,
        )

    try:
        login_result, jwt_key = deepdriver.login(key=key)
    except Exception as e:
        click.echo(click.style(f"Login Failed : {str(e)}", fg='red'))
        return

    if login_result:
        click.echo(click.style("Login Success", fg='green'))

        if not properties.has_section("USER"):
            properties.add_section("USER")
        user_prop = properties["USER"]
        user_prop["KEY"] = key
        user_prop["TOKEN"] = jwt_key

    with open(config_file, "w") as f:
        properties.write(f)


def check_exp_name(exp_name):
    # raise click.BadParameter("Couldn't understand date.", param=exp_name)
    pattern = re.compile('[^a-zA-Z0-9._]+')
    if pattern.findall(exp_name):
        raise click.BadParameter("Experiment Name은 숫자(number), 영문자(alphabet), 언더바(_), 온점(.)만 가능합니다.",
                                 param=exp_name)
        return None
    if len(exp_name) >= 50:
        raise click.BadParameter("Experiment Name의 최대 길이는 50자 미만입니다. [max length 50]", param=exp_name)
        return None
    return exp_name


@click.command('init', short_help='Initialize the Deepdriver Experiment')
@click.option('--exp_name', help='Experiment Name')
@click.option('--team_name', help='Team Name')
@click.pass_context
def init(ctx, exp_name, team_name):
    if not os.path.exists(config_file) or not properties.has_option("DEFAULT", "HTTP_HOST"):
        click.echo(click.style("Deepdriver Setting not exists. Set Deepdriver HTTP server and GRPC Server", fg='red'))
        ctx.invoke(setting)

    # login check
    if not properties.has_section("USER"):
        click.echo(click.style("Deepdriver Login first", fg='red'))
        ctx.invoke(login)
        properties.read(config_file)
        if not properties.has_section("USER"):
            click.echo(click.style("Deepdriver Login Failed", fg='red'))
            return

    if exp_name is None:
        exp_name = click.prompt(
            f"Please enter Experiment Name",
            show_default=False,
            value_proc=check_exp_name
        )
    if team_name is None:
        team_name = click.prompt(
            f"Please enter Team Name",
            default="",
            show_default=True,
        )

    deepdriver.setting(http_host=properties["DEFAULT"]["HTTP_HOST"], grpc_host=properties["DEFAULT"]["GRPC_HOST"])
    deepdriver.login(key=properties["USER"]["KEY"])
    run = deepdriver.init(exp_name=exp_name, team_name="")
    with open('run.pickle', 'wb') as f:  # run 객체를 dump함
        pickle.dump(run, f)


@click.command('artifact', short_help='Upload or Download the Deepdriver Artifact')
@click.argument('command', type=click.Choice(['upload', 'download'], case_sensitive=False))
# @click.argument('path', help="path")
@click.option('--type', help='Type of artifact', prompt="Select type f Artifact",
              type=click.Choice(['model', 'dataset', 'code']), required=True)
@click.option('--name', help='Name of artifact', prompt="Input the name of Artifact", required=True)
@click.option('--tag', help='Tag of artifact', required=False)
@click.argument('path', type=click.Path(exists=True, file_okay=False, resolve_path=True), required=True)
@click.pass_context
def artifact(ctx, command, type, name, tag, path):
    if command == 'upload':
        click.echo('upload')
        deepdriver.setting(http_host=properties["DEFAULT"]["HTTP_HOST"],
                           grpc_host=properties["DEFAULT"]["GRPC_HOST"])
        deepdriver.login(key=properties["USER"]["KEY"])

        with open('run.pickle', 'rb') as f:
            run = pickle.load(f)
            from deepdriver.sdk.data_types.run import set_run, Run, get_run
            set_run(run)

            arti = deepdriver.get_artifact(**{"type": type, "name": name, "tag": tag})
            print(f"artfact info : {arti.__dict__}")
            arti.add(path)

            deepdriver.upload_artifact(arti)


    elif command == 'download':
        click.echo('upload')
        deepdriver.setting(http_host=properties["DEFAULT"]["HTTP_HOST"],
                           grpc_host=properties["DEFAULT"]["GRPC_HOST"])
        deepdriver.login(key=properties["USER"]["KEY"])
        with open('run.pickle', 'rb') as f:
            run = pickle.load(f)
            from deepdriver.sdk.data_types.run import set_run, Run, get_run
            set_run(run)
            arti = deepdriver.get_artifact(**{"type": type, "name": name, "tag": tag})
            arti.download(path)
            click.echo('download')


cli.add_command(setting)
cli.add_command(login)
cli.add_command(init)
cli.add_command(artifact)

if __name__ == "__main__":
    cli()
