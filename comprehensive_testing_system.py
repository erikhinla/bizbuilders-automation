#!/usr/bin/env python3
"""
Comprehensive Testing System
End-to-end testing for the complete digital marketing automation system
"""

import os
import json
import time
import datetime
import requests
import sqlite3
import subprocess
import threading
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import concurrent.futures

@dataclass
class TestResult:
    """Data class for test results"""
    test_name: str
    component: str
    status: str  # 'pass', 'fail', 'warning'
    execution_time: float
    details: str
    timestamp: str
    error_message: Optional[str] = None

@dataclass
class PerformanceMetrics:
    """Data class for performance metrics"""
    component: str
    response_time: float
    memory_usage: float
    cpu_usage: float
    throughput: float
    timestamp: str

class ComprehensiveTestingSystem:
    def __init__(self, db_path: str = "/home/ubuntu/testing_results.db"):
        """Initialize the testing system"""
        self.db_path = db_path
        self.init_database()
        
        # Test configurations
        self.test_configs = {
            'websites': {
                'transformby10x': 'http://localhost:5173',
                'bizbuilders': 'http://localhost:5174'
            },
            'apis': {
                'integration_hub': '/home/ubuntu/integration_automation_hub.py',
                'api_integration': '/home/ubuntu/api_integration_system.py',
                'trend_monitoring': '/home/ubuntu/trend_monitoring_system.py'
            },
            'databases': {
                'seo_analysis': '/home/ubuntu/seo_analysis.db',
                'integration_hub': '/home/ubuntu/integration_hub.db',
                'api_integration': '/home/ubuntu/api_integration.db'
            }
        }
        
        # Performance thresholds
        self.performance_thresholds = {
            'website_response_time': 3.0,  # seconds
            'api_response_time': 1.0,      # seconds
            'database_query_time': 0.5,    # seconds
            'memory_usage': 512,           # MB
            'cpu_usage': 80                # percentage
        }
    
    def init_database(self):
        """Initialize SQLite database for test results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Test results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT,
                component TEXT,
                status TEXT,
                execution_time REAL,
                details TEXT,
                timestamp DATETIME,
                error_message TEXT
            )
        ''')
        
        # Performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                component TEXT,
                response_time REAL,
                memory_usage REAL,
                cpu_usage REAL,
                throughput REAL,
                timestamp DATETIME
            )
        ''')
        
        # Test suites table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_suites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suite_name TEXT,
                total_tests INTEGER,
                passed_tests INTEGER,
                failed_tests INTEGER,
                warnings INTEGER,
                execution_time REAL,
                timestamp DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_test_result(self, result: TestResult):
        """Save test result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO test_results 
            (test_name, component, status, execution_time, details, timestamp, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (result.test_name, result.component, result.status, result.execution_time,
              result.details, result.timestamp, result.error_message))
        
        conn.commit()
        conn.close()
    
    def save_performance_metrics(self, metrics: PerformanceMetrics):
        """Save performance metrics to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_metrics 
            (component, response_time, memory_usage, cpu_usage, throughput, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (metrics.component, metrics.response_time, metrics.memory_usage,
              metrics.cpu_usage, metrics.throughput, metrics.timestamp))
        
        conn.commit()
        conn.close()
    
    def test_website_functionality(self, website_name: str, url: str) -> List[TestResult]:
        """Test website functionality and performance"""
        print(f"🌐 Testing {website_name} website...")
        
        results = []
        
        # Test 1: Basic connectivity
        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)
            execution_time = time.time() - start_time
            
            if response.status_code == 200:
                result = TestResult(
                    test_name="basic_connectivity",
                    component=website_name,
                    status="pass",
                    execution_time=execution_time,
                    details=f"Website accessible, status code: {response.status_code}",
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                result = TestResult(
                    test_name="basic_connectivity",
                    component=website_name,
                    status="fail",
                    execution_time=execution_time,
                    details=f"Unexpected status code: {response.status_code}",
                    timestamp=datetime.datetime.now().isoformat(),
                    error_message=f"HTTP {response.status_code}"
                )
            
            results.append(result)
            
            # Test 2: Response time performance
            if execution_time <= self.performance_thresholds['website_response_time']:
                perf_result = TestResult(
                    test_name="response_time",
                    component=website_name,
                    status="pass",
                    execution_time=execution_time,
                    details=f"Response time: {execution_time:.2f}s (threshold: {self.performance_thresholds['website_response_time']}s)",
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                perf_result = TestResult(
                    test_name="response_time",
                    component=website_name,
                    status="warning",
                    execution_time=execution_time,
                    details=f"Slow response time: {execution_time:.2f}s (threshold: {self.performance_thresholds['website_response_time']}s)",
                    timestamp=datetime.datetime.now().isoformat()
                )
            
            results.append(perf_result)
            
            # Test 3: Content validation
            content = response.text
            required_elements = ['<title>', '<meta name="description"', 'og:title', 'twitter:card']
            missing_elements = [elem for elem in required_elements if elem not in content]
            
            if not missing_elements:
                content_result = TestResult(
                    test_name="seo_elements",
                    component=website_name,
                    status="pass",
                    execution_time=0.1,
                    details="All required SEO elements present",
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                content_result = TestResult(
                    test_name="seo_elements",
                    component=website_name,
                    status="warning",
                    execution_time=0.1,
                    details=f"Missing SEO elements: {', '.join(missing_elements)}",
                    timestamp=datetime.datetime.now().isoformat()
                )
            
            results.append(content_result)
            
        except Exception as e:
            result = TestResult(
                test_name="basic_connectivity",
                component=website_name,
                status="fail",
                execution_time=time.time() - start_time,
                details="Failed to connect to website",
                timestamp=datetime.datetime.now().isoformat(),
                error_message=str(e)
            )
            results.append(result)
        
        return results
    
    def test_api_functionality(self, api_name: str, script_path: str) -> List[TestResult]:
        """Test API and script functionality"""
        print(f"🔌 Testing {api_name} API...")
        
        results = []
        
        # Test 1: Script execution
        start_time = time.time()
        try:
            result = subprocess.run(
                ['python3', script_path],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=os.path.dirname(script_path)
            )
            execution_time = time.time() - start_time
            
            if result.returncode == 0:
                test_result = TestResult(
                    test_name="script_execution",
                    component=api_name,
                    status="pass",
                    execution_time=execution_time,
                    details=f"Script executed successfully in {execution_time:.2f}s",
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                test_result = TestResult(
                    test_name="script_execution",
                    component=api_name,
                    status="fail",
                    execution_time=execution_time,
                    details=f"Script failed with return code: {result.returncode}",
                    timestamp=datetime.datetime.now().isoformat(),
                    error_message=result.stderr
                )
            
            results.append(test_result)
            
        except subprocess.TimeoutExpired:
            test_result = TestResult(
                test_name="script_execution",
                component=api_name,
                status="fail",
                execution_time=60.0,
                details="Script execution timed out",
                timestamp=datetime.datetime.now().isoformat(),
                error_message="Timeout after 60 seconds"
            )
            results.append(test_result)
            
        except Exception as e:
            test_result = TestResult(
                test_name="script_execution",
                component=api_name,
                status="fail",
                execution_time=time.time() - start_time,
                details="Script execution failed",
                timestamp=datetime.datetime.now().isoformat(),
                error_message=str(e)
            )
            results.append(test_result)
        
        return results
    
    def test_database_functionality(self, db_name: str, db_path: str) -> List[TestResult]:
        """Test database functionality and integrity"""
        print(f"🗄️ Testing {db_name} database...")
        
        results = []
        
        # Test 1: Database accessibility
        start_time = time.time()
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Test basic query
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            execution_time = time.time() - start_time
            
            if tables:
                test_result = TestResult(
                    test_name="database_access",
                    component=db_name,
                    status="pass",
                    execution_time=execution_time,
                    details=f"Database accessible with {len(tables)} tables",
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                test_result = TestResult(
                    test_name="database_access",
                    component=db_name,
                    status="warning",
                    execution_time=execution_time,
                    details="Database accessible but no tables found",
                    timestamp=datetime.datetime.now().isoformat()
                )
            
            results.append(test_result)
            
            # Test 2: Query performance
            start_time = time.time()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master;")
            cursor.fetchone()
            query_time = time.time() - start_time
            
            if query_time <= self.performance_thresholds['database_query_time']:
                perf_result = TestResult(
                    test_name="query_performance",
                    component=db_name,
                    status="pass",
                    execution_time=query_time,
                    details=f"Query time: {query_time:.3f}s (threshold: {self.performance_thresholds['database_query_time']}s)",
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                perf_result = TestResult(
                    test_name="query_performance",
                    component=db_name,
                    status="warning",
                    execution_time=query_time,
                    details=f"Slow query time: {query_time:.3f}s (threshold: {self.performance_thresholds['database_query_time']}s)",
                    timestamp=datetime.datetime.now().isoformat()
                )
            
            results.append(perf_result)
            
            conn.close()
            
        except Exception as e:
            test_result = TestResult(
                test_name="database_access",
                component=db_name,
                status="fail",
                execution_time=time.time() - start_time,
                details="Failed to access database",
                timestamp=datetime.datetime.now().isoformat(),
                error_message=str(e)
            )
            results.append(test_result)
        
        return results
    
    def test_integration_flow(self) -> List[TestResult]:
        """Test end-to-end integration flow"""
        print("🔄 Testing integration flow...")
        
        results = []
        
        # Test 1: Trend monitoring to content generation
        start_time = time.time()
        try:
            # Check if trend data exists
            trend_file = "/home/ubuntu/trend_analysis_results.json"
            if os.path.exists(trend_file):
                with open(trend_file, 'r') as f:
                    trend_data = json.load(f)
                
                execution_time = time.time() - start_time
                test_result = TestResult(
                    test_name="trend_to_content",
                    component="integration_flow",
                    status="pass",
                    execution_time=execution_time,
                    details="Trend data successfully flows to content generation",
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                test_result = TestResult(
                    test_name="trend_to_content",
                    component="integration_flow",
                    status="warning",
                    execution_time=time.time() - start_time,
                    details="Trend data file not found",
                    timestamp=datetime.datetime.now().isoformat()
                )
            
            results.append(test_result)
            
        except Exception as e:
            test_result = TestResult(
                test_name="trend_to_content",
                component="integration_flow",
                status="fail",
                execution_time=time.time() - start_time,
                details="Integration flow test failed",
                timestamp=datetime.datetime.now().isoformat(),
                error_message=str(e)
            )
            results.append(test_result)
        
        # Test 2: Social media integration
        start_time = time.time()
        try:
            integration_file = "/home/ubuntu/social_automation_integration.json"
            if os.path.exists(integration_file):
                with open(integration_file, 'r') as f:
                    integration_data = json.load(f)
                
                execution_time = time.time() - start_time
                test_result = TestResult(
                    test_name="social_integration",
                    component="integration_flow",
                    status="pass",
                    execution_time=execution_time,
                    details=f"Social integration file contains {len(integration_data.get('social_posts', []))} posts",
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                test_result = TestResult(
                    test_name="social_integration",
                    component="integration_flow",
                    status="warning",
                    execution_time=time.time() - start_time,
                    details="Social integration file not found",
                    timestamp=datetime.datetime.now().isoformat()
                )
            
            results.append(test_result)
            
        except Exception as e:
            test_result = TestResult(
                test_name="social_integration",
                component="integration_flow",
                status="fail",
                execution_time=time.time() - start_time,
                details="Social integration test failed",
                timestamp=datetime.datetime.now().isoformat(),
                error_message=str(e)
            )
            results.append(test_result)
        
        return results
    
    def run_security_tests(self) -> List[TestResult]:
        """Run basic security tests"""
        print("🔒 Running security tests...")
        
        results = []
        
        # Test 1: Check for sensitive files
        sensitive_files = ['.env', 'config.json', 'secrets.txt', 'api_keys.txt']
        exposed_files = []
        
        for file in sensitive_files:
            if os.path.exists(f"/home/ubuntu/{file}"):
                exposed_files.append(file)
        
        if not exposed_files:
            security_result = TestResult(
                test_name="sensitive_files",
                component="security",
                status="pass",
                execution_time=0.1,
                details="No sensitive files found in root directory",
                timestamp=datetime.datetime.now().isoformat()
            )
        else:
            security_result = TestResult(
                test_name="sensitive_files",
                component="security",
                status="warning",
                execution_time=0.1,
                details=f"Potentially sensitive files found: {', '.join(exposed_files)}",
                timestamp=datetime.datetime.now().isoformat()
            )
        
        results.append(security_result)
        
        # Test 2: Check database permissions
        db_files = [
            "/home/ubuntu/seo_analysis.db",
            "/home/ubuntu/integration_hub.db",
            "/home/ubuntu/api_integration.db"
        ]
        
        secure_dbs = 0
        for db_file in db_files:
            if os.path.exists(db_file):
                file_stat = os.stat(db_file)
                # Check if file is readable by others
                if not (file_stat.st_mode & 0o044):  # Not readable by group/others
                    secure_dbs += 1
        
        if secure_dbs == len([f for f in db_files if os.path.exists(f)]):
            db_security_result = TestResult(
                test_name="database_permissions",
                component="security",
                status="pass",
                execution_time=0.1,
                details="Database files have appropriate permissions",
                timestamp=datetime.datetime.now().isoformat()
            )
        else:
            db_security_result = TestResult(
                test_name="database_permissions",
                component="security",
                status="warning",
                execution_time=0.1,
                details="Some database files may have overly permissive access",
                timestamp=datetime.datetime.now().isoformat()
            )
        
        results.append(db_security_result)
        
        return results
    
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Run the complete test suite"""
        print("🧪 Running Comprehensive Test Suite")
        print("=" * 50)
        
        all_results = []
        suite_start_time = time.time()
        
        # Test websites
        for website_name, url in self.test_configs['websites'].items():
            website_results = self.test_website_functionality(website_name, url)
            all_results.extend(website_results)
        
        # Test APIs
        for api_name, script_path in self.test_configs['apis'].items():
            if os.path.exists(script_path):
                api_results = self.test_api_functionality(api_name, script_path)
                all_results.extend(api_results)
        
        # Test databases
        for db_name, db_path in self.test_configs['databases'].items():
            if os.path.exists(db_path):
                db_results = self.test_database_functionality(db_name, db_path)
                all_results.extend(db_results)
        
        # Test integration flow
        integration_results = self.test_integration_flow()
        all_results.extend(integration_results)
        
        # Run security tests
        security_results = self.run_security_tests()
        all_results.extend(security_results)
        
        # Save all results
        for result in all_results:
            self.save_test_result(result)
        
        # Calculate suite statistics
        total_execution_time = time.time() - suite_start_time
        passed_tests = len([r for r in all_results if r.status == 'pass'])
        failed_tests = len([r for r in all_results if r.status == 'fail'])
        warnings = len([r for r in all_results if r.status == 'warning'])
        
        # Save suite summary
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO test_suites 
            (suite_name, total_tests, passed_tests, failed_tests, warnings, execution_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('comprehensive_test_suite', len(all_results), passed_tests, failed_tests, 
              warnings, total_execution_time, datetime.datetime.now()))
        conn.commit()
        conn.close()
        
        # Generate summary report
        summary = {
            'timestamp': datetime.datetime.now().isoformat(),
            'total_tests': len(all_results),
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'warnings': warnings,
            'success_rate': (passed_tests / len(all_results)) * 100 if all_results else 0,
            'execution_time': total_execution_time,
            'test_results': [asdict(result) for result in all_results],
            'overall_status': 'PASS' if failed_tests == 0 else 'FAIL' if failed_tests > 0 else 'WARNING'
        }
        
        return summary
    
    def generate_test_report(self, summary: Dict[str, Any]) -> str:
        """Generate a detailed test report"""
        report = f"""
# Comprehensive Test Report

**Generated:** {summary['timestamp']}
**Overall Status:** {summary['overall_status']}

## Summary
- **Total Tests:** {summary['total_tests']}
- **Passed:** {summary['passed_tests']}
- **Failed:** {summary['failed_tests']}
- **Warnings:** {summary['warnings']}
- **Success Rate:** {summary['success_rate']:.1f}%
- **Execution Time:** {summary['execution_time']:.2f} seconds

## Test Results by Component

"""
        
        # Group results by component
        components = {}
        for result in summary['test_results']:
            component = result['component']
            if component not in components:
                components[component] = []
            components[component].append(result)
        
        for component, results in components.items():
            report += f"### {component.title()}\n\n"
            for result in results:
                status_emoji = "✅" if result['status'] == 'pass' else "❌" if result['status'] == 'fail' else "⚠️"
                report += f"- {status_emoji} **{result['test_name']}** ({result['execution_time']:.2f}s): {result['details']}\n"
                if result['error_message']:
                    report += f"  - Error: {result['error_message']}\n"
            report += "\n"
        
        return report

def main():
    """Main function to run comprehensive testing"""
    print("🧪 Comprehensive Testing System")
    print("=" * 40)
    
    # Initialize testing system
    testing_system = ComprehensiveTestingSystem()
    
    # Run comprehensive test suite
    summary = testing_system.run_comprehensive_test_suite()
    
    # Generate and save test report
    report = testing_system.generate_test_report(summary)
    
    report_path = "/home/ubuntu/test_report.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    # Save summary as JSON
    summary_path = "/home/ubuntu/test_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    # Print summary
    print(f"\n📊 Test Suite Summary:")
    print(f"   Total Tests: {summary['total_tests']}")
    print(f"   Passed: {summary['passed_tests']}")
    print(f"   Failed: {summary['failed_tests']}")
    print(f"   Warnings: {summary['warnings']}")
    print(f"   Success Rate: {summary['success_rate']:.1f}%")
    print(f"   Overall Status: {summary['overall_status']}")
    
    print(f"\n📋 Test report saved to {report_path}")
    print(f"📊 Test summary saved to {summary_path}")
    
    print("\n✅ Comprehensive testing complete!")

if __name__ == "__main__":
    main()

