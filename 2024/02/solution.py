# Read data
input_file = "2024/02/input.txt"
with open(input_file) as f:
    data = f.read()


def diff(report):
    return [n - c for c, n in zip(report[:-1], report[1:])]

def all_safely_increasing(diff_report):
    return all(1 <= d <= 3 for d in diff_report)

def all_safely_decreasing(diff_report):
    return all(-3 <= d <= -1 for d in diff_report)

def is_safe(report):
    diff_report = diff(report)
    return all_safely_increasing(diff_report) or all_safely_decreasing(diff_report)

safe_report_count = 0
for line in data.strip().split('\n'):
    report = [int(x) for x in line.split()]
    if is_safe(report):
        safe_report_count += 1

# Part 1: number of safe reports
print(f"Number of safe reports: {safe_report_count}")
