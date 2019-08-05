file_names = ["Reading.py", "Parsing.py", "Calculator.py"]
result_file = "ksp.py"
result = open(result_file, "w")
for file_name in file_names:
    with open(file_name) as f:
        char = f.read(1)
        while char != "":
            result.write(char)
            char = f.read(1)
        result.write("\n")
