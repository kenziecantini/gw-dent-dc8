import sys
from bs4 import BeautifulSoup


def parse_report(file_path):
    """
    Parse a ZAP HTML report and extract detailed alert information from the 'alerts' table.

    Args:
        file_path (str): Path to the ZAP HTML report file.

    Returns:
        dict: A dictionary with risk levels as keys and lists of (alert_name, instance_count) tuples as values.
    """
    alert_summary = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            # Find the 'alerts' table, which contains detailed alert information
            alert_table = soup.find('table', class_='alerts')
            if not alert_table:
                print(f"Warning: No 'alerts' table found in {file_path}")
                return {}

            # Skip the header row and iterate through the data rows
            rows = alert_table.find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    # Extract alert name, risk level, and instance count
                    description = cols[0].text.strip()  # Alert name
                    severity = cols[1].text.strip()  # Risk level (e.g., Medium, Low)
                    count = int(cols[2].text.strip())  # Number of instances
                    if severity not in alert_summary:
                        alert_summary[severity] = []
                    alert_summary[severity].append((description, count))
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return alert_summary


def compare_reports(before, after):
    """
    Compare the detailed alerts from the 'before' and 'after' ZAP reports and print the differences.

    Args:
        before (dict): Parsed alert data from the 'before' report.
        after (dict): Parsed alert data from the 'after' report.
    """
    print("Comparison of ZAP Scan Reports:\n")

    # Function to print alerts for a given report
    def print_alerts(report, title):
        print(f"{title}:")
        for severity, alerts in report.items():
            total = sum(count for _, count in alerts)
            print(f"  {severity}: {total} alerts ({len(alerts)} unique)")
            for description, count in alerts:
                print(f"    - {description}: {count}")

    print_alerts(before, "Before WAF")
    print("\nAfter WAF:")
    print_alerts(after, "After WAF")

    # Find differences
    print("\nDifferences (Before -> After):")
    all_severities = set(before.keys()).union(after.keys())
    for severity in sorted(all_severities):
        before_alerts = {desc: count for desc, count in before.get(severity, [])}
        after_alerts = {desc: count for desc, count in after.get(severity, [])}
        all_descriptions = set(before_alerts.keys()).union(after_alerts.keys())
        for desc in sorted(all_descriptions):
            before_count = before_alerts.get(desc, 0)
            after_count = after_alerts.get(desc, 0)
            if before_count != after_count:
                change = "Resolved" if after_count == 0 else f"{before_count} -> {after_count}"
                print(f"  {severity} - {desc}: {change}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python analyze_reports.py <before_report> <after_report>")
        sys.exit(1)

    before_report = parse_report(sys.argv[1])
    after_report = parse_report(sys.argv[2])
    compare_reports(before_report, after_report)
