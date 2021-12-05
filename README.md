# gpx-renamer
## Standalone
This is an early version of GPX renamer with tkinter GUI
Works as is, as long as you provide:
* key.json with your bigdatacloud API key (in the same folder as the script) like this:
    ```json
        {
        "key":"your_key_here"
        }
    ```
### Folder selection:
This program can use 4 folder, however, just 2 are needed
* input - folder with the GPX files to move and rename
* ouput - folder for the renamed files
* orig (optional) - if specified, copies all files from input here begore processing them
* manual (optional) - for incomplete GPX files or non-GPX files
#### automatic
Searches for folders name like the above in the same folder the script is in
#### manual
You can specify paths to all the folders in the GUI

### Output options and missing info handeling
Two textboxes between the two start buttons
First textbox:
#### Output format
You can specify the format of the output
* uses percent sign (%) followed by letter(s) for every piece of information
* This is the default format, you can change it in the code itself, currently on line 516:
    ```python 
        self.formatEntryText.set("%f-%y-%m-%st-%e")
    ```
* You can use only characters specified in the whitelist (currently with czech characters)
    ```python
        whitelist = set(string.ascii_letters + string.digits + "!_-()ěščřžýáíéĚŠČŘŽÝÁÍÉÚŮúůťď∶ ")
    ```
* the percent placeholders are as follows:
    ```
        %c      country code - always
        %dur    duration in format hour:minute
        %f      country code, only when not cz (deletes one character next to itselft if not cz)
        
        %st     locality of the first point- API
        %e      locality of the last point - API
        %y      year of the first point
        %m      month of the first point
        %d      day of first point
        %ts     time of start in format  hour:minute
        %te     time of end in format  hour:minute
    ```
#### Missing info handeling
Defines how to handle missing info (empty time, locality etc.)
```
        "0" - deletes one of surrounding characters
        "1" - doesn't delete anything
        "2" - moves the final gpx to manual if specified, otherwise as "0"
```
## Structured
Not yet functional, work in progress
Some general info:
* automatic folder search can find input, output, manual and orig folders in the folder of the main script
* how to use rename options is explained in the code in comments (for now)

