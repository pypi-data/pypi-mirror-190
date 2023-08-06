# coding: utf-8

import click

import src.commands.init as cmd_init
from src.commands import feature_init, app_init
from src.definitions.platform import Platform
from src.models.project import Project


@click.group()
@click.pass_context
def cli(ctx):
    """ark - Command line tool to manage ark mobile app"""
    ctx.obj = Project()


@cli.command()
@click.pass_obj
@click.option('--name',
              prompt='name of your mobile app',
              default='my-app',
              required=True,
              help='Name of your mobile app')
@click.option('--platform',
              prompt='{0}/{1}'.format(Platform.ANDROID, Platform.IOS),
              default=Platform.ANDROID,
              type=click.Choice([Platform.ANDROID, Platform.IOS]),
              required=True,
              help='Select a platform')
@click.option('--package',
              prompt='package name / app identifier',
              default='com.example.myapp',
              required=True,
              help='PackageName / App identifier')
def init(
        project: Project,
        name: str,
        platform: str,
        package: str):
    cmd_init.init(name, platform, package)


@cli.command()
@click.pass_obj
@click.option('--app_name',
              prompt='name of your app',
              default='myapp',
              required=True,
              help='Name of your app')
@click.option('--package_name',
              prompt='package name / app identifier',
              default='com.example.myapp',
              required=True,
              help='PackageName / App identifier')
@click.option('--platform',
              prompt='{0}/{1}'.format(Platform.ANDROID, Platform.IOS),
              default=Platform.ANDROID,
              type=click.Choice([Platform.ANDROID, Platform.IOS]),
              required=True,
              help='Select a platform')
def init_app(
        project: Project,
        app_name: str,
        package_name: str,
        platform: str):
    app_init.init_app(app_name, package_name, platform)


@cli.command()
@click.pass_obj
@click.option('--app_name',
              prompt='name of your app',
              default='myapp',
              required=True,
              help='Name of your app')
@click.option('--feature_name',
              prompt='name of your feature',
              default='home',
              required=True,
              help='Name of your feature')
@click.option('--package_name',
              prompt='package name / app identifier',
              default='com.example.myapp',
              required=True,
              help='PackageName / App identifier')
@click.option('--platform',
              prompt='{0}/{1}'.format(Platform.ANDROID, Platform.IOS),
              default=Platform.ANDROID,
              type=click.Choice([Platform.ANDROID, Platform.IOS]),
              required=True,
              help='Select a platform')
def init_feature(
        project: Project,
        app_name: str,
        feature_name: str,
        package_name: str,
        platform: str):
    feature_init.init_feature(app_name, feature_name, package_name, platform)


cli.add_command(init)
cli.add_command(init_app)
cli.add_command(init_feature)
