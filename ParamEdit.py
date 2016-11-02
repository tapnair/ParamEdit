#Author-Patrick Rainsberry
#Description-Creates a GUI for all User Parameters

# Script to update all user parameters in a model
# Any variables will be loaded into the UI form with current value
# New values are validated before applying to the model. 

import adsk.core, adsk.fusion, traceback
from . import Fusion360CommandBase

commandName1 = 'ParamEdit'
commandDescription1 = 'Enables you to edit all User Parameters'
commandResources1 = './resources'
cmdId1 = 'ParamEditCmd'
myWorkspace1 = 'FusionSolidEnvironment'
myToolbarPanelID1 = 'SolidModifyPanel'

debug = False

def updateParams(inputs):
    
    # Get Fusion Objects
    app = adsk.core.Application.get()
    ui  = app.userInterface
    design = app.activeProduct
    unitsMgr = design.unitsManager
    
    if inputs.count < 1:
        ui.messageBox('No User Parameters in the model')
        return          
    
    # Set all parameter values based on the input form                            
    for param in design.userParameters:
        inputExpresion = inputs.itemById(param.name).value
        
        # Use Fusion Units Manager to validate user expresion                        
        if unitsMgr.isValidExpression(inputExpresion, unitsMgr.defaultLengthUnits):
            
            # Set parameter value from input form                         
            param.expression = inputExpresion
        
        else:
            ui.messageBox("The following expresion was invalid: \n" +
                            param.name + '\n' +
                            inputExpresion)

class ParamEditCommand(Fusion360CommandBase.Fusion360CommandBase):
    def onPreview(self, command, inputs):
        updateParams(inputs)
    
    def onDestroy(self, command, inputs, reason_):    
        pass
    
    def onInputChanged(self, command, inputs, changedInput):
        pass
    
    def onExecute(self, command, inputs):
        updateParams(inputs)
    
    def onCreate(self, command, inputs):
        app = adsk.core.Application.get()
        design = app.activeProduct
        for param in design.userParameters:                                         
            #if param.name[0] != '_':
            inputs.addStringValueInput(param.name,
                                       param.name,
                                       param.expression)

##### Runtime Add 1 entry for each command#######
newCommand1 = ParamEditCommand(commandName1, commandDescription1, commandResources1, cmdId1, myWorkspace1, myToolbarPanelID1, debug)

def run(context):
    newCommand1.onRun()
def stop(context):
    newCommand1.onStop()