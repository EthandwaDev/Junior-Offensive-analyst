# Security Log Analysis - Data Analytics Approach

## Project Overview
Uses data analytics techniques to identify security threats and suspicious patterns in system logs. Combines Python, data science fundamentals, and cybersecurity knowledge.

## Objectives
- Parse and analyze security logs
- Identify anomalies and suspicious patterns
- Generate actionable security insights
- Visualize security events

## Log Analysis Workflow

### 1. Data Collection
Log sources:
- Web server logs (Apache, Nginx)
- Authentication logs (syslog)
- Firewall logs
- Application logs
- System event logs

### 2. Data Parsing & Cleaning
```python
import pandas as pd
import re
from datetime import datetime

def parse_apache_logs(log_file):
    """Parse Apache access logs"""
    # Apache log format: IP METHOD URL STATUS SIZE USER_AGENT
    pattern = r'(\S+) - - \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\S+) "([^"]*)" "([^"]*)"'
    
    logs = []
    with open(log_file, 'r') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                logs.append({
                    'ip': match.group(1),
                    'timestamp': datetime.strptime(match.group(2), '%d/%b/%Y:%H:%M:%S %z'),
                    'method': match.group(3),
                    'url': match.group(4),
                    'status': int(match.group(6)),
                    'size': match.group(7),
                    'user_agent': match.group(9)
                })
    
    return pd.DataFrame(logs)
```

### 3. Anomaly Detection Techniques

#### A. Statistical Analysis
```python
def detect_outliers_statistical(df, column, threshold=3):
    """
    Detect outliers using z-score method
    Values beyond 3 standard deviations are outliers
    """
    mean = df[column].mean()
    std = df[column].std()
    
    df['z_score'] = abs((df[column] - mean) / std)
    outliers = df[df['z_score'] > threshold]
    
    return outliers

# Example: Detect unusual large response sizes
large_responses = detect_outliers_statistical(logs, 'size')
print(f"Found {len(large_responses)} unusual response sizes")
```

#### B. Pattern-Based Detection
```python
def detect_brute_force(logs, threshold=10):
    """
    Detect brute force attempts:
    Multiple failed login attempts from same IP
    """
    failed_attempts = logs[logs['status'].isin([401, 403])]
    
    ip_attempts = failed_attempts.groupby('ip').size()
    suspicious_ips = ip_attempts[ip_attempts > threshold]
    
    return suspicious_ips

# Example: Find IPs with >10 failed attempts
suspicious = detect_brute_force(auth_logs)
for ip, count in suspicious.items():
    print(f"IP {ip}: {count} failed attempts")
```

#### C. Time-Series Analysis
```python
def detect_ddos_activity(logs, window='1H'):
    """
    Detect DDoS patterns using time-series analysis
    Unusual spike in traffic volume
    """
    logs['timestamp'] = pd.to_datetime(logs['timestamp'])
    
    # Count requests per hour
    traffic = logs.set_index('timestamp').resample(window).size()
    
    mean_traffic = traffic.mean()
    std_traffic = traffic.std()
    
    # Flag times with traffic > 3 std devs above mean
    ddos_periods = traffic[traffic > (mean_traffic + 3 * std_traffic)]
    
    return ddos_periods

# Example: Find unusual traffic periods
ddos_times = detect_ddos_activity(web_logs)
print("Potential DDoS periods:", ddos_times.index.tolist())
```

#### D. Clustering for Behavior Analysis
```python
from sklearn.cluster import DBSCAN
import numpy as np

def detect_anomalous_behavior(logs):
    """
    Use clustering to find unusual access patterns
    """
    features = logs[['hour', 'requests_count', 'unique_users']].values
    
    clustering = DBSCAN(eps=0.5, min_samples=5).fit(features)
    
    anomalies = logs[clustering.labels_ == -1]
    
    return anomalies

# Example: Find unusual time-based access patterns
anomalies = detect_anomalous_behavior(behavior_logs)
```

### 4. Security Indicators

