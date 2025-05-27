# CLUSTERIFIER

>**Latest *Semi*-Stable Release: [1.4.0](https://github.com/dk865/clusterifier/releases/tag/v1.4.0)**

## Features:
### Single File Mode
- Change all of the light entities in a map to `Static`, `Specular`, `Static Bounce`, or `Dynamic`
- Convert all light entities to/from `light_rt` and `light_rt_spot`
- Automatically backup the `VMF` file (in case of damage or corruption to file, only semi-rare)

### Batch Mode
- Recursively change all of the light entities in every map to `Static`, `Specular`, `Static Bounce`, or `Dynamic`
- Convert all light entities in every map to/from `light_rt` and `light_rt_spot`
- Ignores any `VMF` files that don't contain lights (\*cough cough instances\*)
- Automatically backup all `VMF` files (that contain lights), and compress to a `ZIP` file


## How it works:
- First, the script searches for any line containing `_lightmode` in the selected `VMF` file(s)
- These are all removed to avoid conflicts.
- Next, it searches for lines containing `_lightHDR`. 
- It then appends a new `_lightmode` entry containing the selected light mode from the dropdown.
- Lastly, it saves the file and shows a message box.

>[!WARNING]
>If you manually tweaked your map in a text editor, this can corrupt it (in semi-rare cases). Please make a backup!

> Made with <3 by dk865