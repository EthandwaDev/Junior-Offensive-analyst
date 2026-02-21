"""
Security Log Analysis - Data Analytics Approach
Demonstrates anomaly detection and security insights from logs
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from collections import defaultdict
import json

class SecurityLogAnalyzer:
    """Analyze security logs for threats and anomalies"""
    
    def __init__(self):
        self.logs = None
        self.analysis_results = {}
    
    def parse_apache_logs(self, log_content):
        """Parse Apache web server logs"""
        # Apache log format: IP - - [timestamp] "METHOD URL PROTOCOL" STATUS SIZE "REFERER" "USER_AGENT"
        pattern = r'(\S+) - - \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\S+) "([^"]*)" "([^"]*)"'
        
        logs = []
        for line in log_content.strip().split('\n'):
            match = re.match(pattern, line)
            if match:
                logs.append({
                    'ip': match.group(1),
                    'timestamp': match.group(2),
                    'method': match.group(3),
                    'url': match.group(4),
                    'protocol': match.group(5),
                    'status': int(match.group(6)),
                    'size': match.group(7),
                    'referer': match.group(8),
                    'user_agent': match.group(9)
                })
        
        self.logs = pd.DataFrame(logs)
        self.logs['timestamp'] = pd.to_datetime(self.logs['timestamp'], 
                                               format='%d/%b/%Y:%H:%M:%S %z',
                                               errors='coerce')
        return self.logs
    
    def parse_auth_logs(self, log_content):
        """Parse authentication/syslog format logs"""
        # Syslog format: timestamp host service[pid]: message
        pattern = r'(\w+ +\d+ \d+:\d+:\d+) (\S+) (\S+)\[(\d+)\]: (.+)'
        
        logs = []
        for line in log_content.strip().split('\n'):
            match = re.match(pattern, line)
            if match:
                logs.append({
                    'timestamp': match.group(1),
                    'host': match.group(2),
                    'service': match.group(3),
                    'pid': match.group(4),
                    'message': match.group(5)
                })
        
        self.logs = pd.DataFrame(logs)
        return self.logs
    
    def detect_brute_force_attempts(self, threshold=5):
        """
        Detect brute force attacks:
        Multiple failed login attempts from same IP
        """
        if self.logs is None:
            return None
        
        # Look for 401/403 status codes (unauthorized/forbidden)
        failed_attempts = self.logs[self.logs['status'].isin([401, 403])]
        
        if len(failed_attempts) == 0:
            return pd.DataFrame()
        
        # Count attempts per IP
        ip_counts = failed_attempts.groupby('ip').agg({
            'ip': 'count',
            'timestamp': ['min', 'max']
        }).rename(columns={'ip': 'attempt_count'})
        
        # Filter IPs with attempts >= threshold
        suspicious = ip_counts[ip_counts['attempt_count'] >= threshold]
        
        return suspicious.reset_index()
    
    def detect_sql_injection_attempts(self):
        """Detect potential SQL injection attempts"""
        if self.logs is None:
            return None
        
        # SQL injection patterns
        sql_patterns = [
            r"union.*select",
            r"select.*from",
            r"insert.*into",
            r"delete.*from",
            r"drop.*table",
            r"update.*set",
            r"or\s+1\s*=\s*1",
            r"';.*--",
            r"/\*.*\*/",
            r"xp_",
            r"sp_"
        ]
        
        # Combine patterns
        combined_pattern = '|'.join(sql_patterns)
        
        # Search in URL and parameters
        suspicious = self.logs[
            self.logs['url'].str.contains(combined_pattern, case=False, na=False, regex=True) |
            self.logs['referer'].str.contains(combined_pattern, case=False, na=False, regex=True)
        ]
        
        return suspicious[['timestamp', 'ip', 'url', 'status']]
    
    def detect_unusual_traffic_volume(self, window_minutes=5, threshold_zscore=3):
        """
        Detect unusual traffic volumes (potential DDoS)
        Using z-score statistical analysis
        """
        if self.logs is None or len(self.logs) == 0:
            return None
        
        # Group by time window
        self.logs['time_bucket'] = pd.to_datetime(self.logs['timestamp']).dt.floor(f'{window_minutes}T')
        traffic = self.logs.groupby('time_bucket').size()
        
        # Calculate z-scores
        mean = traffic.mean()
        std = traffic.std()
        z_scores = np.abs((traffic - mean) / std)
        
        # Find anomalies
        anomalies = traffic[z_scores > threshold_zscore]
        
        results = pd.DataFrame({
            'time_bucket': anomalies.index,
            'request_count': anomalies.values,
            'z_score': z_scores[z_scores > threshold_zscore].values
        })
        
        return results
    
    def analyze_status_codes(self):
        """Analyze HTTP status code distribution"""
        if self.logs is None:
            return None
        
        status_dist = self.logs['status'].value_counts().sort_index()
        
        summary = {
            'status_distribution': status_dist.to_dict(),
            '2xx_success': len(self.logs[self.logs['status'].between(200, 299)]),
            '4xx_errors': len(self.logs[self.logs['status'].between(400, 499)]),
            '5xx_errors': len(self.logs[self.logs['status'].between(500, 599)]),
            'error_rate': (len(self.logs[~self.logs['status'].between(200, 299)]) / len(self.logs)) * 100
        }
        
        return summary
    
    def detect_suspicious_user_agents(self):
        """Detect suspicious or automated user agents"""
        if self.logs is None:
            return None
        
        suspicious_agents = [
            r'bot',
            r'crawler',
            r'spider',
            r'sqlmap',
            r'nikto',
            r'nmap',
            r'masscan',
            r'nessus',
            r'qualys',
            r'burp',
            r'zap'
        ]
        
        combined_pattern = '|'.join(suspicious_agents)
        
        suspicious = self.logs[
            self.logs['user_agent'].str.contains(combined_pattern, case=False, na=False, regex=True)
        ]
        
        return suspicious[['timestamp', 'ip', 'user_agent', 'url']].head(20)
    
    def analyze_top_sources(self, top_n=10):
        """Analyze top source IPs"""
        if self.logs is None:
            return None
        
        top_ips = self.logs.groupby('ip').agg({
            'ip': 'count',
            'status': lambda x: (x >= 400).sum()  # Count errors
        }).rename(columns={'ip': 'total_requests', 'status': 'error_count'})
        
        top_ips = top_ips.sort_values('total_requests', ascending=False).head(top_n)
        
        return top_ips
    
    def detect_path_traversal_attempts(self):
        """Detect path traversal/directory traversal attempts"""
        if self.logs is None:
            return None
        
        traversal_patterns = [
            r'\.\.',
            r'\.\./',
            r'%2e%2e',
            r'%252e',
            r'\.\.\\',
            r'file://',
            r'etc/passwd',
            r'windows/system32'
        ]
        
        combined_pattern = '|'.join(traversal_patterns)
        
        suspicious = self.logs[
            self.logs['url'].str.contains(combined_pattern, case=False, na=False, regex=True)
        ]
        
        return suspicious[['timestamp', 'ip', 'url', 'status']]
    
    def generate_report(self):
        """Generate comprehensive security report"""
        if self.logs is None:
            return {
                'status': 'error',
                'message': 'No logs loaded'
            }
        
        report = {
            'summary': {
                'total_events': len(self.logs),
                'time_period': {
                    'start': str(self.logs['timestamp'].min()),
                    'end': str(self.logs['timestamp'].max())
                },
                'unique_sources': self.logs['ip'].nunique()
            },
            'findings': {
                'brute_force_attempts': len(self.detect_brute_force_attempts()),
                'sql_injection_attempts': len(self.detect_sql_injection_attempts()),
                'path_traversal_attempts': len(self.detect_path_traversal_attempts()),
                'suspicious_user_agents': len(self.detect_suspicious_user_agents()),
                'traffic_anomalies': len(self.detect_unusual_traffic_volume())
            },
            'statistics': self.analyze_status_codes(),
            'top_sources': self.analyze_top_sources().to_dict()
        }
        
        return report


def main():
    """Example usage of SecurityLogAnalyzer"""
    
    analyzer = SecurityLogAnalyzer()
    
    # Sample logs for demonstration
    sample_logs = """