#### A. Authentication Analysis
```python
def analyze_authentication(auth_logs):
    """Analyze authentication attempts for security"""
    
    results = {
        'total_attempts': len(auth_logs),
        'successful': len(auth_logs[auth_logs['status'] == 200]),
        'failed': len(auth_logs[auth_logs['status'].isin([401, 403])]),
        'unique_users': auth_logs['user'].nunique(),
        'unique_ips': auth_logs['ip'].nunique(),
    }
    
    # Failed login rate
    results['failed_rate'] = results['failed'] / results['total_attempts']
    
    # Users with unusual activity
    user_attempts = auth_logs.groupby('user').size()
    results['top_users'] = user_attempts.nlargest(5)
    
    return results
```

#### B. Access Pattern Analysis
```python
def analyze_access_patterns(logs):
    """Identify unusual access patterns"""
    
    # Detect access to suspicious paths
    suspicious_paths = [
        '/admin', '/config', '/.env', 'web.config',
        '/sql', 'union', 'select', 'drop'  # SQL injection patterns
    ]
    
    suspicious_access = logs[logs['url'].str.contains(
        '|'.join(suspicious_paths), 
        case=False, 
        na=False
    )]
    
    return suspicious_access
```

#### C. Geographic Analysis
```python
def analyze_ip_geography(logs):
    """Analyze access by geographic location"""
    
    # Using MaxMind GeoIP or similar
    # Maps IPs to countries/cities
    
    # Detect impossible travel (access from distant locations in short time)
    grouped = logs.groupby('user').apply(check_impossible_travel)
    
    return grouped

def check_impossible_travel(user_logs):
    """Check if user accessed from impossible locations"""
    # Calculate distance between locations
    # Flag if not enough time to travel between locations
    pass
```

### 5. Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_security_report(logs):
    """Create security visualization report"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Requests over time
    logs['hour'] = logs['timestamp'].dt.floor('H')
    logs.groupby('hour').size().plot(ax=axes[0,0], title='Requests Over Time')
    
    # 2. Top IPs
    logs['ip'].value_counts().head(10).plot(kind='barh', ax=axes[0,1], title='Top 10 IPs')
    
    # 3. Status code distribution
    logs['status'].value_counts().plot(kind='pie', ax=axes[1,0], title='Status Codes')
    
    # 4. Response size distribution
    logs['size'].hist(ax=axes[1,1], bins=50, title='Response Size Distribution')
    
    plt.tight_layout()
    plt.savefig('security_report.png')
```

## Sample Implementation

See `log_analysis.py` for complete working example with:
- Log parsing
- Multiple anomaly detection methods
- Security metrics calculation
- Report generation

## Tools & Libraries

```
pandas          - Data manipulation
numpy           - Numerical computing
scikit-learn    - Machine learning/clustering
matplotlib      - Visualization
seaborn         - Statistical visualization
python-geoip    - Geographic analysis
```

## Key Metrics to Track

1. **Failed Authentication Rate**
   - Target: < 5% of total attempts
   - Alert: > 20% indicates brute force attempts

2. **Unique Sources**
   - Track unique IPs making requests
   - Geographic diversity analysis

3. **Response Time Anomalies**
   - Detect slow responses (potential attack)
   - Baseline comparison

4. **Error Rate by Status Code**
   - 4xx: Client errors
   - 5xx: Server errors (investigate spikes)

5. **Traffic Volume**
   - Detect DDoS patterns
   - Capacity planning

## Report Generation

```python
def generate_security_report(logs):
    """Generate comprehensive security report"""
    
    report = {
        'period': {
            'start': logs['timestamp'].min(),
            'end': logs['timestamp'].max()
        },
        'summary': {
            'total_events': len(logs),
            'event_rate': len(logs) / (logs['timestamp'].max() - logs['timestamp'].min())
        },
        'authentication': analyze_authentication(logs),
        'anomalies': detect_anomalies(logs),
        'security_risks': identify_risks(logs)
    }
    
    return report
```

## Best Practices

1. **Data Quality**
   - Validate log format before analysis
   - Handle missing/corrupted entries
   - Normalize timestamps across systems

2. **Privacy**
   - Anonymize sensitive data
   - Follow data retention policies
   - Secure log storage

3. **Real-time Analysis**
   - Set up streaming analysis
   - Alert on critical events immediately
   - Use tools like ELK Stack or Splunk

4. **Historical Analysis**
   - Establish baselines
   - Trend analysis
   - Compare year-over-year

## References
- NIST Cybersecurity Framework
- OWASP Log Cheat Sheet
- ELK Stack Documentation
- Splunk Best Practices

## Last Updated
February 2026
