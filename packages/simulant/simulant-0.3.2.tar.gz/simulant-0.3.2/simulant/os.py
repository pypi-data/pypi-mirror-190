import subprocess


class Shell:
    @staticmethod
    def execute(command):
        try:
            output = subprocess.check_output(command, shell=True)
            output_as_string = output.decode("utf-8")
            normal_output = output_as_string.rstrip('\n')
            if normal_output.isdigit() and not ',' in normal_output and not '.' in normal_output:
                return int(output)
            elif normal_output.isdigit() and ',' in normal_output or '.' in normal_output:
                return float(output)
            else:
                return normal_output
        except subprocess.CalledProcessError:
            raise ValueError("Could not execute command")
