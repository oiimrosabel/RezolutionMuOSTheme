#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path

import muos_rezolution.tools.display_tools as c
import muos_rezolution.tools.files_tools as d
import muos_rezolution.tools.generate_tools as g

# Paths
root = Path(__file__).parent / "resources"
iconsFolder = root / "__icons"
buildFolder = Path("build")
factoryFolder = root / "__factory"
interFolder = buildFolder / "__intermediate"
commonFolder = root / "__common"


def generateMacro(themeName: str, gridSupport=False):
    gridNameSupplement = "Grid" if gridSupport else ""
    d.createFolder(interFolder)
    c.task(f"Generating schemes for {themeName} version...")
    g.cookTheme(interFolder, root / f"variants/{themeName}", commonFolder)
    d.createFolder(interFolder / "scheme")
    g.generateSchemes(factoryFolder / "template/default.txt",
                      factoryFolder / f"data/template{themeName}.json",
                      interFolder / "scheme/default.txt")
    g.generateSchemes(factoryFolder / "template/muxlaunch.txt",
                      factoryFolder / f"data/template{themeName}.json",
                      interFolder / "scheme/muxlaunch.txt")
    if gridSupport:
        g.generateSchemes(factoryFolder / "template/muxplore.txt",
                          factoryFolder / f"data/template{themeName}.json",
                          interFolder / "scheme/muxplore.txt")
    g.zipFolder(interFolder, buildFolder / f"Rezolution{themeName}{gridNameSupplement}.zip")
    d.deleteFilesInFolder(interFolder)


def generate(macros: list[str], grid: str):
    c.task("Generating __build folder...")
    d.deleteFolder(buildFolder)
    d.createFolder(buildFolder)
    if grid in {"both", "off"}:  # if No or Both
        for macro in macros:
            generateMacro(macro)
    if grid in {"both", "on"}:  # if Yes or Both
        for macro in macros:
            generateMacro(macro, True)
        g.zipFolder(iconsFolder, buildFolder / "RezolutionIcons.zip")
    c.task("Cleaning up...")
    d.deleteFolder(interFolder)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="rezolution",
        description="An elegant and easy on the eyes MuOS theme.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "-t",
        "--theme",
        help="theme variant to generate (Dark, Indigo, OLED, White, All)",
        metavar="THEME",
        type=str,
        dest="theme",
        default="All",
    )
    parser.add_argument(
        "-g",
        "--grid",
        help="generate themes with grid variant (on, off, both)",
        metavar="GRID",
        type=str,
        dest="grid_style",
        default="both",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        help="run in interactive mode",
        action="store_true",
        dest="interactive_flag",
    )
    args = parser.parse_args()

    macros_list = ["Dark", "Indigo", "OLED", "White"]
    if args.interactive_flag:
        res = c.ask("Do you want to generate the theme with grid support ?", ["Both", "No", "Yes"])
        grid = ("both", "off", "on")[res]

        macro_choice = c.ask("Which theme variants do you want?", ["All", *macros_list])
        macros = macros_list if macro_choice == "All" else macros_list[macro_choice - 1]
    else:
        grid = args.grid_style
        macros = macros_list if args.theme == "All" else list(set(s.strip() for s in args.theme.split(",")))

    generate(macros, grid)