192.168.1.100 - - [20/Feb/2026:10:15:30 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
192.168.1.101 - - [20/Feb/2026:10:15:31 +0000] "POST /login HTTP/1.1" 401 567 "-" "curl/7.68.0"
192.168.1.101 - - [20/Feb/2026:10:15:32 +0000] "POST /login HTTP/1.1" 401 567 "-" "curl/7.68.0"
192.168.1.101 - - [20/Feb/2026:10:15:33 +0000] "POST /login HTTP/1.1" 401 567 "-" "curl/7.68.0"
192.168.1.102 - - [20/Feb/2026:10:15:35 +0000] "GET /product?id=1' OR '1'='1 HTTP/1.1" 200 2345 "-" "Mozilla/5.0"
192.168.1.103 - - [20/Feb/2026:10:15:40 +0000] "GET /admin/../../etc/passwd HTTP/1.1" 404 0 "-" "sqlmap/1.4.9"
192.168.1.100 - - [20/Feb/2026:10:15:50 +0000] "GET /api/users HTTP/1.1" 200 5678 "-" "Mozilla/5.0"
    """.strip()
    
    # Parse logs
    print("Parsing logs...")
    analyzer.parse_apache_logs(sample_logs)
    
    # Generate report
    print("\n=== SECURITY LOG ANALYSIS REPORT ===\n")
    report = analyzer.generate_report()
    
    print("Summary:")
    print(f"  Total Events: {report['summary']['total_events']}")
    print(f"  Unique Sources: {report['summary']['unique_sources']}")
    
    print("\nSecurity Findings:")
    for finding, count in report['findings'].items():
        if count > 0:
            print(f"  ⚠️  {finding}: {count}")
    
    print("\nStatus Code Analysis:")
    stats = report['statistics']
    print(f"  Success (2xx): {stats['2xx_success']}")
    print(f"  Client Errors (4xx): {stats['4xx_errors']}")
    print(f"  Server Errors (5xx): {stats['5xx_errors']}")
    print(f"  Error Rate: {stats['error_rate']:.2f}%")
    
    # Export report
    with open('/tmp/security_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print("\n✓ Report exported to /tmp/security_report.json")


if __name__ == '__main__':
    main()
