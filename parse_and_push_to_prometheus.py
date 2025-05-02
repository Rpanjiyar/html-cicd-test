from bs4 import BeautifulSoup
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import sys

# Parse the cucumber report HTML
with open(sys.argv[1], 'r') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Example: Extract passed and failed tests (adjust based on your HTML structure)
passed_tests = len(soup.find_all('div', class_='passed'))
failed_tests = len(soup.find_all('div', class_='failed'))

# Set up Prometheus metrics
registry = CollectorRegistry()

passed_gauge = Gauge('passed_tests', 'Number of passed tests', registry=registry)
failed_gauge = Gauge('failed_tests', 'Number of failed tests', registry=registry)

passed_gauge.set(passed_tests)
failed_gauge.set(failed_tests)

# Push to Push Gateway
push_to_gateway('http://<push_gateway_address>:9091', job='test_report', registry=registry)
