# Written by Gökdeniz Özkan, github:gokdenizozkan, linkedin:/in/gokdenizozkan
# Under MIT License, see further information on LICENSE file.
# PyInstaller is used to create an executable file.

# A translator tool for updating translations of xliff files; first purpose was to create a ready-to-upload SmartCAT xliff files to update translation on SmartCAT.
# It is done by storing relevant information aquired from an original & pure xliff file, named as template, and exporting the manipulated/updated version out.
# txt or any easily editable file that contains Target Text should be prepared line by line. See the example_translated.txt.

from shutil import copyfile
import sys
import os
import re


def duplicate_file(original_file_path, name="", path=""):
    """
    Can be used to duplicate a file (e.g. to backup)
    :param original_file_name: the name of the file to be duplicated
    :param name: OPTIONAL the name of the duplicated file, path will be set to the current path (on_current_path())
    :param path: OPTIONAL the path of the duplicated file, if it is given, 'param name' will not be used
    """
    default_name = os.path.splitext(original_file_path)[0] + "-duplicated"
    extension = os.path.splitext(original_file_path)[1]

    default_path = on_current_path("{P_name}{P_extension}".format(
        P_name=name if name else default_name, P_extension=extension))  # default value
    try:
        copyfile(original_file_path, "{}".format(
            path if path else default_path))
    except:
        input("Paths cannot be the same. The file will be duplicated on the current directory of which python code runs.\n\nEnter anything to proceed.")
        duplicate_file(original_file_path)


def form_xliff(template, translated_file):
    """
    Can be used to form a xliff file derived from a template, which is an original & pure xliff file of the source text. In this case, source text will be added translations.
    :param template: the path of the the original & pure form of the source text, which is called template in this context (txt, xliff, or any easily editable file extension works)
    :param translated_file: the path of the file that contains the translated text (txt or any editable file that contains only the translated text, line by line)
    """
    pattern = r'(?P<preciding>xml:space="preserve">)(?P<following></target></trans-unit>)'

    with open(template, "r", encoding="utf-8") as template_file:
        template_text = template_file.read()
    with open(translated_file, "r+", encoding="utf-8") as translated_file:
        translated_lines = translated_file.readlines()

    for line in translated_lines:
        # template_text = re.sub(pattern, r'\g<preciding>' + line + r'\g<following>', template_text, 1)  # below is same as this one
        template_text = re.sub(
            pattern, fr'\g<preciding>{line}\g<following>', template_text, count=1)
    with open(on_current_path("output.xliff"), "w", encoding="utf-8") as output_file:
        output_file.write(template_text)


def get_trans_unit_id(path):
    """
    Can be used to get the "trans-unit id" of the original xliff file. Not used anywhere around the code as of v0.1
    :param path: the path of the xliff file
    """
    pattern = r'<trans-unit id="(\d*)"'
    with open(path, "r", encoding="utf-8") as f:
        return re.search(pattern, f.read()).group(1)


def menu():
    """
    Can be used to prompt users with a menu that uses the program
    """
    prompt_text = """To update an xliff file, 
        - 'the path of the template, which is the original & pure xliff file'
        - 'the path of the text file that contains translated texts line by line'
        are needed.
        
        The use of this program is rather limited. You can see the source code and use any function according to your needs. However, this alone will be fine.

        If you need assistance, please see the example files.
        ------
        Please put your template (original & pure xliff) file and translated text file into the same directory as of the 'xliff_transup.exe'
        
        If you are ready, please enter the TEMPLATE FILE's and the TRANSLATED FILE's name with their extensions as given below:
        template.xliff, translated.txt
        
        Please be CAUTIOUS that there is a comma and a space between the two file names.
        ------"""
    user_inputs = ocp_input(prompt_text + "\n\nExample input: 'template.xliff, translated.txt' | Please take the comma in mind.\nYour input >>> ", split=True, split_param=", ", strip=True, strip_param="'")
    form_xliff(user_inputs[0], user_inputs[1])


def ocp_input(ask_user=None, split=False, split_param=None, strip=False, strip_param=None, replace=False, replace_param_pattern="", replace_param_repl="", replace_param_count=None):
    """
    Can be used to ask user the path or name of a file. If the input is the name, it will be converted into path using on_current_path function that retrieves the main python file's directory as its base.
    :param ask_user: OPTIONAL a text to be shown when prompting the user for input; default = None
    :param split: OPTIONAL a boolean for the use of split method; default = False
    :param split_param: OPTIONAL a string to be used as the parameter for split method; default = None
    :param strip: OPTIONAL a boolean for the use of strip method; default = False
    :param strip_param: OPTIONAL a string to be used as the parameter for split method; default = None
    :param replace: OPTIONAL a boolean for the use of replace method; default = False
    :param replace_param_pattern: OPTIONAL a string to be used as the parameter for replace method's first parameter; default = ""
    :param replace_param_repl: OPTIONAL a string to be used as the parameter for replace method's second parameter; default = ""
    :param replace_param_count: OPTIONAL an integer to be used as a parameter for replace method's third parameter; default = None
    """
    the_input = input(ask_user)
    if strip:
        the_input = the_input.strip(strip_param)
    if replace:
        the_input = the_input.replace(replace_param_pattern, replace_param_repl)
    if split:
        temp_list = the_input.split(split_param)
        for i in range(len(temp_list)):
            temp_list[i] = on_current_path(temp_list[i])
        return temp_list
    return on_current_path(the_input)


def on_current_path(file_name):
    """
    Can be used to retrieve the path based on the python code that is running.
    :param file_name: the name of the file with its extension

    example:
    print(on_current_path("template.xliff"))
    """
    return os.path.join(sys.path[0], file_name)


def rename_file(path, new_name="", new_extension="", duplicate_first=False):
    """
    Can be used to change the name & extension of a file.
    :param path: the path of the file
    :param new_name: OPTIONAL the name to be applied
    :param new_extension: OPTIONAL the extension to be applied
    :param duplicate_first: OPTIONAL a boolean for whether duplicating the file before it is renamed or not

    example:
    rename_file(on_current_path("template.xliff"), new_extension="txt")
    """
    name = os.path.splitext(path)[0]
    extension = os.path.splitext(path)[1]

    if duplicate_first:
        duplicate_file(path)
    if new_name:
        name = new_name
    if new_extension:
        extension = new_extension

    os.rename(path, "{P_name}.{P_extension}".format(
        P_name=name, P_extension=extension))


try:
    menu()
except Exception as e:
    input(str(e) + "\n\nAn error has occured. Enter anything to exit.")
    sys.exit()
input("If you are able to see this message without any errors, it means your process is finished.")