from .move_op_dialog import entry as commandDialog

commands = [
    commandDialog
]

def start():
    for command in commands:
        command.start()


def stop():
    for command in commands:
        command.stop()