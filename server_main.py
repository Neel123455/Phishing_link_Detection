"""
URL Phishing Detector Server
Main Flask application for URL analysis
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import requests

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== URL Analysis Logic ====================

def is_valid_url(url_string: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url_string: URL to validate
        
    Returns:
        True if valid URL format, False otherwise
    """
    try:
        from urllib.parse import urlparse
        result = urlparse(url_string if url_string.startswith('http') else f'https://{url_string}')
        return all([result.scheme, result.netloc])
    except:
        return False


def normalize_url(url: str) -> str:
    """
    Normalize URL to standard format.
    
    Args:
        url: Raw URL input
        
    Returns:
        Normalized URL with https:// prefix
    """
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    return url


def parse_url(url_string: str) -> dict:
    """
    Parse URL into components.
    
    Args:
        url_string: URL to parse
        
    Returns:
        Dictionary with URL components
    """
    from urllib.parse import urlparse
    url = urlparse(url_string)
    return {
        'full': url.geturl(),
        'hostname': url.hostname or '',
        'protocol': url.scheme or '',
        'pathname': url.path or '',
        'search': url.query or ''
    }


def analyze_url(url_string: str) -> dict:
    """
    Perform 7-layer security analysis on URL.
    
    Args:
        url_string: URL to analyze
        
    Returns:
        Analysis results with verdict and risk score
    """
    parsed = parse_url(url_string)
    checks = []
    risk_score = 0

    # Check 1: SSL/TLS Encryption
    if parsed['protocol'] == 'https':
        checks.append({
            'name': 'SSL/TLS Encryption',
            'status': 'pass',
            'description': 'URL uses secure HTTPS protocol'
        })
    elif parsed['protocol'] == 'http':
        checks.append({
            'name': 'SSL/TLS Encryption',
            'status': 'fail',
            'description': 'URL uses unencrypted HTTP protocol'
        })
        risk_score += 15

    # Check 2: Subdomain Count
    hostname = parsed['hostname']
    domain_parts = hostname.split('.')
    
    if len(domain_parts) > 3:
        checks.append({
            'name': 'Subdomain Count',
            'status': 'warn',
            'description': 'Multiple subdomains may indicate suspicious hosting'
        })
        risk_score += 8
    else:
        checks.append({
            'name': 'Subdomain Count',
            'status': 'pass',
            'description': 'Normal subdomain structure'
        })

    # Check 3: IP Address Detection
    import re
    ip_regex = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    if re.match(ip_regex, hostname):
        checks.append({
            'name': 'IP Address Domain',
            'status': 'fail',
            'description': 'Direct IP addresses are often used in phishing'
        })
        risk_score += 20
    else:
        checks.append({
            'name': 'IP Address Domain',
            'status': 'pass',
            'description': 'Uses standard domain name'
        })

    # Check 4: Domain Length
    if hostname.length < 4:
        checks.append({
            'name': 'Domain Length',
            'status': 'warn',
            'description': 'Very short domain names are uncommon'
        })
        risk_score += 5
    elif len(hostname) > 50:
        checks.append({
            'name': 'Domain Length',
            'status': 'warn',
            'description': 'Very long domain names may be suspicious'
        })
        risk_score += 5
    else:
        checks.append({
            'name': 'Domain Length',
            'status': 'pass',
            'description': 'Domain length appears normal'
        })

    # Check 5: Special Characters
    if re.search(r'[^\w.-]', hostname):
        checks.append({
            'name': 'Special Characters',
            'status': 'fail',
            'description': 'Domain contains suspicious special characters'
        })
        risk_score += 15
    else:
        checks.append({
            'name': 'Special Characters',
            'status': 'pass',
            'description': 'No suspicious characters in domain'
        })

    # Check 6: Suspicious Keywords
    suspicious_keywords = ['verify', 'confirm', 'update', 'login', 'urgent', 'click', 'secure', 'validate']
    url_lower = url_string.lower()
    found_keywords = [kw for kw in suspicious_keywords if kw in url_lower]
    
    if len(found_keywords) >= 2:
        checks.append({
            'name': 'Suspicious Keywords',
            'status': 'warn',
            'description': f'Found {len(found_keywords)} common phishing keywords'
        })
        risk_score += len(found_keywords) * 3
    elif len(found_keywords) > 0:
        checks.append({
            'name': 'Suspicious Keywords',
            'status': 'warn',
            'description': f'Found {len(found_keywords)} common phishing keyword'
        })
        risk_score += 5
    else:
        checks.append({
            'name': 'Suspicious Keywords',
            'status': 'pass',
            'description': 'No common phishing keywords detected'
        })

    # Check 7: URL Length
    if len(parsed['full']) > 100:
        checks.append({
            'name': 'URL Length',
            'status': 'warn',
            'description': 'Very long URLs may contain hidden parameters'
        })
        risk_score += 8
    else:
        checks.append({
            'name': 'URL Length',
            'status': 'pass',
            'description': 'URL length is reasonable'
        })

    # Calculate safety score
    safety_score = max(0, 100 - risk_score)
    verdict = 'safe' if safety_score >= 75 else 'risky' if safety_score >= 50 else 'unsafe'

    return {
        'safety_score': safety_score,
        'risk_score': risk_score,
        'checks': checks,
        'verdict': verdict
    }


