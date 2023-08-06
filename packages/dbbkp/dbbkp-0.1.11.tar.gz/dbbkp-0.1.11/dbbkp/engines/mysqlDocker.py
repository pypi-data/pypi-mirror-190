import time
import os
import utilum
from . import scripts


def gitConfig(name, email, repoPath):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''
    utilum.system.shell(wrapperRegular(
        f'git config --local user.name "{name}"'))
    utilum.system.shell(wrapperRegular(
        f'git config --local user.email "{email}"'))


def gitInitOrRegular(repoPath):
    def wrapperRegular(cmd):
        return f'''cd {repoPath} && {cmd}'''

    cmd3 = wrapperRegular(f'''git add .''')
    cmd4 = wrapperRegular(f'''git commit -m "Regular Update"''')
    cmd5 = wrapperRegular(f'''git push origin main''')

    utilum.system.shell(cmd3)
    utilum.system.shell(cmd4)
    utilum.system.shell(cmd5)

    return None


def manageDatabases(repoPath, containerName, passwordFilePath):
    cmd1 = scripts.showDatabasesDocker(containerName, passwordFilePath)
    (out, err) = utilum.system.shellRead(cmd1)
    decoded = out.decode('utf-8')
    dbs = decoded.split("\n")
    dbs = dbs[1:-1]

    for databaseName in dbs:
        outputDbPath = os.path.join(repoPath, databaseName + '.sql')
        exportCmd = scripts.exportDatabaseDocker(
            containerName, passwordFilePath, databaseName, outputDbPath)
        utilum.system.shell(exportCmd)


def flow(config):
    # Mid Function to Transfer DB Files
    manageDatabases(config.STAGE_STORAGE_PATH,
                    config.CONTAINER_NAME, config.PASSWORD_FILE_PATH)

    # git config set
    gitConfig(config.GIT_NAME, config.GIT_EMAIL, config.STAGE_STORAGE_PATH)

    # Last Function to Commit
    gitInitOrRegular(config.STAGE_STORAGE_PATH)


def start(config):
    count = 0.001
    while (True):
        print("\nCount: ", count)
        flow(config)
        time.sleep(config.INTERVAL)
        count += 0.001
