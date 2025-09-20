import os
from dotenv import load_dotenv
from typing import List
import casbin
from casbin_sqlalchemy_adapter import Adapter
from sqlalchemy import Tuple
from hackathon_backend.casbin import policies

load_dotenv()
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_SERVER = os.environ["POSTGRES_SERVER"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


def init_policies():

    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, "rbac_model.conf")

    adapter = Adapter(DATABASE_URL)
    e = casbin.Enforcer(model_path, adapter)
    e.load_policy()

    # Polities example
    base_policies: List[Tuple[str, str, str]] = policies.policies

    # Convert the current policies to tuples
    current_policies = set(tuple(p) for p in e.get_policy())
    base_set = set(base_policies)

    to_add = base_set - current_policies
    to_remove = current_policies - base_set

    # Policies to remove
    for policy in to_remove:
        e.remove_policy(*policy)
        print(f"Política eliminada: {policy}")

    # Policies to add
    added_count = 0
    for policy in to_add:
        e.add_policy(*policy)
        added_count += 1
        print(f"Política agregada: {policy}")

    if added_count > 0 or (to_remove):
        print(f"Se agregaron {added_count} políticas nuevas")
    else:
        print("Todas las políticas ya existen, no se realizaron cambios")


if __name__ == "__main__":
    init_policies()
