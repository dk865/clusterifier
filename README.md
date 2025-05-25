# CLUSTERIFIER
By dk865


### How it works:
- First, the script searches for any line containing `_lightmode` in the selected `VMF` file.
- These are all removed to avoid conflicts.
- Next, it searches for lines containing `_lightHDR`. 
- It then appends a new `_lightmode` entry containing the selected light mode from the dropdown.
- Lastly, it saves the file and shows a message box.

>[!WARNING]
>This can completely ruin your map, or corrupt it. Please select the backup option!


Todo:
- DON'T PROCESS FILES WITHOUT LIGHTS! (INSTANCES)
- Export a file containing the name of each light replaced?
- Allow direct decompiling of a `BSP`, modifying, then recompiling?
