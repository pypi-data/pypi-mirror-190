import importlib.util
import os
from typing import Union

from opensearchpy import OpenSearch


def dynamically_import_migrations() -> Union[
    tuple[OpenSearch, OpenSearch, str], tuple[None, None]
]:
    """
    Dynamically imports the necessary migration files and returns the 'source_client' from the 'env.py' file.
    """
    try:
        # Obtain the file's path
        current_working_dir = os.getcwd()
        migrations_dir = os.path.join(current_working_dir, "migrations")
        file_path = os.path.join(migrations_dir, "env.py")
        init_file_path = os.path.join(migrations_dir, "__init__.py")

        # Create a ModuleSpec object
        spec = importlib.util.spec_from_file_location("env", file_path)
        init_spec = importlib.util.spec_from_file_location("init", init_file_path)

        # Load the module
        env = importlib.util.module_from_spec(spec)
        init = importlib.util.module_from_spec(init_spec)

        spec.loader.exec_module(env)
        init_spec.loader.exec_module(init)

        return env.source_client, env.destination_client, env.VERSION_CONTROL_INDEX
    except FileNotFoundError:
        pass
    return None, None
