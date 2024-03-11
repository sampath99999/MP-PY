import os
import subprocess
import shutil
import webbrowser

fmsApiRepo = "git@gitlab.pixelvide.com:ifmismp/fms-apis.git"
fmsUiRepo = "git@gitlab.pixelvide.com:ifmismp/fms-ui.git"
hrmsApiRepo = "git@gitlab.pixelvide.com:ifmismp/hrms-apis.git"
hrmsUiRepo = "git@gitlab.pixelvide.com:ifmismp/hrms-ui.git"
commonFrontendRepo = "git@gitlab.pixelvide.com:ifmismp/common-frontend.git"


def check_nodejs_version():
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        installed_version = result.stdout.strip()
        if installed_version.startswith("v18"):
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def check_folder(folder_name):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder_name)
    return os.path.exists(folder_path)


def clone_repo(repo_url, folder_name):
    os.system(f"git clone {repo_url} {folder_name}")
    print(f"Cloned {folder_name} ✅")
    return folder_name


def processFMSCloning():
    if not check_folder("fms-apis"):
        clone_repo(fmsApiRepo, "fms-apis")
    if not check_folder("fms-ui"):
        clone_repo(fmsUiRepo, "fms-ui")
    print("FMS Repo Cloned ✅")


def processHRMSCloning():
    if not check_folder("hrms-apis"):
        clone_repo(hrmsApiRepo, "hrms-apis")
    if not check_folder("hrms-ui"):
        clone_repo(hrmsUiRepo, "hrms-ui")
    print("HRMS Repo Cloned ✅")


def processCommonFrontend():
    if not check_folder("common-frontend"):
        clone_repo(commonFrontendRepo, "common-frontend")
    print("Common Frontend Repo Cloned ✅")


def processComposerPackages():
    if not check_folder("fms-apis/vendor"):
        os.chdir("fms-apis/")
        os.system("..\php\php.exe ..\php\composer.phar update")
        os.chdir("../")
    if not check_folder("hrms-apis/vendor"):
        os.chdir("hrms-apis/")
        os.system("..\php\php.exe ..\php\composer.phar update")
        os.chdir("../")
    print("Composer Packages Updated ✅")


def processNodePackages():
    if not check_folder("fms-ui/node_modules"):
        os.chdir("fms-ui/")
        os.remove("package-lock.json")
        if check_nodejs_version() == True:
            os.system("npm install --legacy-peer-deps")
        else:
            os.system("..\\nodejs\\npm.cmd install --legacy-peer-deps")
        os.chdir("../")
    if not check_folder("hrms-ui/node_modules"):
        os.chdir("hrms-ui/")
        os.remove("package-lock.json")
        if check_nodejs_version() == True:
            os.system("npm install --legacy-peer-deps")
        else:
            os.system("..\\nodejs\\npm.cmd install --legacy-peer-deps")
        os.chdir("../")
    print("Node Packages Updated ✅")


def is_postgresql_installed():
    return False
    try:
        result = subprocess.run(
            ["pg_config", "--version"], capture_output=True, text=True
        )
        if result.returncode == 0 and "PostgreSQL" in result.stdout:
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def processPostgres():
    if is_postgresql_installed() == False:
        print("Postgresql is not installed\n")
        option = int(input("Do you want to download postgresql?\n1: Yes\n0: No\n"))
        if option == 1:
            webbrowser.open("https://www.postgresql.org/download/")
            option = int(input("Is Install Done?\n1: Yes\n0: No\n"))
    print("Postgresql ✅")


processFMSCloning()
processHRMSCloning()
processCommonFrontend()

processComposerPackages()
processNodePackages()
processPostgres()

input("")
