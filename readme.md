# Koopatlas Updated ("Koopatlas-Marinara" fork)

An editor for world maps for the custom Koopatlas Engine for New Super Mario Bros. Wii, created by Treeki.

Koopatlas $${\color{red}Marinara}$$ contains a few enhancements for Koopatlas Updated, summed up here:
- Migration to PyQt6, which allows for:
  - Native dark mode that relies on the system settings rather than "themes" or anything similar
  - A much cleaner looking base UI
  - Other QoL features from this migrate as well, probably...
- Improved UI design
  - World exit/actual stage nodes now have significantly better renders, and the colors now update depending on if the stage is one-time, has a secret, etc.
  - KP's World Editor no longer requires manually typing in hex codes, and now has a proper color picker UI
  - Another grid mode, ported from Reggie-Next
  - Better organization of the menu bar, with less categories and better option names
    - Shortcuts for almost every single option, as well
    - Cutting with Ctrl+X now functions properly (HOW was this never a feature before?!)
  - Almost every single piece of the UI can now be toggled on/off
  - All options should have a new, more modern looking icon assigned to them (from <https://icons8.com/icons/all--style-color>)
  - The default viewport background color has been changed to be the same as Reggie-Next's, to better fit both light and dark mode
    - The background color now also changes color automatically if Water.brres or Lava.brres is set

There are currently a few planned features for future releases as well, as listed:
- Custom themes outside of light/dark mode
- Custom background color definitions
- Better World/Level ID spinner for nodes
- Settings menu
- "Open recents..." option functionality
- Proper loading screen for maps, as well as a better general loading time
- Fix the decently severe lag that occurs when trying to play animations (probably something caused by the migration from PyQt5->PyQt6)
- Any and all crashes within the UI (or as many as can be found)
- PyQt5 support, as well as PyQt4 support (maybe)
- PyQt7+ support in the future
- Undo/Redo

If you have any ideas or suggestions for features/bugfixes, feel free to create an issue in this repository.

## Original readme below

Where do I even begin with this...

This is the editor half of Koopatlas - a totally new 2D map engine we wrote
for Newer. Without going into too much detail, here's a quick roundup:

- Ridiculously buggy and unpolished editor
- 2D maps with an unlimited* amount of layers
- Tileset layers, supporting an unlimited* amount of tilesets
- Doodad layers, allowing you to place arbitrary textures on the map at any
  position and scale/rotate them
- Doodad animations
- Unlockable paths and level nodes
- More hardcoded things than you can shake a stick at (possibly rivalling
  Nintendo's 3D maps)
- Multiple maps with entrances/exits a la Reggie
- Maps are stored in a ".kpmap" format for easy editability - a JSON file in a
  specific format - and exported to an optimised ".kpbin" format for usage
  in-game

*\*Unlimited: Not really. This is the Wii, a game console which was
underpowered when it was released in 2006. There's not a lot of room in RAM
for lots of tilesets and doodads. A couple of the Newer maps use up almost all
the available space, so...*

If you want to make maps, feel free to try it. Then bash your head against a
wall when you accidentally close the editor and lose your unsaved work because
there's no warning against that. Or when it crashes on you, which might happen.
