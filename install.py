import os

# since the python_core package is private,
# you need to already have it on your computer and to specify it's path
python_core_path = r"C:\Users\Lenny\Documents\CODE_MesProjets\0000_python_core"

# create the install commands
cmds = list()
cmds.append(f"cd {os.path.dirname(__file__)}")
cmds.append("python -m venv venv")
cmds.append(r"call venv\Scripts\activate.bat")
cmds.append(f"pip install -e {python_core_path}")

# write the commands in a .bat file
install_file = os.path.join(os.path.dirname(__file__), "install.bat")
with open(install_file, "w") as file:
    file.write("\n".join(cmds))

# execute the commands
os.system(f"call {install_file}")

# remove the created bat file
os.remove(install_file)

print("\n\nSuccessfully installed\n\n")
