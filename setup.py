from distutils.core import setup
import py2exe

#"d:\NeruralNetworks\DeepLearning_Py\    "
#setup(console=["testSetup.py"])

# to build the program
#python setup.py build

#You must be installed Python 3.6 and cx_Freeze.
#To install cx_Freeze, open your command prompt and type ‘pip install cx_Freeze‘. Make a .py program of yourself say ‘my first prog.py’ .
#Create a new python file named ‘setup.py’ on the current directory of your script.
#On the setup.py, code this and save it.
#With shift pressed right click on the same directory, so you are able to open a command prompt window.
#Type in the prompt as >> python setup.py build
#If your script is error free, then there is no problem on creating application.
#Check the newly created folder ‘build‘. It has another folder in it. Within that folder you can able to find your application. Run it. Make yourself hap

from cx_Freeze import setup, Executable

base = None


executables = [Executable("testSetup.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "test",
    options = options,
    version = "1.0",
    description = 'note',
    executables = executables
)