file_path = "./multi.vcf"
file = open(file_path, "r")

# FIND LINES ASSOCIATED WITH FIRST OCCURENCES OF CHR##
def find_line_with_target(file_path, target):
    last_line_number = 0
    with open(file_path, "r") as file:
        for line_num, line in enumerate(file, start=1):
            if target in line and '#' not in line:
                return line_num
            last_line_number = line_num
    return last_line_number

# DEFINE A DICTIONARY WITH CHR## AS KEYS AND THEIR UPPER AND LOWER BOUND LINE NUMBERS AS VALUES
chrRanges = {}
class Bounds:
        def __init__(self,lowerBound: float,upperBound: float):
             self.lowerBound = lowerBound
             self.upperBound = upperBound

print("HI")
header_lower_limit = 0
header_upper_limit = find_line_with_target(file_path, "chr1") - 1

for i in range(1, 23):
    chromosome = "chr" + str(i)
    chromosomeUB = "chr" + str(i + 1)
    lower_bound = 0
    upper_bound = 0
    if i != 22:
        lower_bound = find_line_with_target(file_path, chromosome)
        upper_bound = find_line_with_target(file_path, chromosomeUB)
        print(find_line_with_target(file_path, chromosome))
    else:
        lower_bound = find_line_with_target(file_path, chromosome)
        upper_bound = find_line_with_target(file_path, "LAST")
        print(find_line_with_target(file_path, chromosome))
    if lower_bound is not None and upper_bound is not None:
        chrRanges[chromosome] = Bounds(lower_bound, upper_bound - 1)
    else:
        print(f"Target values not found for {chromosome} and/or {chromosomeUB}.")

for chromosome, bounds in chrRanges.items():
    print(f"{chromosome} : {bounds.lowerBound} - {bounds.upperBound}")

# WRITE EACH FILE AS A DISTINCT VCF WITH A SINGULAR CHR##
def writeFiles(input_file_path, output_file_path, lower_limit, upper_limit, header_lower_limit, header_upper_limit):
    with open(input_file_path, "r") as input_file:
        with open(output_file_path, "w") as output_file:
            header_lines = []
            for line_num, line in enumerate(input_file, start = 1):
                if header_lower_limit <= line_num <= header_upper_limit:
                    header_lines.append(line)  
            output_file.writelines(header_lines)
            input_file.seek(0) 
            for line_num, line in enumerate(input_file, start = 1):
                if lower_limit <= line_num <= upper_limit:
                    output_file.write(line)  
            
for i in range(1, 23):
    chromosome = "chr" + str(i)
    filename = "chr" + str(i) + ".vcf"
    writeFiles(file_path,filename,chrRanges[chromosome].lowerBound,chrRanges[chromosome].upperBound, header_lower_limit, header_upper_limit)