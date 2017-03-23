__author__ = 'rainsbp'

import adsk.core
import adsk.fusion
import traceback

from .Fusion360Utilities.Fusion360Utilities import get_app_objects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase


def update_params(inputs):
    # Gets necessary application objects from utility function
    app_objects = get_app_objects()
    design = app_objects['design']
    units_manager = app_objects['units_manager']

    if inputs.count < 1:
        app_objects['ui'].messageBox('No User Parameters in the model')
        return

    # Set all parameter values based on the input form
    for param in design.userParameters:
        input_expression = inputs.itemById(param.name).value

        # Use Fusion Units Manager to validate user expression
        if units_manager.isValidExpression(input_expression, units_manager.defaultLengthUnits):

            # Set parameter value from input form
            param.expression = input_expression

        else:
            app_objects['ui'].messageBox("The following expression was invalid: \n" +
                                         param.name + '\n' +
                                         input_expression)


class ParamEditCommand(Fusion360CommandBase):
    def on_preview(self, command, inputs, args, input_values):
        update_params(inputs)

    def on_execute(self, command, inputs, args, input_values):
        update_params(inputs)

    def on_create(self, command, inputs):
        # Gets necessary application objects from utility function
        app_objects = get_app_objects()
        design = app_objects['design']

        for param in design.userParameters:
            inputs.addStringValueInput(param.name,
                                       param.name,
                                       param.expression)
