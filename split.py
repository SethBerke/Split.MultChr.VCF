# FIND LINES ASSOCIATED WITH FIRST OCCURRENCES OF CHR##
def find_first_occurrence_line_numbers(file_path):
    first_occurrences = {}
    line_number = 0

    with open(file_path, "r") as file:
        for line in file:
            line_number += 1
            if line.startswith("chr"):
                chromosome = line.split()[0]  # Extract the chromosome name from the line

                if chromosome not in first_occurrences:
                    first_occurrences[chromosome] = line_number

    return first_occurrences

# DEFINE A DICTIONARY WITH CHR## AS KEYS AND THEIR UPPER AND LOWER BOUND LINE NUMBERS AS VALUES
chrRanges = {}
class Bounds:
        def __init__(self, lowerBound: float, upperBound: float):
             self.lowerBound = lowerBound
             self.upperBound = upperBound

# Call the function to find the first occurrences of each chromosome
file_path = "./multi.vcf"
first_occurrences = find_first_occurrence_line_numbers(file_path)

# Calculate header lower and upper limits (assuming it's before the first "chr1" line)
header_lower_limit = 0
header_upper_limit = first_occurrences.get("chr1", 1) - 1

# Define the chromosome bounds
for i in range(1, 23):
    chromosome = "chr" + str(i)
    chromosomeUB = "chr" + str(i + 1)
    lower_bound = first_occurrences.get(chromosome)
    upper_bound = first_occurrences.get(chromosomeUB, float("inf")) - 1

    if lower_bound is not None and upper_bound is not None:
        chrRanges[chromosome] = Bounds(lower_bound, upper_bound)
    else:
        print(f"Target values not found for {chromosome} and/or {chromosomeUB}.")

# WRITE EACH FILE AS A DISTINCT VCF WITH A SINGULAR CHR##
def writeFiles(input_file_path, output_file_path, lower_limit, upper_limit, header_lower_limit, header_upper_limit):
    with open(input_file_path, "r") as input_file:
        with open(output_file_path, "w") as output_file:
            header_lines = []
            for line_num, line in enumerate(input_file, start=1):
                if header_lower_limit <= line_num <= header_upper_limit:
                    header_lines.append(line)
            output_file.writelines(header_lines)
            input_file.seek(0)
            for line_num, line in enumerate(input_file, start=1):
                if lower_limit <= line_num <= upper_limit:
                    output_file.write(line)

# Create individual VCF files for each chromosome
for i in range(1, 23):
    chromosome = "chr" + str(i)
    filename = "chr" + str(i) + ".vcf"
    print("ITERATION: ", i)
    print("INPUT FILE PATH", file_path)
    print("OUTPUT FILE NAME", filename)
    print("CHR LOWER BOUND", chrRanges[chromosome].lowerBound)
    print("CHR UPPER BOUND", chrRanges[chromosome].upperBound)
    print("HEADER LOWER LIMIT", header_lower_limit)
    print("HEADER UPPER LIMIT", header_upper_limit)
    writeFiles(file_path, filename, chrRanges[chromosome].lowerBound, chrRanges[chromosome].upperBound, header_lower_limit, header_upper_limit)
