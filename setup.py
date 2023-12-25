import subprocess
import time


def run_cmd(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess_return = process.stdout.read()
    subprocess_error = process.stderr.read()
    return subprocess_return, subprocess_error


def main():
    time.sleep(5)
    cmds = ['python manage.py migrate',
            'python manage.py runserver 0.0.0.0:8000']

    for cmd in cmds:
        _, _ = run_cmd(cmd)


if __name__ == '__main__':
    main()

