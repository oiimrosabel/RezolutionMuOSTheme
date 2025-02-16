import glob
import os
import shutil

import muos_rezolution.tools.display_tools as c


def deleteFile(path: str):
    if not os.path.exists(path):
        c.warning(f"{path} does not exist")
        return
    if not os.path.isfile(path):
        c.warning(f"{path} is not a file")
        return
    os.remove(path)
    c.success(f"Deleted file {path}")


def deleteFolder(path: str):
    if not os.path.exists(path):
        c.warning(f"{path} does not exist")
        return
    if not os.path.isdir(path):
        c.warning(f"{path} is not a directory")
    shutil.rmtree(path)
    c.success(f"Deleted folder {path}")


def deleteFilesInFolder(path: str):
    if not os.path.exists(path):
        c.warning(f"{path} does not exist")
        return
    for file in glob.glob(f"{path}/*"):
        if os.path.isfile(file):
            deleteFile(file)
        else:
            deleteFolder(file)


def readFile(filePath: str) -> str:
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            c.success(f"File {filePath} read successfully")
            return file.read()
    except FileNotFoundError:
        c.error(f"File not found : {filePath}")
        exit(os.EX_DATAERR)


def saveFile(filePath: str, content: str) -> None:
    try:
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(content)
            c.success(f"File {filePath} saved successfully")
    except FileNotFoundError:
        c.error(f"File not found : {filePath}")
        exit(os.EX_DATAERR)
    except IOError as e:
        c.error(f"Unable to edit '{filePath}': {e}")
        exit(os.EX_DATAERR)


def createFolder(path: str):
    if os.path.exists(path):
        c.warning(f"{path} already exists")
        return
    os.makedirs(path, exist_ok=True)
    c.success(f"Created folder '{path}'")
