# coding: utf-8

import os
import shutil
from functools import partial

import click
from binaryornot.check import is_binary

from src.definitions.ark_definitions import ArkDefinitions
from src.definitions.platform import Platform
from src.utils.file import (
    find_files_recursively,
    read_text_file,
    write_text_file,
    walk_dirs,
)
from src.utils.git import git_clone, git_cleanup


def init_app(app_name: str, package_name: str, platform: str):
    current_dir = os.getcwd()

    # list folders of current_directory
    dirs = list(filter(
        lambda x: os.path.isdir(x), os.listdir(current_dir)))

    target_dir_name = app_name.title()

    # check folder exists
    if target_dir_name in dirs:
        click.echo('Error: Directory name "{0}" already exists!'.format(target_dir_name))
        exit(-1)

    project_dir = f'{current_dir}{Platform.PATH_SEP}{target_dir_name}'

    # download the latest ark project from branch 'main'
    git_clone(
        ArkDefinitions.REPO_ANDROID_APP_TEMPLATE,
        project_dir,
        'main')

    # clear .git, .github
    git_cleanup(project_dir)

    # different process on each platform
    if platform == Platform.ANDROID:
        __process_android_app(project_dir, app_name, package_name)
    else:
        __process_ios_feature()


def __process_android_app(
        project_dir: str,
        app_name: str,
        package_name: str
):
    # walk all text file and replace package
    find_files_recursively(
        project_dir,
        partial(__on_walk_android_app_project_file,
                app_name=app_name,
                package_name=package_name)
    )

    # walk all dirs end with ark package
    walk_dirs(
        project_dir,
        partial(__on_walk_android_app_project_dir, package_name=package_name)
    )

    click.echo('Project generated at: {0}'.format(project_dir))
    click.echo('\nDone!')


def __process_ios_feature():
    return None


def __on_walk_android_app_project_file(
        file_name: str,
        app_name: str,
        package_name: str
):
    if not is_binary(file_name):
        text = read_text_file(file_name)
        text = text.replace(ArkDefinitions.ANDROID_APP_NAME, app_name.title()). \
            replace(ArkDefinitions.ANDROID_PACKAGE_NAME, package_name)
        write_text_file(file_name, text)

        return True


def __on_walk_android_app_project_dir(dir_name: str, package_name: str):
    new_dir_name = dir_name

    if ArkDefinitions.ANDROID_PACKAGE_NAME in new_dir_name:
        new_dir_name = new_dir_name.replace(ArkDefinitions.ANDROID_PACKAGE_NAME,
                                            package_name.replace('.', Platform.PATH_SEP))

    if new_dir_name != dir_name:
        shutil.copytree(dir_name, new_dir_name)
        shutil.rmtree(dir_name)
        return new_dir_name

    return None
