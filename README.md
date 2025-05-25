# CLUSTERIFIER
By dk865


### How it works:
- First, the script searches for any line containing `_lightmode` in the selected `VMF` file.
- These are all removed to avoid conflicts.
- Next, it searches for lines containing `_lightHDR`. 
- It then appends a new `_lightmode` entry containing the selected light mode from the dropdown.
- Lastly, it saves the file and shows a message box.

>[!WARNING]
>If you manually tweaked your map in a text editor, this can corrupt it (in semi-rare cases). Please make a backup!


Todo:
- Allow direct decompiling of a `BSP`, modifying, then recompiling?