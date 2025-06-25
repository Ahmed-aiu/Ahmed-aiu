import os
import logging

# Configure logging to display messages in the console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get(file: str) -> tuple[str, str, str]:
    """
    Retrieve paths to the template and static folders, and generate a static URL path
    relative to a 'flask' directory in the project's structure.

    This function computes paths to the `template` and `static` folders based on
    the directory structure of the provided `file` path. It assumes a project
    structure where the `flask` folder is a significant directory marker for 
    relative path determination. The resulting paths are typically used in Flask
    applications to configure static and template folders.

    Args:
        file (str): The absolute path to a file within the project, used as a 
                    base for determining folder locations.

    Returns:
        tuple[str, str, str]: A tuple containing:
            - template_folder (str): Path to the `html` template folder.
            - static_folder (str): Path to the `js` static folder.
            - static_url_path (str): Relative URL path to the `static` folder for use in web routing.
    """
    basedir = os.path.abspath(os.path.dirname(file))
    # logging.debug(f"Basedir: {basedir}")

    parent_dir = os.path.dirname(basedir)
    static_folder = os.path.join(parent_dir, 'js')
    # logging.debug(f"static_folder: {static_folder}")

    template_folder = os.path.join(parent_dir, 'html')
    # logging.debug(f"template_folder: {template_folder}")

    # Split basedir into components using os.path methods
    path_components = os.path.normpath(basedir).split(os.sep)
    # logging.debug(f"path_components: {path_components}")

    flask_index = -4
    # Get the components after 'flask'
    rel_components = path_components[flask_index+1:]
    project_relative_path = '/' + '/'.join(rel_components)
    static_url_path = '/' + path_components[-4] + project_relative_path + '/js'
    # logging.debug(f"static_url_path: {static_url_path}")

    return template_folder, static_folder, static_url_path
