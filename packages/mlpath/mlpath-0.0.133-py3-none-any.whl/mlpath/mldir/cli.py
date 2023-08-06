'''
This is the CLI for the mlpath package. Includes commands to create a new project
'''

import zipfile
import click
import os
import pkg_resources


@click.command()
def main():
    click.echo('Project creation in progress')
    if True:
        #try:
            #print the current working directory
            click.echo('Current working directory is: ' + os.getcwd())
            # view the contents of the current directory
            click.echo('Contents of current directory are: ' + str(os.listdir()))
            zip_path = pkg_resources.resource_filename(__name__, "/Project.zip")
            with zipfile.ZipFile(zip_path,"r") as zip_ref:
                
                zip_ref.extractall("Project")
            click.echo('Project created successfully')
        #except:
        #    click.echo('Project creation failed')

