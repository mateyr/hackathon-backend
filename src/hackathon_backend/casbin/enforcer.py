import os
import casbin
from casbin_sqlalchemy_adapter import Adapter
from fastapi import HTTPException
from .init_policies import DATABASE_URL
from .policies import policies


expanded_policies = [
    (role, endpoint, method)
    for role, endpoint, methods in policies
    for method in (methods if isinstance(methods, list) else [methods])
]

def get_enforcer() -> casbin.Enforcer:
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, "rbac_model.conf")
    adapter = Adapter(DATABASE_URL)
    e = casbin.Enforcer(model_path, adapter)
    e.load_policy()
    return e


enforcer = get_enforcer()


# Validate permission
def check_permission(user_role: str, path: str, method: str):
    if not enforcer.enforce(user_role, path, method):
        raise HTTPException(
            status_code=403, detail="You do not have permission to perform this action"
        )
