# FIND LINES ASSOCIATED WITH FIRST OCCURRENCES OF CHR##
def chromosomeSplitPoints(file_path):
    first_occurrences = {}
    unique_chromosomes = set()
    line_number = 0
    with open(file_path, "r") as file:
        for line in file:
            line_number += 1
            if line.startswith("chr") and "#" not in line:
                chromosome = line.split()[0]  
                unique_chromosomes.add(chromosome)
                if chromosome not in first_occurrences:
                    first_occurrences[chromosome] = line_number
    return first_occurrences, unique_chromosomes

file_path = "./multi.vcf"
first_occurrences, unique_chromosomes = chromosomeSplitPoints(file_path)

# CALCULATE HEADERLINE BOUNDS
header_lower_limit = 0
header_upper_limit = min(first_occurrences.values()) - 1

# DEFINE CHR## BOUNDS
chrRanges = {}
class Bounds:
        def __init__(self, lowerBound: float, upperBound: float):
             self.lowerBound = lowerBound
             self.upperBound = upperBound

for chromosome in unique_chromosomes:
    lower_bound = first_occurrences[chromosome]
    if len(unique_chromosomes) > 1:
        upper_bound = first_occurrences.get(next(iter(unique_chromosomes - {chromosome}), float("inf"))) - 1
    else:
        upper_bound = float("inf")
    if lower_bound is not None and upper_bound is not None:
        chrRanges[chromosome] = Bounds(lower_bound, upper_bound)
    else:
        print(f"Target values not found for {chromosome}.")

# WRITE EACH FILE AS A DISTINCT FILE WITH A SINGULAR CHR##
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

# CREATE INDIVIDUAL .VCF FILES FOR EACH CHR##
chromosomes_sorted = sorted(unique_chromosomes, key=lambda x: first_occurrences[x])
num_unique_chromosomes = len(chromosomes_sorted)
for i in range(len(chromosomes_sorted)):
    chromosome = chromosomes_sorted[i]
    lower_bound = first_occurrences[chromosome]
    if i + 1 < num_unique_chromosomes:
        upper_bound = first_occurrences[chromosomes_sorted[i + 1]] - 1
    else:
        upper_bound = float("inf")
    chrRanges[chromosome] = Bounds(lower_bound, upper_bound)
    filename = f"{chromosome}.vcf"
    print("\nITERATION:", chromosome)
    print("INPUT FILE PATH:", file_path)
    print("OUTPUT FILE NAME:", filename)
    print("CHR LOWER BOUND:", chrRanges[chromosome].lowerBound)
    print("CHR UPPER BOUND:", chrRanges[chromosome].upperBound)
    print("HEADER LOWER LIMIT:", header_lower_limit)
    print("HEADER UPPER LIMIT:", header_upper_limit)
    writeFiles(file_path, filename, chrRanges[chromosome].lowerBound, chrRanges[chromosome].upperBound, header_lower_limit, header_upper_limit)