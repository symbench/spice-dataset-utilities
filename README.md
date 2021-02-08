# SPICE Netlist Dataset Utilities
## Creation
This repository contains scripts for curating a dataset of SPICE netlists. Currently, these are KiCad schematics scraped from GitHub and then converted to SPICE netlists.

A couple caveats:
- The GitHub search API requires you to scope code searches to a repo or organization (unlike their search in the browser). 
- The search API only returns up to 1k results. 
- KiCad doesn't have a command line interface for converting schematics to netlists. This is annoying but can be worked around in a pretty hacky way with GUI scripting (ie, xdotool). 
- Schematics may need to be updated before they can export a meaningful netlist. A bit annoying but can be solved w/ GUI scripting, too (it requires KiCad which doesn't have a useful CLI). 

## Visualization
