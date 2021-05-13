# xliff-translation-updater
A translator tool for updating translations embedded in xliff files.

Written by Gökdeniz Özkan, github: gokdenizozkan
Under MIT License, see further information in LICENSE document.

# how it works
A template, in our case, an original & pure xliff file is used as a base to add our translations and export to a different xliff file.
Apart from a template, an easily editable file -like txt- that stores the translated text *line by line* is needed.

Translated text is added to the text of the template file line by line.
Then the resulting text is exported to a seperate xliff file.

# how to use
v0.1:
1. Download the Python 3 from https://www.python.org/downloads/
2. Download the source code.
3. Right click to the 'xliff_transup.py' and Open With Python.
4. Follow the instructions.

Though I have written some other functions that can be used, the only function that needed is *form_xliff*.
This one is implemented in the releases. Further features may be added in the future versions.
