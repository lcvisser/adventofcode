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

safe_report_count1 = 0
safe_report_count2 = 0
for line in data.strip().split('\n'):
    report = [int(x) for x in line.split()]
    if is_safe(report):
        safe_report_count1 += 1
        safe_report_count2 += 1
    else:
        # Try to remove one level and try again
        for i in range(len(report)):
            if is_safe(report[:i] + report[i+1:]):
                safe_report_count2 += 1
                break

# Part 1: number of safe reports
print(f"Number of safe reports: {safe_report_count1}")

# Part 2: number of safe reports with Problem Dampener
print(f"Number of safe reports with Problem Dampener: {safe_report_count2}")
