# -*- coding: utf-8 -*-
from flask import g
from flask_principal import Permission, RoleNeed, ActionNeed, identity_loaded
# https://github.com/mickey06/Flask-principal-example/blob/master/FPrincipals.py


be_admin = RoleNeed("admin")
be_editor = RoleNeed("editor")
to_sign_in = ActionNeed("sign in")

user_permission = Permission(to_sign_in)
user_permission.description = "User Permissions"

editor_permission = Permission(be_editor)
editor_permission.description = "Editor Permissions"

admin_permission = Permission(be_admin)
admin_permission.description = "Admin Permissions"

apps_needs = [be_admin, be_editor, to_sign_in]
apps_permissions = [user_permission, editor_permission, admin_permission]

def current_privileges():
    return (("{method}: {value}").format(method=n.method, value=n.value)
            for n in apps_needs if n in g.identity.provides)
