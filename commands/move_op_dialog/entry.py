import adsk.core
import adsk.cam
import os
import traceback
from ...lib import fusionAddInUtils as futil
from ... import config

# =============================================================================
# GLOBAL VARIABLES
# =============================================================================
#region

# Get the active document
app = adsk.core.Application.get()
ui = app.userInterface

# List to store local event handlers
local_handlers = []

# Command configuration constants
CMD_UP_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_moveUp'
CMD_DOWN_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_moveDown'
CMD_UP_NAME = 'Move Operation Up'
CMD_DOWN_NAME = 'Move Operation Down'
CMD_DESCRIPTION = 'Moves selected CAM operation up/down in the operations list'
IS_PROMOTED = True

# Workspace and panel configuration
WORKSPACE_ID = 'CAMEnvironment'
PANEL_ID = 'MoveOpPanel'
PANEL_NAME = 'Move Operations'
POSITION_ID = 'CAMManagePanel'
COMMAND_BESIDE_ID = ''

# Path to the folder containing command icons
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), './resources', '')

#endregion

# =============================================================================
# EVENT HANDLERS
# =============================================================================
#region

def start():
    """Initialize the add-in."""
    try:
        # Create command definitions if they don't exist
        cmd_defs = [
            (CMD_UP_ID, CMD_UP_NAME, os.path.join(ICON_FOLDER, 'move_up_button')),
            (CMD_DOWN_ID, CMD_DOWN_NAME, os.path.join(ICON_FOLDER, 'move_down_button'))
        ]

        for cmd_id, cmd_name, icon_folder in cmd_defs:
            cmd_def = ui.commandDefinitions.itemById(cmd_id)
            if not cmd_def:
                cmd_def = ui.commandDefinitions.addButtonDefinition(
                    cmd_id, 
                    cmd_name, 
                    CMD_DESCRIPTION, 
                    icon_folder
                )
                if cmd_id == CMD_UP_ID:
                    futil.add_handler(cmd_def.commandCreated, move_up_command_created)
                else:
                    futil.add_handler(cmd_def.commandCreated, move_down_command_created)

        # Retrieve workspace and panel, create if not found
        workspace = ui.workspaces.itemById(WORKSPACE_ID)
        if workspace is None:
            ui.messageBox(f"Workspace '{WORKSPACE_ID}' not found.")
            return
        futil.log(f"Workspace '{WORKSPACE_ID}' found")

        panel = workspace.toolbarPanels.itemById(PANEL_ID)
        if not panel:
            panel = workspace.toolbarPanels.add(PANEL_ID, PANEL_NAME, POSITION_ID, False)
            futil.log(f"Created new panel '{PANEL_NAME}' in workspace")

        # Clear existing controls to avoid duplicates
        while panel.controls.count > 0:
            panel.controls.item(0).deleteMe()

        # Add commands to UI panel
        for cmd_id in [CMD_UP_ID, CMD_DOWN_ID]:
            cmd_def = ui.commandDefinitions.itemById(cmd_id)
            if cmd_def:
                panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False).isPromoted = IS_PROMOTED
        futil.log(f"Added command controls to panel with promotion = {IS_PROMOTED}")

    except:
        ui.messageBox('Failed during start:\n{}'.format(traceback.format_exc()))

def stop():
    """Remove the command and UI elements from Fusion 360"""
    try:
        workspace = ui.workspaces.itemById(WORKSPACE_ID)
        if not workspace:
            futil.log(f"Workspace '{WORKSPACE_ID}' not found")
            return

        panel = workspace.toolbarPanels.itemById(PANEL_ID)
        if panel:
            # Remove all controls from the panel
            while panel.controls.count > 0:
                panel.controls.item(0).deleteMe()
            # Remove the panel itself
            panel.deleteMe()
            futil.log(f"Panel '{PANEL_ID}' removed")

        # Remove command definitions
        for cmd_id in [CMD_UP_ID, CMD_DOWN_ID]:
            cmd_def = ui.commandDefinitions.itemById(cmd_id)
            if cmd_def:
                cmd_def.deleteMe()
                futil.log(f"Command definition '{cmd_id}' removed")

    except:
        ui.messageBox('Failed during stop:\n{}'.format(traceback.format_exc()))

def move_up_command_created(args: adsk.core.CommandCreatedEventArgs):
    """Handle command created event for moving operations up."""

    futil.log(f'{CMD_UP_NAME} Command Created Event')
    futil.add_handler(args.command.execute, move_up_execute, local_handlers=local_handlers)

def move_down_command_created(args: adsk.core.CommandCreatedEventArgs):
    """Handle command created event for moving operations down."""

    futil.log(f'{CMD_DOWN_NAME} Command Created Event')
    futil.add_handler(args.command.execute, move_down_execute, local_handlers=local_handlers)

def move_up_execute(args: adsk.core.CommandEventArgs):
    """Handle command execute event for moving operations up."""
    
    futil.log(f'{CMD_UP_NAME} Command Execute Event')
    try:

        if not check_cam_setups():
            ui.messageBox("No CAM setups found in the current document.")
            return

        selected_entities = ui.activeSelections
        
        if selected_entities.count == 0:
            ui.messageBox("Please select at least one operation.")
            return

        operations = [sel.entity for sel in selected_entities if isinstance(sel.entity, adsk.cam.Operation)]
        if not operations:
            ui.messageBox("Please select only operations.")
            return

        operations.sort(key=lambda op: get_operation_index(op))
        
        for operation in operations:
            parent = operation.parent
            index = get_operation_index(operation)
            if index > 0:
                operation.moveBefore(parent.operations.item(index - 1))

    except:
        ui.messageBox('Failed during execution:\n{}'.format(traceback.format_exc()))

def move_down_execute(args: adsk.core.CommandEventArgs):
    """Handle command execute event for moving operations down."""

    futil.log(f'{CMD_DOWN_NAME} Command Execute Event')
    try:

        if not check_cam_setups():
            ui.messageBox("No CAM setups found in the current document.")
            return

        selected_entities = ui.activeSelections
        
        if selected_entities.count == 0:
            ui.messageBox("Please select at least one operation.")
            return

        operations = [sel.entity for sel in selected_entities if isinstance(sel.entity, adsk.cam.Operation)]
        if not operations:
            ui.messageBox("Please select only operations.")
            return

        operations.sort(key=lambda op: get_operation_index(op), reverse=True)
        
        for operation in operations:
            parent = operation.parent
            index = get_operation_index(operation)
            if index < parent.operations.count - 1:
                operation.moveAfter(parent.operations.item(index + 1))

    except:
        ui.messageBox('Failed during execution:\n{}'.format(traceback.format_exc()))

def command_destroy(args: adsk.core.CommandEventArgs):
    """Handle command destroy event."""
    
    futil.log(f"Command '{args.command.id}' Destroy Event")
    
    global local_handlers
    local_handlers = []

#endregion
# =============================================================================

# =============================================================================
# OTHER FUNCTIONS
# =============================================================================

#region

def get_operation_index(operation):
    """Get the index of the operation in its parent operations list."""
    parent = operation.parent
    for i in range(parent.operations.count):
        if parent.operations.item(i) == operation:
            return i
    return -1

def check_cam_setups():
    
    # Get the active document
    doc = app.activeDocument
    
    # Get the CAM product
    product = doc.products.itemByProductType('CAMProductType')
    cam = adsk.cam.CAM.cast(product)

    # Check if the CAM product exists and if there are setups
    if not cam or cam.setups.count == 0:
        ui.messageBox("No setups found in the current document.")
        return False
    
    return True

# =============================================================================

#endregion