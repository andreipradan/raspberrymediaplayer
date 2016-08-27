import subprocess


def send_command(*args):
    delimiter = '&&'
    if len(args) == 2 and delimiter in args[1]:
        split_arg = args[1].split(delimiter)
        args = [args[1]]
        args.extend(split_arg)
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    return process.communicate()[0].decode("utf-8")
