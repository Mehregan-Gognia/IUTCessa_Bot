from core.StateLevels import KMKYAR_MENUS, TECH_STACK_USER_PANEL, TECH_STACK_ADMIN_PANEL
from kmkyar import Menus as kmkyar_menus
from techstack import UserMenus as techstack_user_menus
from techstack import AdminMenus as techstack_admin_menus

async def dispatch(update, context, state):
    if state in KMKYAR_MENUS:
        await kmkyar_menus.handle_message(update, context, state)
        return True
    elif state in TECH_STACK_USER_PANEL:
        await techstack_user_menus.handle_message(update, context, state)
        return True
    elif state in TECH_STACK_ADMIN_PANEL:
        await techstack_admin_menus.handle_message(update, context, state)
        return True
    elif state != "main-menu":
        print(f"Unknown State Reached! {state}")
    return False
    