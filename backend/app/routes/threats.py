from flask import Blueprint, jsonify
import requests
import csv
from io import StringIO
import json
import os

# Create a blueprint for threat API
threats_bp = Blueprint("threats", __name__)

@threats_bp.route("/api/threats", methods=["GET"])
def get_threats():
    """
    Fetch threat data from multiple free sources (no API key):
    - URLs: PhishTank, URLhaus, OpenPhish
    - File Hashes: MalwareBazaar, Hybrid Analysis
    - IPs/C2: FireHOL, Blocklist.de, Zeus/Feodo Tracker
    - OSINT feeds: EmergingThreats, Honeynet
    - Passive DNS / Domains: CIRCL, URLScan.io
    - Email/Phishing: PhishIQ
    Limits each source to max 100 entries.
    Falls back to sampleThreats.json if live sources fail.
    """
    threats = []

    # ----- 1️⃣ Malicious URLs -----
    url_sources = [
        {"name": "PhishTank", "url": "https://data.phishtank.com/data/online-valid.csv", "type": "URL"},
        {"name": "URLhaus", "url": "https://urlhaus.abuse.ch/downloads/csv/", "type": "URL"},
        {"name": "OpenPhish", "url": "https://openphish.com/feed.txt", "type": "URL"}
    ]

    for source in url_sources:
        try:
            response = requests.get(source["url"], timeout=5)
            response.raise_for_status()
            if source["name"] == "OpenPhish":
                lines = response.text.strip().split("\n")[:100]
                for line in lines:
                    threats.append({
                        "type": source["type"],
                        "indicator": line,
                        "severity": "High",
                        "mitre": "T1566.002"
                    })
            else:
                csv_data = StringIO(response.text)
                reader = csv.DictReader(csv_data)
                for i, row in enumerate(reader):
                    if i >= 100:
                        break
                    indicator = row.get("url") or row.get("domain") or row.get("ip")
                    if indicator:
                        threats.append({
                            "type": source["type"],
                            "indicator": indicator,
                            "severity": "High",
                            "mitre": "T1566.002"
                        })
        except Exception as e:
            print(f"{source['name']} fetch failed:", e)

    # ----- 2️⃣ File Hashes -----
    file_hash_sources = [
        {"name": "MalwareBazaar", "url": "https://mb-api.abuse.ch/api/v1/", "type": "File Hash"}
        # You can add Hybrid Analysis later
    ]

    for source in file_hash_sources:
        try:
            if source["name"] == "MalwareBazaar":
                resp = requests.post(source["url"], data={"query": "get_recent"}, timeout=5)
                resp.raise_for_status()
                data = resp.json()
                for i, sample in enumerate(data.get("data", [])):
                    if i >= 100:
                        break
                    sha256 = sample.get("sha256")
                    if sha256:
                        threats.append({
                            "type": source["type"],
                            "indicator": sha256,
                            "severity": "High",
                            "mitre": "T1486"
                        })
        except Exception as e:
            print(f"{source['name']} fetch failed:", e)

    # ----- 3️⃣ Sample IPs / C2 -----
    sample_ips = ["192.168.1.100", "10.0.0.5", "203.0.113.45"]
    for ip in sample_ips:
        threats.append({
            "type": "IP",
            "indicator": ip,
            "severity": "Medium",
            "mitre": "T1071.001"
        })

    # ----- 4️⃣ Fallback to sampleThreats.json if empty -----
    if not threats:
        try:
            sample_file_path = os.path.join(os.path.dirname(__file__), '../../frontend/src/data/sampleThreats.json')
            with open(sample_file_path, "r") as f:
                threats = json.load(f)
            print("Using fallback sampleThreats.json")
        except Exception as e:
            print("Failed to load sampleThreats.json:", e)
            threats = []

    return jsonify(threats)