def check_global_database(url: str) -> dict:
    """
    Check URL against URLhaus global phishing database.
    
    Args:
        url: URL to check
        
    Returns:
        Dictionary with threat status
    """
    try:
        api_url = os.getenv('URLHAUS_API_URL', 'https://urlhaus-api.abuse.ch/v1/url/')
        response = requests.post(api_url, data={'url': url}, timeout=5)
        data = response.json()
        
        if data.get('query_status') == 'ok' and data.get('result') != 'not_found':
            return {
                'is_phishing': True,
                'threat': data.get('result', 'malware'),
                'last_analysis': data.get('last_analysis_date', 'Unknown')
            }
        return {'is_phishing': False}
    except Exception as e:
        logger.error(f"URLhaus API error: {str(e)}")
        return {'is_phishing': False, 'api_error': True}


# ==================== Flask Routes ====================

@app.route('/', methods=['GET'])
def index():
    """Serve main HTML page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    API endpoint to analyze URL.
    
    POST body:
        {
            "url": "https://example.com"
        }
    
    Returns:
        JSON with analysis results
    """
    try:
        data = request.get_json()
        url = data.get('url', '').strip()

        # Validate input
        if not url:
            return jsonify({
                'status': 'error',
                'error': 'Please enter a URL'
            }), 400

        if not is_valid_url(url):
            return jsonify({
                'status': 'error',
                'error': 'Invalid URL format'
            }), 400

        # Normalize URL
        normalized_url = normalize_url(url)
        logger.info(f"Analyzing URL: {normalized_url}")

        # Perform local analysis
        analysis = analyze_url(normalized_url)

        # Check global database
        threat_check = check_global_database(normalized_url)

        if threat_check.get('is_phishing'):
            analysis['risk_score'] += 50
            analysis['safety_score'] = max(0, 100 - analysis['risk_score'])
            analysis['verdict'] = 'unsafe'
            analysis['checks'].insert(0, {
                'name': 'Global Threat Database',
                'status': 'fail',
                'description': f"⚠️ URL detected in abuse.ch malicious database ({threat_check.get('threat')})"
            })
        elif not threat_check.get('api_error'):
            analysis['checks'].insert(0, {
                'name': 'Global Threat Database',
                'status': 'pass',
                'description': '✓ URL verified clean in global malicious database'
            })

        return jsonify({
            'status': 'ok',
            'verdict': analysis['verdict'],
            'safety_score': analysis['safety_score'],
            'risk_score': analysis['risk_score'],
            'checks': analysis['checks'],
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error analyzing URL: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': f'Error during analysis: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get application statistics."""
    return jsonify({
        'status': 'ok',
        'app': 'URL Phishing Detector',
        'version': '1.0.0',
        'features': {
            'local_analysis': True,
            'global_database': True,
            'history_tracking': True,
            'batch_processing': False
        }
    })


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'status': 'error', 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    logger.error(f"Server error: {str(error)}")
    return jsonify({'status': 'error', 'error': 'Internal server error'}), 500


# ==================== Application Entry Point ====================

if __name__ == '__main__':
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    logger.info(f"Starting phishing detector on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
