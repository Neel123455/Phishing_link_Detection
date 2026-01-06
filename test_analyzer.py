"""
Unit tests for URL analyzer
"""

import pytest
from server import is_valid_url, normalize_url, parse_url, analyze_url


class TestURLValidation:
    """Test URL validation function."""
    
    def test_valid_https_url(self):
        """Test validation of valid HTTPS URL."""
        assert is_valid_url("https://google.com") == True
    
    def test_valid_http_url(self):
        """Test validation of valid HTTP URL."""
        assert is_valid_url("http://example.com") == True
    
    def test_valid_url_without_protocol(self):
        """Test validation of URL without protocol."""
        assert is_valid_url("google.com") == True
    
    def test_invalid_url(self):
        """Test validation of invalid URL."""
        assert is_valid_url("not a url") == False
    
    def test_empty_url(self):
        """Test validation of empty URL."""
        assert is_valid_url("") == False


class TestURLNormalization:
    """Test URL normalization function."""
    
    def test_normalize_adds_https(self):
        """Test that normalize adds https:// prefix."""
        result = normalize_url("google.com")
        assert result == "https://google.com"
    
    def test_normalize_preserves_https(self):
        """Test that normalize preserves https."""
        result = normalize_url("https://google.com")
        assert result == "https://google.com"
    
    def test_normalize_preserves_http(self):
        """Test that normalize preserves http."""
        result = normalize_url("http://google.com")
        assert result == "http://google.com"


class TestURLParsing:
    """Test URL parsing function."""
    
    def test_parse_complete_url(self):
        """Test parsing of complete URL."""
        result = parse_url("https://subdomain.example.com/path?query=1")
        assert result['protocol'] == 'https'
        assert result['hostname'] == 'subdomain.example.com'
        assert result['pathname'] == '/path'
        assert result['search'] == 'query=1'
    
    def test_parse_simple_url(self):
        """Test parsing of simple URL."""
        result = parse_url("https://example.com")
        assert result['protocol'] == 'https'
        assert result['hostname'] == 'example.com'


class TestURLAnalysis:
    """Test URL analysis function."""
    
    def test_analyze_safe_https_url(self):
        """Test analysis of safe HTTPS URL."""
        result = analyze_url("https://google.com")
        assert result['verdict'] == 'safe'
        assert result['safety_score'] >= 75
        assert result['checks'] is not None
        assert len(result['checks']) == 7
    
    def test_analyze_unsafe_http_url(self):
        """Test analysis of unsafe HTTP URL."""
        result = analyze_url("http://example.com")
        assert result['verdict'] in ['risky', 'unsafe']
        assert result['risk_score'] > 0
    
    def test_analyze_phishing_keywords(self):
        """Test analysis detects phishing keywords."""
        result = analyze_url("https://verify-account-urgent.com")
        # Should have detected suspicious keywords
        suspicious = [check for check in result['checks'] 
                     if 'keyword' in check['name'].lower()]
        assert len(suspicious) > 0
    
    def test_analyze_ip_address(self):
        """Test analysis detects IP addresses."""
        result = analyze_url("https://192.168.1.1")
        # Should detect IP address
        ip_check = [check for check in result['checks'] 
                   if 'IP' in check['name']]
        assert len(ip_check) > 0
    
    def test_analyze_long_url(self):
        """Test analysis detects long URLs."""
        long_url = "https://example.com/" + "a" * 150
        result = analyze_url(long_url)
        # Should detect long URL
        assert result['risk_score'] > 0
    
    def test_safety_score_calculation(self):
        """Test safety score is calculated correctly."""
        result = analyze_url("https://google.com")
        assert 0 <= result['safety_score'] <= 100
        assert result['safety_score'] + result['risk_score'] <= 100


class TestVerdictDetermination:
    """Test verdict determination logic."""
    
    def test_safe_verdict(self):
        """Test safe verdict for high safety score."""
        result = analyze_url("https://google.com")
        assert result['verdict'] == 'safe'
    
    def test_unsafe_verdict(self):
        """Test unsafe verdict for low safety score."""
        result = analyze_url("http://192.168.1.1/verify-account-urgent-confirm-login-click-here-validate-secure")
        assert result['verdict'] in ['unsafe', 'risky']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
