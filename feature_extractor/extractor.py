# feature_extractor/extractor.py
import re
import whois
import ssl
import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

def extract_url_features(url: str) -> dict:
    features = {}
    parsed = urlparse(url)
    features['url_length'] = len(url)
    features['n_dots'] = url.count('.')
    features['has_ip'] = bool(re.match(r'\d+\.\d+\.\d+\.\d+', parsed.netloc))
    # WHOIS age (days since creation)
    try:
        w = whois.whois(parsed.netloc)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        features['domain_age_days'] = (datetime.now() - creation).days
    except Exception:
        features['domain_age_days'] = -1
    # SSL cert checks
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=parsed.netloc) as s:
            s.connect((parsed.netloc, 443))
            cert = s.getpeercert()
            features['ssl_valid_from'] = (datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z'))
            features['ssl_valid_to']   = (datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z'))
            features['cert_lifetime_days'] = (features['ssl_valid_to'] - features['ssl_valid_from']).days
    except Exception:
        features['cert_lifetime_days'] = -1
    return features

def extract_html_features(url: str) -> dict:
    r = requests.get(url, timeout=5)
    soup = BeautifulSoup(r.text, 'html.parser')
    features = {
        'n_links': len(soup.find_all('a')),
        'n_forms': len(soup.find_all('form')),
        'text_length': len(soup.get_text()),
    }
    return features

def extract_all(url: str) -> dict:
    feats = extract_url_features(url)
    try:
        feats.update(extract_html_features(url))
    except:
        feats.update({'n_links':0,'n_forms':0,'text_length':0})
    return feats
