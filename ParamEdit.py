# Author-Patrick Rainsberry
# Description-Creates a GUI for all User Parameters

# Script to update all user parameters in a model
# Any variables will be loaded into the UI form with current value
# New values are validated before applying to the model. 

# Importing sample Fusion Command
# Could import multiple Command definitions here
from .ParamEditCommand import ParamEditCommand

commands = []
command_definitions = []

# Define parameters for vent maker command
cmd = {
    'cmd_name': 'ParamEdit',
    'cmd_description': 'Enables you to edit all User Parameters',
    'cmd_resources': './resources',
    'cmd_id': 'cmdID_ParamEdit',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'SolidModifyPanel',
    'class': ParamEditCommand
}
command_definitions.append(cmd)

# Set to True to display various useful messages when debugging your app
debug = False

# Don't change anything below here:
for cmd_def in command_definitions:
    command = cmd_def['class'](cmd_def, debug)
    commands.append(command)


def run(context):
    for run_command in commands:
        run_command.on_run()


def stop(context):
    for stop_command in commands:
        stop_command.on_stop()
