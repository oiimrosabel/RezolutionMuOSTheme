import os
import shutil
import sys

import muos_rezolution.tools.display_tools as c
import muos_rezolution.tools.files_tools as d
import muos_rezolution.tools.mustache_tools as m


def mergeFolders(srcPath: str, destPath):
    if not os.path.exists(destPath):
        os.makedirs(destPath)

    for root, _, files in os.walk(srcPath):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(destPath, os.path.relpath(src_file, srcPath))

            if not os.path.exists(dst_file):
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
            else:
                c.warning(f"File {dst_file} already exists")
    c.success(f"Merged {srcPath} to {destPath}")


def generateSchemes(templatePath: str, dataPath: str, outputPath: str):
    templateStr = d.readFile(templatePath)
    dataDict = m.interpretAsJson(d.readFile(dataPath))
    output = m.replaceMustaches(templateStr, dataDict)
    d.saveFile(outputPath, output)
    c.success(f"Scheme generated in {outputPath}")


def cookTheme(interPath: str, srcPath: str, commonPath: str):
    if not os.path.exists(interPath):
        c.error(f"Invalid intermediate path : {interPath}")
        sys.exit(1)
    if not os.path.exists(srcPath):
        c.error(f"Invalid source path : {srcPath}")
        sys.exit(1)
    if not os.path.exists(commonPath):
        c.error(f"Invalid common path : {commonPath}")
        sys.exit(1)
    mergeFolders(commonPath, interPath)
    mergeFolders(srcPath, interPath)
    c.success(f"Theme cooked in {interPath}")


def zipFolder(srcPath: str, destPath: str):
    if not os.path.exists(srcPath):
        c.error(f"Invalid path : {srcPath}")
        sys.exit(1)
    if destPath.endswith(".zip"):
        destPath = destPath[:-len(".zip")]

    currentDir = os.getcwd()
    absDestPath = os.path.abspath(destPath)
    os.chdir(srcPath)
    shutil.make_archive(absDestPath, "zip", root_dir=".", base_dir=".")
    os.chdir(currentDir)

    c.success(f"Archived {srcPath} into {destPath}.zip")
