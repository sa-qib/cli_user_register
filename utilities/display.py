from time import sleep
import os

class Display:
    main_menu = (["1. Add Task, 4. Logout"],)
    menu_table = (["1. Add, 2. Remove, 3.Edit, 4. Logout"],)
    edit_menu = (["0. Menu, 1. Mark, 2. logout"],)

    @classmethod
    def flash_msg(cls, msg):
            print(cls.color("red", msg), end='', flush=True)
            sleep(1)
            print('\r', ' ' * len(msg), '\r', end='', flush=True)

    @classmethod
    def clear_screen(cls):
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")


    @classmethod
    def color(cls, clr, prompt):
        """
        Add color using the ASNI escape.

        Args:
            prompt (clr): selecting color [red, green,
                        yellow, blue, megenta, cyan, white].
            prompt (prompt): prompt msg you want apply color.
        """

        if prompt == "Task removed successfully.":
            return f"\u001b[32m {prompt} \u001b[0m"

        match clr:
            case "red":
                return f"\u001b[31m {prompt} \u001b[0m"
            case "green":
                return f"\u001b[32m {prompt} \u001b[0m"
            case "yellow":
                return f"\u001b[33m {prompt} \u001b[0m"
            case "blue":
                return f"\u001b[34m {prompt} \u001b[0m"
            case "megenta":
                return f"\u001b[35m {prompt} \u001b[0m"
            case "cyan":
                return f"\u001b[36m {prompt} \u001b[0m"
            case "white":
                return f"\u001b[37m {prompt} \u001b[0m"