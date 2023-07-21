from subprocess import run, PIPE

path = "[path]"
app_name = "[app name]"
commands_array = ["adb","shell","input keyevent 85"]
try:
    result = run(commands_array, stdout=PIPE, stderr=PIPE, 
                  check=True, universal_newlines=True)
except Exception as e:
   print("An error occured:")
   print(e)

print(result.stdout)