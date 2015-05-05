#Author-Patrick Rainsberry
#Description-Creates a GUI for all User Parameters

import adsk.core, adsk.fusion, traceback

# global event handlers referenced for the duration of the command
handlers = []

commandName = 'CHange Parameters'
commandDescription = 'Enables you to edit all User Parameters'
command_id= 'ParamEditCmd'
control_id = 'ParamEditControl'
menu_panel = 'SolidModifyPanel'
commandResources = './resources'

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        class CommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:  
                    # Get values from input form
                    cmd = args.firingEvent.sender
                    inputs = cmd.commandInputs
                    if inputs.count < 1:
                    	app.userInterface.messageBox('No User Parameters in the model')
                    	return 
                     
                    # Get Fusion Objects
                    design = app.activeProduct
                    unitsMgr = design.unitsManager
                    
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
                except:
                    if ui:
                        ui.messageBox('command executed failed:\n{}'
                        .format(traceback.format_exc()))

        class CommandCreatedEventHandlerPanel(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    # Setup Handlers for change and execute
                    cmd = args.command
                    onExecute = CommandExecuteHandler()
                    cmd.execute.add(onExecute)
                    
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)
                    
                    # Define UI Elements
                    commandInputs_ = cmd.commandInputs                
                  
                    # Add all parameters to the input form
                    design = app.activeProduct
                    for param in design.userParameters:                                         
                        commandInputs_.addStringValueInput(param.name,
                                                           param.name,
                                                           param.expression)                
                except:
                    if ui:
                        ui.messageBox('Panel command created failed:\n{}'
                        .format(traceback.format_exc()))
                                       
        # Get the UserInterface object and the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions
         
        # Create a basic button command definition.
        buttonDef = cmdDefs.addButtonDefinition(command_id, 
                                                commandName, 
                                                commandDescription, 
                                                commandResources)                                               
        # Setup Event Handler
        onCommandCreated = CommandCreatedEventHandlerPanel()
        buttonDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # Add the controls to the Inspect toolbar panel.
        inspectPanel = ui.toolbarPanels.itemById(menu_panel)
        buttonControl = inspectPanel.controls.addCommand(buttonDef, control_id)
        buttonControl.isVisible = True

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        commandDef = ui.commandDefinitions.itemById(command_id)
        commandDef.deleteMe()

        panel = ui.toolbarPanels.itemById(menu_panel)
        control = panel.controls.itemById(control_id)
        control.deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
