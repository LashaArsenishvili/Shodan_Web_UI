#!/usr/bin/env python3
"""
Shodan Explorer Pro — Georgian / English bilingual UI
Starts in Georgian (KA), toggle to English (EN) via header button.
"""

import os
import json
from datetime import datetime
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State, dash_table, ctx, ALL
import dash_bootstrap_components as dbc

# ====================== AUTO-LOAD API KEY ======================
def load_api_key_from_file(path="api.txt"):
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
    except FileNotFoundError:
        pass
    return ""

DEFAULT_API_KEY = load_api_key_from_file()

# ====================== TRANSLATIONS ======================
TRANSLATIONS = {
    "ka": {
        # Header
        "brand_main": "შოდანი ",
        "brand_sub": "მკვლევარი",
        "brand_pro": " პრო",
        "lang_btn": "🇬🇧 EN",
        # Sidebar labels
        "api_key": "API გასაღები",
        "api_placeholder": "შოდანის API გასაღები…",
        "verify_btn": "✓ გასაღების შემოწმება",
        "search_query": "საძიებო მოთხოვნა",
        "query_placeholder": "apache port:80 country:GE\n(დატოვეთ ცარიელი ფილტრებისთვის)",
        "search_btn": "⌕  ძიება",
        "count_btn": "≡  მხოლოდ დათვლა",
        "filters_label": "ფილტრები",
        # Status bar
        "ready_status": "მზადაა — შეიყვანეთ API გასაღები და შექმენით მოთხოვნა",
        # Tabs
        "tab_charts": "◈  გრაფიკები",
        "tab_results": "⊞  შედეგები",
        "tab_map": "🌍  რუქა",
        "tab_host": "⚡  ჰოსტის ძიება",
        # Empty states
        "empty_charts": "ჩაატარეთ ძიება გრაფიკების სანახავად",
        "empty_results": "ჩაატარეთ ძიება შედეგების სანახავად",
        "empty_count": "მხოლოდ დათვლის რეჟიმი — შედეგის სტრიქონები არ არის",
        "empty_map": "ჩაატარეთ ძიება რუქის სანახავად",
        "empty_geo": "გეო-კოორდინატები შედეგებში არ არის",
        "no_facets": "ფასეტის მონაცემები არ დაბრუნდა — სცადეთ ფართო მოთხოვნა",
        # Host lookup
        "host_lookup_label": "ჰოსტის ძიება",
        "host_ip_placeholder": "შეიყვანეთ IP მისამართი (მაგ. 8.8.8.8)",
        "lookup_btn": "ძიება",
        "provide_key_ip": "მიუთითეთ API გასაღები და IP მისამართი",
        # Host detail
        "overview": "მიმოხილვა",
        "vulnerabilities": "დაუცველობები",
        "services": "სერვისები",
        "no_banner": "ბანერი არ არის",
        "ip": "IP",
        "organization": "ორგანიზაცია",
        "country": "ქვეყანა",
        "city": "ქალაქი",
        "region": "რეგიონი",
        "asn": "ASN",
        "os": "ოპ. სისტემა",
        "hostnames": "ჰოსტის სახელები",
        "tags": "თეგები",
        "open_ports": "ღია პორტები",
        "last_updated": "ბოლო განახლება",
        # Table
        "hosts_page": "ჰოსტი ამ გვერდზე",
        "export_csv": "↓ CSV ექსპორტი",
        # Charts
        "top_countries": "ტოპ ქვეყნები",
        "top_ports": "ტოპ პორტები",
        "top_orgs": "ტოპ ორგანიზაციები",
        "top_products": "ტოპ პროდუქტები",
        "op_systems": "ოპ. სისტემები",
        # Status messages
        "enter_key_first": "⚠  პირველ რიგში შეიყვანეთ API გასაღები",
        "build_query": "⚠  შექმენით მოთხოვნა საძიებო ველის ან ფილტრების გამოყენებით",
        "count_only": "მხოლოდ დათვლა  ",
        "total_hosts": "  სულ ჰოსტი",
        "total": "სულ  │  ნაჩვენებია  ",
        "results": "  შედეგი  │  ",
        "enter_key_str": "შეიყვანეთ გასაღები ჯერ",
        "verified": "✓ დამოწმებულია",
        "geo_located": "გეო-განთავსებული ჰოსტი",
        # Filter groups
        "fg_network": "🌐 ქსელი",
        "fg_location": "🏳️ მდებარეობა",
        "fg_system": "🖥️ სისტემა",
        "fg_software": "🔧 პროგრამა",
        "fg_ssl": "🔐 SSL / TLS",
        "fg_services": "⚙️ სერვისები",
        "fg_protocols": "📡 პროტოკოლები",
        # API badge
        "plan": "გეგმა",
        "query_credits": "მოთხოვნა",
        "scan_credits": "სკანირება",
        # History tab
        "tab_history": "🕐  ისტორია",
        "history_label": "IP სკანირების ისტორია",
        "history_ip_placeholder": "შეიყვანეთ IP (მაგ. 8.8.8.8)",
        "history_btn": "ისტორია",
        "history_empty": "შეიყვანეთ IP სკანირების ისტორიის სანახავად",
        "history_scanned": "ჩაწერილი სკანირება",
        "history_port": "პორტი",
        "history_product": "პროდუქტი",
        "history_timestamp": "დრო",
        "history_banner": "ბანერი",
        # OSINT tab
        "tab_osint": "🗃️  OSINT ბაზა",
        "osint_label": "OSINT მონაცემთა ბაზა",
        "osint_query_placeholder": "სახელი + გვარი  ან  პირადი ნომერი",
        "osint_search_btn": "ძიება",
        "osint_db_paths": "ბაზის ფაილები (მძიმით გამოყოფილი)",
        "osint_db_placeholder": "databases/geodb.txt,databases/geodb1.txt",
        "osint_empty": "ჩაწერეთ სახელი გვარი ან პირადი ნომერი",
        "osint_no_result": "❌ შედეგი ვერ მოიძებნა",
        "osint_results_count": "ნაპოვნია",
        "osint_col_name": "სახელი",
        "osint_col_surname": "გვარი",
        "osint_col_id": "პ/ნ",
        "osint_col_extra": "დამატებითი",
        "osint_no_db": "⚠ ბაზის ფაილი ვერ მოიძებნა",
    },
    "en": {
        "brand_main": "SHODAN ",
        "brand_sub": "EXPLORER",
        "brand_pro": " PRO",
        "lang_btn": "🇬🇪 KA",
        "api_key": "API KEY",
        "api_placeholder": "Shodan API key…",
        "verify_btn": "✓ VERIFY KEY",
        "search_query": "SEARCH QUERY",
        "query_placeholder": "apache port:80 country:US\n(leave blank to use filters)",
        "search_btn": "⌕  SEARCH",
        "count_btn": "≡  COUNT ONLY",
        "filters_label": "FILTERS",
        "ready_status": "Ready — enter API key and build a query",
        "tab_charts": "◈  CHARTS",
        "tab_results": "⊞  RESULTS",
        "tab_map": "🌍  MAP",
        "tab_host": "⚡  HOST LOOKUP",
        "empty_charts": "RUN A SEARCH TO SEE CHARTS",
        "empty_results": "RUN A SEARCH TO SEE RESULTS",
        "empty_count": "COUNT-ONLY MODE — NO RESULT ROWS",
        "empty_map": "RUN A SEARCH TO SEE MAP",
        "empty_geo": "NO GEO COORDINATES IN RESULTS",
        "no_facets": "No facet data returned — try a broader query",
        "host_lookup_label": "HOST LOOKUP",
        "host_ip_placeholder": "Enter IP address (e.g. 8.8.8.8)",
        "lookup_btn": "LOOKUP",
        "provide_key_ip": "Provide API key and IP address",
        "overview": "OVERVIEW",
        "vulnerabilities": "VULNERABILITIES",
        "services": "SERVICES",
        "no_banner": "No banner",
        "ip": "IP",
        "organization": "Organization",
        "country": "Country",
        "city": "City",
        "region": "Region",
        "asn": "ASN",
        "os": "OS",
        "hostnames": "Hostnames",
        "tags": "Tags",
        "open_ports": "Open Ports",
        "last_updated": "Last Updated",
        "hosts_page": "hosts on this page",
        "export_csv": "↓ EXPORT CSV",
        "top_countries": "TOP COUNTRIES",
        "top_ports": "TOP PORTS",
        "top_orgs": "TOP ORGS",
        "top_products": "TOP PRODUCTS",
        "op_systems": "OPERATING SYSTEMS",
        "enter_key_first": "⚠  Enter your API key first",
        "build_query": "⚠  Build a query using the search box or filters",
        "count_only": "COUNT ONLY  ",
        "total_hosts": "  total hosts",
        "total": "total  │  showing  ",
        "results": "  results  │  ",
        "enter_key_str": "Enter a key first",
        "verified": "✓ Verified",
        "geo_located": "geo-located hosts",
        "fg_network": "🌐 Network",
        "fg_location": "🏳️ Location",
        "fg_system": "🖥️ System",
        "fg_software": "🔧 Software",
        "fg_ssl": "🔐 SSL / TLS",
        "fg_services": "⚙️ Services",
        "fg_protocols": "📡 Protocols",
        "plan": "PLAN",
        "query_credits": "QUERY",
        "scan_credits": "SCAN",
        # History tab
        "tab_history": "🕐  HISTORY",
        "history_label": "IP SCAN HISTORY",
        "history_ip_placeholder": "Enter IP address (e.g. 8.8.8.8)",
        "history_btn": "LOAD HISTORY",
        "history_empty": "Enter an IP address to view its full scan history",
        "history_scanned": "recorded scans",
        "history_port": "Port",
        "history_product": "Product",
        "history_timestamp": "Timestamp",
        "history_banner": "Banner",
        # OSINT tab
        "tab_osint": "🗃️  OSINT DB",
        "osint_label": "OSINT DATABASE SEARCH",
        "osint_query_placeholder": "First name + Surname  or  ID Number",
        "osint_search_btn": "SEARCH",
        "osint_db_paths": "Database files (comma-separated paths)",
        "osint_db_placeholder": "databases/geodb.txt,databases/geodb1.txt",
        "osint_empty": "Enter a name/surname or ID number to search",
        "osint_no_result": "❌ No results found",
        "osint_results_count": "found",
        "osint_col_name": "Name",
        "osint_col_surname": "Surname",
        "osint_col_id": "ID No.",
        "osint_col_extra": "Extra",
        "osint_no_db": "⚠ Database file not found",
    }
}

# ====================== HELPERS ======================
def shodan_search(api_key, query, page=1, facets="country,port,org,product,os"):
    r = requests.get(
        "https://api.shodan.io/shodan/host/search",
        params={"key": api_key, "query": query, "page": page, "facets": facets},
        timeout=20
    )
    return r.json()

def shodan_host(api_key, ip):
    r = requests.get(
        f"https://api.shodan.io/shodan/host/{ip}",
        params={"key": api_key},
        timeout=20
    )
    return r.json()

def shodan_count(api_key, query, facets="country,port,org,product,os"):
    r = requests.get(
        "https://api.shodan.io/shodan/host/count",
        params={"key": api_key, "query": query, "facets": facets},
        timeout=20
    )
    return r.json()

def shodan_api_info(api_key):
    r = requests.get(
        "https://api.shodan.io/api-info",
        params={"key": api_key},
        timeout=10
    )
    return r.json()

def shodan_host_history(api_key, ip):
    """Fetch full host history (all banners ever seen) from Shodan."""
    r = requests.get(
        f"https://api.shodan.io/shodan/host/{ip}",
        params={"key": api_key, "history": "true", "minify": "false"},
        timeout=30
    )
    return r.json()

def shodan_dns_resolve(api_key, hostnames):
    """Resolve hostnames to IPs."""
    r = requests.get(
        "https://api.shodan.io/dns/resolve",
        params={"key": api_key, "hostnames": ",".join(hostnames)},
        timeout=15
    )
    return r.json()

# ====================== OSINT DB SEARCH ======================
import unicodedata

def osint_normalize(text):
    return unicodedata.normalize('NFC', text.strip().lower())

def osint_search(query, db_paths):
    """Search OSINT databases (mirrors L45OSINT_BOT logic)."""
    query = query.strip()
    results = []
    for db_file in db_paths:
        if not os.path.exists(db_file):
            continue
        with open(db_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) < 3:
                    continue
                saxeli = parts[0].strip()
                gvari  = parts[1].strip()
                piradi = parts[2].strip()
                # Search by ID number
                clean_query = query.replace(" ", "").replace("-", "")
                if clean_query.isdigit():
                    if clean_query == piradi or clean_query == piradi.lstrip("0"):
                        results.append(parts)
                    continue
                # Search by name + surname
                q_parts = query.split()
                if len(q_parts) < 2:
                    continue
                name_q    = osint_normalize(q_parts[0])
                surname_q = osint_normalize(q_parts[1])
                if name_q == osint_normalize(saxeli) and surname_q == osint_normalize(gvari):
                    results.append(parts)
    # Deduplicate
    seen = set()
    unique = []
    for r in results:
        key = "\t".join(r)
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

def matches_to_df(matches):
    rows = []
    for h in matches:
        rows.append({
            "IP":        h.get("ip_str", ""),
            "Port":      h.get("port", ""),
            "Transport": h.get("transport", "tcp"),
            "Org":       h.get("org") or h.get("isp") or "",
            "Country":   h.get("location", {}).get("country_name") or h.get("country_name", ""),
            "City":      h.get("location", {}).get("city", ""),
            "OS":        h.get("os") or "",
            "Product":   h.get("product") or "",
            "Version":   h.get("version") or "",
            "Hostnames": ", ".join(h.get("hostnames", [])[:3]),
            "CVEs":      len(h.get("vulns", {})),
            "Timestamp": h.get("timestamp", "")[:10],
            "Banner":    (h.get("data") or h.get("banner") or "")[:200],
        })
    return pd.DataFrame(rows)

# ====================== COLOR THEME ======================
BG      = "#060a0f"
BG2     = "#0a1018"
PANEL   = "#0d1520"
PANEL2  = "#111d2b"
BORDER  = "#162436"
BORDER2 = "#1e3347"
ACCENT  = "#00c8ff"
ACCENT2 = "#0088cc"
RED     = "#ff3d5a"
GREEN   = "#00e5a0"
YELLOW  = "#ffc533"
PURPLE  = "#a78bfa"
TEXT    = "#b8ccd8"
TEXTDIM = "#3d5a70"
TEXTBR  = "#e0eef8"

PLOT_CFG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono, monospace", color=TEXT, size=11),
    margin=dict(l=10, r=10, t=36, b=10),
    colorway=[ACCENT, GREEN, YELLOW, RED, PURPLE, "#fb923c", "#34d399"],
)

# ====================== FILTER GROUPS (keys only, labels from translations) ======================
FILTER_GROUPS_RAW = {
    "fg_network": [
        ("ip",  "IP Address / CIDR",           "text",   "192.168.1.0/24"),
        ("port","Port",                          "number", "80"),
        ("net", "Network / CIDR",               "text",   "8.8.8.0/24"),
        ("asn", "ASN",                           "text",   "AS15169"),
        ("isp", "ISP",                           "text",   "Amazon"),
    ],
    "fg_location": [
        ("country","Country Code",              "text",   "US"),
        ("city",   "City",                      "text",   "Berlin"),
        ("region", "Region / State",            "text",   "California"),
        ("geo",    "Geo Coordinates",           "text",   "40.7,-74.0,100"),
        ("postal", "Postal Code",               "text",   "10001"),
    ],
    "fg_system": [
        ("os",       "Operating System",        "text",   "Windows"),
        ("hostname", "Hostname",                "text",   "*.amazonaws.com"),
        ("domain",   "Domain",                  "text",   "example.com"),
        ("org",      "Organization",            "text",   "Google"),
    ],
    "fg_software": [
        ("product",            "Product",       "text",   "Apache"),
        ("version",            "Version",       "text",   "2.4.51"),
        ("cpe",                "CPE",           "text",   "cpe:/a:apache"),
        ("http.title",         "HTTP Title",    "text",   "Dashboard"),
        ("http.status",        "HTTP Status",   "number", "200"),
        ("http.favicon.hash",  "Favicon Hash",  "number", "-335242539"),
        ("http.html_hash",     "HTML Hash",     "number", "0"),
        ("http.headers_hash",  "Headers Hash",  "number", "0"),
    ],
    "fg_ssl": [
        ("ssl",                        "SSL Keywords",      "text",   "Let's Encrypt"),
        ("ssl.cert.subject.cn",        "SSL Subject CN",    "text",   "*.google.com"),
        ("ssl.cert.issuer.cn",         "SSL Issuer CN",     "text",   "DigiCert"),
        ("ssl.cert.serial",            "SSL Serial",        "text",   ""),
        ("ssl.cert.fingerprint",       "SSL Fingerprint",   "text",   ""),
        ("ssl.version",                "SSL Version",       "text",   "TLSv1.3"),
        ("ssl.jarm",                   "JARM Fingerprint",  "text",   ""),
        ("ssl.cert.expired",           "SSL Expired",       "select", ["", "true", "false"]),
        ("ssl.cert.subject.organization","SSL Subject Org", "text",   ""),
    ],
    "fg_services": [
        ("tag",            "Shodan Tags",    "select", ["", "cloud","database","ftp","ics","iot","self-signed","honeypot","tor","vpn","starttls"]),
        ("category",       "Category",       "select", ["", "ics","iot","networking","storage","database","devops"]),
        ("cloud.provider", "Cloud Provider", "select", ["", "Amazon","Azure","Google","DigitalOcean","OVH","Alibaba","Vultr"]),
        ("cloud.region",   "Cloud Region",   "text",   "us-east-1"),
        ("device",         "Device Type",    "text",   "router"),
        ("has_screenshot", "Has Screenshot", "select", ["", "true", "false"]),
        ("has_ssl",        "Has SSL",        "select", ["", "true", "false"]),
        ("vuln",           "CVE ID",         "text",   "CVE-2021-44228"),
    ],
    "fg_protocols": [
        ("ssh.type",       "SSH Type",       "text",   ""),
        ("ssh.fingerprint","SSH Fingerprint","text",   ""),
        ("ftp.anonymous",  "FTP Anonymous",  "select", ["", "true", "false"]),
        ("mongodb.databases","MongoDB DB",   "text",   ""),
        ("rdp.info.os",    "RDP OS",         "text",   ""),
        ("telnet.option",  "Telnet Option",  "text",   ""),
        ("snmp.location",  "SNMP Location",  "text",   ""),
        ("smtp.ehlo",      "SMTP EHLO",      "text",   ""),
        ("ntp.ip",         "NTP IP",         "text",   ""),
    ],
}

ALL_FILTERS = [(key, label, ftype, placeholder)
               for group in FILTER_GROUPS_RAW.values()
               for key, label, ftype, placeholder in group]
FILTER_IDS = [f"f-{k.replace('.','_')}" for k, *_ in ALL_FILTERS]

# ====================== CUSTOM CSS ======================
CUSTOM_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Syne:wght@400;600;700;800&family=Noto+Sans+Georgian:wght@300;400;500;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

body, html {{
    background: {BG} !important;
    color: {TEXT};
    font-family: 'JetBrains Mono', 'Noto Sans Georgian', monospace;
    margin: 0; padding: 0;
    scrollbar-width: thin;
    scrollbar-color: {BORDER2} {BG2};
}}

::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {BG2}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER2}; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {ACCENT2}; }}

.shodpro-header {{
    background: linear-gradient(90deg, {BG}f0 0%, {BG2}f0 100%);
    border-bottom: 1px solid {BORDER2};
    backdrop-filter: blur(16px);
    position: sticky; top: 0; z-index: 500;
    padding: 0 28px;
    height: 60px;
    display: flex; align-items: center; justify-content: space-between;
}}

.header-brand {{
    font-family: 'Syne', 'Noto Sans Georgian', sans-serif;
    font-weight: 800;
    font-size: 20px;
    letter-spacing: 0.08em;
    display: flex; align-items: center; gap: 10px;
}}

.brand-accent {{ color: {ACCENT}; }}
.brand-dim {{ color: {GREEN}; opacity: 0.9; }}

.pulse-dot {{
    width: 8px; height: 8px;
    background: {GREEN};
    border-radius: 50%;
    animation: pulse 2s infinite;
    flex-shrink: 0;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 {GREEN}66; }}
    50% {{ opacity: 0.7; box-shadow: 0 0 0 5px transparent; }}
}}

.btn-lang {{
    background: transparent;
    border: 1px solid {ACCENT}66;
    border-radius: 4px;
    color: {ACCENT};
    font-family: 'JetBrains Mono', 'Noto Sans Georgian', monospace;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
    cursor: pointer;
    padding: 6px 14px;
    transition: all 0.2s;
    white-space: nowrap;
}}

.btn-lang:hover {{
    border-color: {ACCENT};
    background: {ACCENT}18;
    box-shadow: 0 0 12px {ACCENT}33;
}}

.sidebar {{
    width: 290px;
    flex-shrink: 0;
    background: {BG2};
    border-right: 1px solid {BORDER};
    height: calc(100vh - 60px);
    overflow-y: auto;
    padding: 18px 14px;
    display: flex; flex-direction: column; gap: 12px;
}}

.card-panel {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 14px;
    transition: border-color 0.2s;
}}

.card-panel:hover {{ border-color: {BORDER2}; }}
.card-panel.active {{ border-color: {ACCENT}44; }}

.section-label {{
    font-size: 9px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: {TEXTDIM};
    font-weight: 500;
    margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px;
    font-family: 'Noto Sans Georgian', 'JetBrains Mono', sans-serif;
}}

.section-label::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: {BORDER};
}}

.stdinput {{
    width: 100%;
    background: {BG2} !important;
    color: {TEXTBR} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 4px !important;
    padding: 8px 12px !important;
    font-family: 'JetBrains Mono', 'Noto Sans Georgian', monospace !important;
    font-size: 12px !important;
    outline: none !important;
    transition: border-color 0.2s !important;
}}

.stdinput:focus {{
    border-color: {ACCENT}88 !important;
    box-shadow: 0 0 0 2px {ACCENT}18 !important;
}}

.stdinput::placeholder {{ color: {TEXTDIM} !important; }}

.btn-primary {{
    width: 100%;
    background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT2} 100%);
    border: none;
    border-radius: 4px;
    color: {BG};
    font-family: 'Syne', 'Noto Sans Georgian', sans-serif;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 1px;
    cursor: pointer;
    padding: 11px;
    transition: all 0.2s;
    text-transform: uppercase;
}}

.btn-primary:hover {{
    filter: brightness(1.15);
    box-shadow: 0 0 18px {ACCENT}44;
}}

.btn-secondary {{
    width: 100%;
    background: transparent;
    border: 1px solid {YELLOW}66;
    border-radius: 4px;
    color: {YELLOW};
    font-family: 'JetBrains Mono', 'Noto Sans Georgian', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    cursor: pointer;
    padding: 8px;
    transition: all 0.2s;
}}

.btn-secondary:hover {{
    border-color: {YELLOW};
    background: {YELLOW}11;
}}

.btn-verify {{
    width: 100%;
    background: transparent;
    border: 1px solid {GREEN}66;
    border-radius: 4px;
    color: {GREEN};
    font-family: 'JetBrains Mono', 'Noto Sans Georgian', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    cursor: pointer;
    padding: 6px;
    margin-top: 8px;
    transition: all 0.2s;
}}

.btn-verify:hover {{
    border-color: {GREEN};
    background: {GREEN}11;
}}

.btn-download {{
    background: {GREEN};
    color: {BG};
    border: none;
    border-radius: 4px;
    padding: 8px 18px;
    font-family: 'Syne', 'Noto Sans Georgian', sans-serif;
    font-weight: 700;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
}}

.btn-download:hover {{ filter: brightness(1.1); }}

.status-bar {{
    padding: 10px 20px;
    border-bottom: 1px solid {BORDER};
    font-size: 11px;
    color: {TEXTDIM};
    display: flex; align-items: center; gap: 12px;
    min-height: 38px;
    background: {BG2};
    font-family: 'JetBrains Mono', 'Noto Sans Georgian', monospace;
}}

.tab-bar .tab {{
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: {TEXTDIM} !important;
    font-family: 'Noto Sans Georgian', 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    padding: 10px 20px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}}

.tab-bar .tab--selected {{
    color: {ACCENT} !important;
    border-bottom-color: {ACCENT} !important;
    background: {ACCENT}08 !important;
}}

.tab-bar .tab:hover {{ color: {TEXT} !important; }}

.tab-bar > .tab-container {{
    border-bottom: 1px solid {BORDER} !important;
    background: {BG2} !important;
}}

.filter-label {{
    font-size: 9px;
    letter-spacing: 2px;
    color: {TEXTDIM};
    text-transform: uppercase;
    margin-bottom: 5px;
    display: block;
    font-family: 'Noto Sans Georgian', 'JetBrains Mono', sans-serif;
}}

.badge {{
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 10px;
    letter-spacing: 1px;
    font-weight: 500;
}}

.badge-accent {{ background: {ACCENT}22; color: {ACCENT}; border: 1px solid {ACCENT}44; }}
.badge-green  {{ background: {GREEN}22;  color: {GREEN};  border: 1px solid {GREEN}44;  }}
.badge-red    {{ background: {RED}22;    color: {RED};    border: 1px solid {RED}44;    }}
.badge-yellow {{ background: {YELLOW}22; color: {YELLOW}; border: 1px solid {YELLOW}44; }}

.empty-state {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 40px;
    color: {TEXTDIM};
    font-size: 13px;
    letter-spacing: 1px;
    gap: 12px;
    text-align: center;
    font-family: 'Noto Sans Georgian', 'JetBrains Mono', sans-serif;
}}

.empty-state .icon {{ font-size: 36px; opacity: 0.4; }}

.host-card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 10px;
}}

.host-card h5 {{
    font-family: 'Noto Sans Georgian', 'Syne', sans-serif;
    font-size: 13px;
    letter-spacing: 2px;
    color: {ACCENT};
    margin-bottom: 12px;
    text-transform: uppercase;
}}

.kv-row {{
    display: flex;
    border-bottom: 1px solid {BORDER};
    padding: 6px 0;
    font-size: 11px;
    gap: 10px;
}}

.kv-row:last-child {{ border-bottom: none; }}
.kv-key {{ color: {TEXTDIM}; min-width: 140px; flex-shrink: 0; font-family: 'Noto Sans Georgian', 'JetBrains Mono', sans-serif; }}
.kv-val {{ color: {TEXTBR}; word-break: break-all; }}

.accordion-button {{
    background: transparent !important;
    color: {TEXT} !important;
    font-family: 'Noto Sans Georgian', 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    border: none !important;
    box-shadow: none !important;
    padding: 8px 0 !important;
}}

.accordion-item {{
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid {BORDER} !important;
}}

.accordion-body {{
    padding: 8px 0 !important;
    background: transparent !important;
}}

.accordion-button:not(.collapsed) {{
    color: {ACCENT} !important;
}}

.scan-line {{
    position: fixed;
    left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, {ACCENT}33, transparent);
    animation: scan 8s linear infinite;
    pointer-events: none;
    z-index: 9999;
}}

@keyframes scan {{
    0%   {{ top: 0; opacity: 0.6; }}
    50%  {{ opacity: 0.2; }}
    100% {{ top: 100vh; opacity: 0.6; }}
}}

.grid-bg {{
    position: fixed; inset: 0;
    background-image:
        linear-gradient({ACCENT}08 1px, transparent 1px),
        linear-gradient(90deg, {ACCENT}08 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}}

.main-content {{ position: relative; z-index: 1; }}

.chart-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    padding: 16px;
}}

.chart-card {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 6px;
    overflow: hidden;
}}

.chart-title {{
    font-size: 9px;
    letter-spacing: 3px;
    color: {TEXTDIM};
    text-transform: uppercase;
    padding: 10px 14px;
    border-bottom: 1px solid {BORDER};
    background: {BG2};
    font-family: 'Noto Sans Georgian', 'JetBrains Mono', sans-serif;
}}

.cve-badge {{
    display: inline-block;
    padding: 1px 6px;
    border-radius: 3px;
    font-size: 10px;
}}
"""

# ====================== APP ======================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
app.title = "Shodan Explorer Pro"
app.index_string = f'''<!DOCTYPE html>
<html>
<head>
{{%metas%}}
<title>{{%title%}}</title>
{{%favicon%}}
{{%css%}}
<style>{CUSTOM_CSS}</style>
</head>
<body>
{{%app_entry%}}
<footer>{{%config%}}{{%scripts%}}{{%renderer%}}</footer>
</body>
</html>'''

# ====================== FILTER PANEL ======================
def make_filter_panel():
    sections = []
    for group_key, filters in FILTER_GROUPS_RAW.items():
        items = []
        for key, label, ftype, placeholder in filters:
            fid = f"f-{key.replace('.', '_')}"
            if ftype == "select":
                ctrl = dcc.Dropdown(
                    id=fid,
                    options=[{"label": v or "— any —", "value": v} for v in placeholder],
                    value="", clearable=False,
                    style={
                        "background": BG2, "color": TEXT,
                        "border": f"1px solid {BORDER}",
                        "fontSize": "11px", "fontFamily": "JetBrains Mono"
                    }
                )
            else:
                ctrl = dcc.Input(
                    id=fid, type=ftype, placeholder=str(placeholder),
                    className="stdinput",
                    style={"marginTop": "0"}
                )
            items.append(html.Div([
                html.Span(label, className="filter-label"),
                ctrl
            ], style={"marginBottom": "10px"}))
        # Use English label as default; will be updated by callback
        sections.append(
            dbc.AccordionItem(
                html.Div(items, style={"padding": "8px 0"}),
                title=TRANSLATIONS["ka"][group_key],
                item_id=group_key,
                style={"fontSize": "11px"}
            )
        )
    return dbc.Accordion(sections, start_collapsed=True, always_open=True, id="filter-accordion")

# ====================== LAYOUT ======================
def layout():
    t = TRANSLATIONS["ka"]  # Start in Georgian
    return html.Div([
        html.Div(className="grid-bg"),
        html.Div(className="scan-line"),

        # Language store — "ka" by default
        dcc.Store(id="store-lang", data="ka"),

        # ── Header ──────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Div(className="pulse-dot"),
                html.Div([
                    html.Span(id="brand-main", children=t["brand_main"], className="brand-accent"),
                    html.Span(id="brand-sub",  children=t["brand_sub"],  className="brand-dim"),
                    html.Span(id="brand-pro",  children=t["brand_pro"],
                              style={"color": TEXTDIM, "fontSize": "12px",
                                     "fontFamily": "JetBrains Mono", "marginLeft": "4px"}),
                ], className="header-brand"),
            ], style={"display": "flex", "alignItems": "center", "gap": "12px"}),

            html.Div([
                html.Div(id="api-info-badge",
                         style={"fontFamily": "JetBrains Mono", "fontSize": "11px", "color": TEXTDIM}),
                html.Button(t["lang_btn"], id="btn-lang", n_clicks=0, className="btn-lang"),
            ], style={"display": "flex", "alignItems": "center", "gap": "16px"}),

        ], className="shodpro-header"),

        # ── Body ────────────────────────────────────────────────
        html.Div([
            # Sidebar
            html.Div([
                # API Key
                html.Div([
                    html.Div(id="label-api-key", children=t["api_key"], className="section-label"),
                    dcc.Input(
                        id="api-key", type="password",
                        placeholder=t["api_placeholder"],
                        value=DEFAULT_API_KEY,
                        className="stdinput"
                    ),
                    html.Button(t["verify_btn"], id="btn-verify", n_clicks=0, className="btn-verify"),
                    html.Div(id="api-verify-msg", style={"marginTop": "6px", "fontSize": "10px"}),
                ], className="card-panel"),

                # Query
                html.Div([
                    html.Div(id="label-search-query", children=t["search_query"], className="section-label"),
                    dcc.Textarea(
                        id="free-query",
                        placeholder=t["query_placeholder"],
                        className="stdinput",
                        style={"height": "72px", "resize": "vertical", "width": "100%"}
                    ),
                    html.Button(t["search_btn"], id="btn-search", n_clicks=0,
                                className="btn-primary", style={"marginTop": "10px"}),
                    html.Button(t["count_btn"], id="btn-count", n_clicks=0,
                                className="btn-secondary", style={"marginTop": "6px"}),
                ], className="card-panel"),

                # Filters
                html.Div([
                    html.Div(id="label-filters", children=t["filters_label"], className="section-label"),
                    make_filter_panel(),
                ], className="card-panel",
                   style={"maxHeight": "55vh", "overflowY": "auto"}),

            ], className="sidebar main-content"),

            # Main Content
            html.Div([
                # Status bar
                html.Div(
                    html.Span(t["ready_status"], style={"color": TEXTDIM}),
                    id="status-bar", className="status-bar"
                ),

                # Tabs
                dcc.Tabs(id="tabs", value="tab-charts", className="tab-bar", children=[
                    dcc.Tab(label=t["tab_charts"],  value="tab-charts",  className="tab"),
                    dcc.Tab(label=t["tab_results"], value="tab-table",   className="tab"),
                    dcc.Tab(label=t["tab_map"],     value="tab-map",     className="tab"),
                    dcc.Tab(label=t["tab_host"],    value="tab-host",    className="tab"),
                    dcc.Tab(label=t["tab_history"], value="tab-history", className="tab"),
                    dcc.Tab(label=t["tab_osint"],   value="tab-osint",   className="tab"),
                ], colors={"border": BORDER, "primary": ACCENT, "background": BG2}),

                html.Div(id="tab-content",
                         style={"overflowY": "auto", "height": "calc(100vh - 155px)"}),
            ], style={"flex": "1", "minWidth": "0", "display": "flex",
                      "flexDirection": "column"}, className="main-content"),

        ], style={"display": "flex", "height": "calc(100vh - 60px)"}),

        dcc.Store(id="store-results"),
        dcc.Store(id="store-facets"),
        dcc.Download(id="download-csv"),
    ], style={"background": BG, "minHeight": "100vh", "position": "relative"})

app.layout = layout()

# ====================== CALLBACKS ======================

# ── Language toggle ──────────────────────────────────────
@app.callback(
    Output("store-lang", "data"),
    Input("btn-lang", "n_clicks"),
    State("store-lang", "data"),
    prevent_initial_call=True
)
def toggle_lang(n, current_lang):
    return "en" if current_lang == "ka" else "ka"


@app.callback(
    Output("btn-lang",          "children"),
    Output("brand-main",        "children"),
    Output("brand-sub",         "children"),
    Output("brand-pro",         "children"),
    Output("label-api-key",     "children"),
    Output("api-key",           "placeholder"),
    Output("btn-verify",        "children"),
    Output("label-search-query","children"),
    Output("free-query",        "placeholder"),
    Output("btn-search",        "children"),
    Output("btn-count",         "children"),
    Output("label-filters",     "children"),
    Input("store-lang", "data"),
)
def update_ui_language(lang):
    t = TRANSLATIONS[lang]
    return (
        t["lang_btn"],
        t["brand_main"],
        t["brand_sub"],
        t["brand_pro"],
        t["api_key"],
        t["api_placeholder"],
        t["verify_btn"],
        t["search_query"],
        t["query_placeholder"],
        t["search_btn"],
        t["count_btn"],
        t["filters_label"],
    )


def build_query(free_text, filter_values):
    parts = [free_text.strip()] if free_text and free_text.strip() else []
    for (key, label, ftype, _), val in zip(ALL_FILTERS, filter_values):
        if val and str(val).strip():
            v = str(val).strip()
            if " " in v and not v.startswith('"'):
                v = f'"{v}"'
            parts.append(f"{key}:{v}")
    return " ".join(parts)


@app.callback(
    Output("api-verify-msg", "children"),
    Output("api-info-badge", "children"),
    Input("btn-verify", "n_clicks"),
    State("api-key", "value"),
    State("store-lang", "data"),
    prevent_initial_call=True
)
def verify_api(n, api_key, lang):
    t = TRANSLATIONS[lang]
    if not api_key:
        return html.Span(t["enter_key_str"], style={"color": YELLOW}), ""
    try:
        info = shodan_api_info(api_key)
        if "error" in info:
            return html.Span(f"✗ {info['error']}", style={"color": RED}), ""
        plan    = info.get("plan", "unknown")
        credits = info.get("query_credits", "?")
        scan    = info.get("scan_credits", "?")
        badge = html.Span([
            html.Span(f"{t['plan']}: {plan.upper()} ", style={"color": ACCENT}),
            html.Span(f"| {t['query_credits']}: {credits} | {t['scan_credits']}: {scan}",
                      style={"color": TEXTDIM}),
        ])
        return html.Span(t["verified"], style={"color": GREEN}), badge
    except Exception as e:
        return html.Span(f"✗ {e}", style={"color": RED}), ""


@app.callback(
    Output("status-bar", "children"),
    Output("store-results", "data"),
    Output("store-facets", "data"),
    Input("btn-search", "n_clicks"),
    Input("btn-count",  "n_clicks"),
    State("api-key",    "value"),
    State("free-query", "value"),
    State("store-lang", "data"),
    *[State(fid, "value") for fid in FILTER_IDS],
    prevent_initial_call=True
)
def do_search(n_search, n_count, api_key, free_text, lang, *filter_values):
    t = TRANSLATIONS[lang]
    triggered = ctx.triggered_id
    if not api_key:
        return html.Span(t["enter_key_first"], style={"color": YELLOW}), None, None

    query = build_query(free_text or "", filter_values)
    if not query.strip():
        return html.Span(t["build_query"], style={"color": YELLOW}), None, None

    try:
        if triggered == "btn-count":
            data   = shodan_count(api_key, query)
            total  = data.get("total", 0)
            facets = data.get("facets", {})
            status = html.Span([
                html.Span(t["count_only"], style={"color": TEXTDIM}),
                html.Span(f"{total:,}", style={"color": ACCENT, "fontWeight": "700"}),
                html.Span(t["total_hosts"], style={"color": TEXTDIM}),
                html.Span(f"  │  q: {query[:60]}{'…' if len(query) > 60 else ''}",
                          style={"color": TEXTDIM, "fontSize": "10px"}),
            ])
            return status, [], facets

        data = shodan_search(api_key, query)
        if "error" in data:
            return html.Span(f"✗ API Error: {data['error']}", style={"color": RED}), None, None

        total   = data.get("total", 0)
        matches = data.get("matches", [])
        facets  = data.get("facets", {})
        status  = html.Span([
            html.Span(f"{total:,}", style={"color": ACCENT, "fontWeight": "700"}),
            html.Span(f"  {t['total']}",       style={"color": TEXTDIM}),
            html.Span(f"{len(matches)}",        style={"color": GREEN, "fontWeight": "700"}),
            html.Span(t["results"],             style={"color": TEXTDIM}),
            html.Span(f"{query[:50]}{'…' if len(query) > 50 else ''}",
                      style={"color": TEXTDIM, "fontSize": "10px"}),
        ])
        return status, matches, facets
    except Exception as e:
        return html.Span(f"✗ Error: {e}", style={"color": RED}), None, None


# ── Charts tab ──────────────────────────────────────────
def render_charts(facets, lang="ka"):
    t = TRANSLATIONS[lang]
    if not facets:
        return html.Div([html.Div([
            html.Div("◈", className="icon"),
            html.Div(t["empty_charts"]),
        ], className="empty-state")])

    cards = []
    chart_defs = [
        ("country", t["top_countries"], "bar"),
        ("port",    t["top_ports"],     "pie"),
        ("org",     t["top_orgs"],      "bar"),
        ("product", t["top_products"],  "pie"),
        ("os",      t["op_systems"],    "bar"),
    ]

    for key, title, kind in chart_defs:
        items = facets.get(key, [])
        if not items:
            continue
        labels = [str(i.get("value", "?")) for i in items[:12]]
        values = [i.get("count", 0) for i in items[:12]]

        if kind == "bar":
            fig = go.Figure(go.Bar(
                x=values, y=labels, orientation="h",
                marker=dict(color=ACCENT, opacity=0.85,
                            line=dict(color=ACCENT2, width=0.5)),
                hovertemplate="%{y}: %{x:,}<extra></extra>"
            ))
            fig.update_layout(**PLOT_CFG, title=dict(text="", x=0),
                              xaxis=dict(showgrid=True, gridcolor=BORDER,
                                         zeroline=False, tickfont=dict(size=10)),
                              yaxis=dict(showgrid=False, autorange="reversed",
                                         tickfont=dict(size=10)),
                              height=300)
        else:
            fig = go.Figure(go.Pie(
                labels=labels, values=values,
                hole=0.45, textfont=dict(size=10),
                marker=dict(colors=[ACCENT, GREEN, YELLOW, RED, PURPLE,
                                    "#fb923c", "#34d399", "#60a5fa"]),
                hovertemplate="%{label}: %{value:,}<extra></extra>"
            ))
            fig.update_layout(**PLOT_CFG, height=300,
                              showlegend=True,
                              legend=dict(font=dict(size=10)))

        cards.append(html.Div([
            html.Div(title, className="chart-title"),
            dcc.Graph(figure=fig, config={"displayModeBar": False},
                      style={"height": "300px"}),
        ], className="chart-card"))

    if not cards:
        return html.Div(html.Div(t["no_facets"], className="empty-state"))

    return html.Div(cards, className="chart-grid")


# ── Table tab ───────────────────────────────────────────
def render_table(results, lang="ka"):
    t = TRANSLATIONS[lang]
    if results is None:
        return html.Div(html.Div([
            html.Div("⊞", className="icon"),
            html.Div(t["empty_results"]),
        ], className="empty-state"))
    if len(results) == 0:
        return html.Div(html.Div([
            html.Div("≡", className="icon"),
            html.Div(t["empty_count"]),
        ], className="empty-state"))

    df = matches_to_df(results)

    def cve_badge(val):
        if val == 0:
            return val
        return f"🔴 {val}"

    df["CVEs"] = df["CVEs"].apply(cve_badge)

    return html.Div([
        html.Div([
            html.Span(f"{len(df)} {t['hosts_page']}",
                      style={"fontSize": "11px", "color": TEXTDIM}),
            html.Button(t["export_csv"], id="btn-download-csv", className="btn-download"),
        ], style={"display": "flex", "alignItems": "center",
                  "justifyContent": "space-between",
                  "padding": "12px 16px",
                  "borderBottom": f"1px solid {BORDER}"}),

        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": c, "id": c} for c in df.columns],
            page_size=20,
            filter_action="native",
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_cell={
                "backgroundColor": PANEL,
                "color": TEXT,
                "border": f"1px solid {BORDER}",
                "fontSize": "11px",
                "padding": "8px 12px",
                "fontFamily": "JetBrains Mono",
                "maxWidth": "240px",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
            },
            style_header={
                "backgroundColor": BG2,
                "color": ACCENT,
                "fontWeight": "700",
                "fontSize": "10px",
                "letterSpacing": "1px",
                "border": f"1px solid {BORDER}",
                "textTransform": "uppercase",
            },
            style_data_conditional=[
                {"if": {"filter_query": '{CVEs} > 0'}, "color": RED},
            ],
            tooltip_data=[
                {c: {"value": str(row[c]), "type": "markdown"}
                 for c in df.columns} for row in df.to_dict("records")
            ],
            tooltip_duration=None,
        )
    ], style={"height": "100%"})


# ── Map tab ─────────────────────────────────────────────
def render_map(results, lang="ka"):
    t = TRANSLATIONS[lang]
    if not results:
        return html.Div(html.Div([
            html.Div("🌍", className="icon"),
            html.Div(t["empty_map"]),
        ], className="empty-state"))

    rows = []
    for h in results:
        loc = h.get("location", {})
        lat = loc.get("latitude") or h.get("latitude")
        lon = loc.get("longitude") or h.get("longitude")
        if lat and lon:
            rows.append({
                "ip":      h.get("ip_str", ""),
                "org":     h.get("org") or "",
                "port":    str(h.get("port", "")),
                "country": loc.get("country_name", ""),
                "lat": lat, "lon": lon,
            })

    if not rows:
        return html.Div(html.Div([
            html.Div("🌍", className="icon"),
            html.Div(t["empty_geo"]),
        ], className="empty-state"))

    df = pd.DataFrame(rows)
    fig = px.scatter_geo(
        df, lat="lat", lon="lon",
        hover_name="ip",
        hover_data={"org": True, "port": True, "country": True, "lat": False, "lon": False},
        color_discrete_sequence=[ACCENT],
        projection="natural earth"
    )
    fig.update_traces(marker=dict(size=7, opacity=0.8, line=dict(color=BG, width=0.5)))
    fig.update_geos(
        bgcolor=BG, landcolor=PANEL2, oceancolor=BG, lakecolor=BG2,
        countrycolor=BORDER2, showcountries=True, showocean=True,
        showlakes=True, framecolor=BORDER,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", geo_bgcolor=BG,
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(color=TEXT, family="JetBrains Mono"),
    )

    return html.Div([
        html.Div([
            html.Span(f"{len(rows)} {t['geo_located']}",
                      style={"fontSize": "11px", "color": TEXTDIM}),
        ], style={"padding": "10px 16px", "borderBottom": f"1px solid {BORDER}"}),
        dcc.Graph(figure=fig, config={"displayModeBar": False},
                  style={"height": "calc(100vh - 210px)"}),
    ])


# ── Host Lookup tab ─────────────────────────────────────
def render_host_lookup(api_key, lang="ka"):
    t = TRANSLATIONS[lang]
    return html.Div([
        html.Div([
            html.Div(t["host_lookup_label"], className="section-label"),
            html.Div([
                dcc.Input(
                    id="host-ip-input", type="text",
                    placeholder=t["host_ip_placeholder"],
                    className="stdinput", style={"flex": "1"}
                ),
                html.Button(t["lookup_btn"], id="btn-host-lookup", n_clicks=0,
                            style={
                                "background": ACCENT, "color": BG,
                                "border": "none", "borderRadius": "4px",
                                "padding": "8px 18px",
                                "fontFamily": "'Noto Sans Georgian', 'Syne', sans-serif",
                                "fontWeight": "700", "fontSize": "12px",
                                "letterSpacing": "1px", "cursor": "pointer",
                                "flexShrink": "0",
                            }),
            ], style={"display": "flex", "gap": "8px", "alignItems": "center"}),
        ], style={"padding": "16px", "borderBottom": f"1px solid {BORDER}"}),
        html.Div(id="host-lookup-result",
                 style={"padding": "16px", "overflowY": "auto",
                        "height": "calc(100vh - 240px)"}),
        dcc.Store(id="store-api-key-shadow"),
    ])


@app.callback(
    Output("host-lookup-result", "children"),
    Input("btn-host-lookup", "n_clicks"),
    State("host-ip-input", "value"),
    State("api-key", "value"),
    State("store-lang", "data"),
    prevent_initial_call=True
)
def do_host_lookup(n, ip, api_key, lang):
    t = TRANSLATIONS[lang]
    if not ip or not api_key:
        return html.Span(t["provide_key_ip"], style={"color": YELLOW})
    try:
        data = shodan_host(api_key, ip.strip())
        if "error" in data:
            return html.Span(f"✗ {data['error']}", style={"color": RED})

        ports     = data.get("ports", [])
        vulns     = list(data.get("vulns", {}).keys())
        tags      = data.get("tags", [])
        hostnames = data.get("hostnames", [])

        def kv(key, val):
            return html.Div([
                html.Span(key, className="kv-key"),
                html.Span(str(val) if val else "—", className="kv-val"),
            ], className="kv-row")

        overview = html.Div([
            html.H5(t["overview"]),
            kv(t["ip"],           data.get("ip_str", "")),
            kv(t["organization"], data.get("org") or data.get("isp", "")),
            kv(t["country"],      data.get("country_name", "")),
            kv(t["city"],         data.get("city", "")),
            kv(t["region"],       data.get("region_code", "")),
            kv(t["asn"],          data.get("asn", "")),
            kv(t["os"],           data.get("os") or "Unknown"),
            kv(t["hostnames"],    ", ".join(hostnames) if hostnames else "—"),
            kv(t["tags"],         ", ".join(tags) if tags else "—"),
            kv(t["open_ports"],   ", ".join(str(p) for p in sorted(ports)) if ports else "—"),
            kv(t["last_updated"], data.get("last_update", "")),
        ], className="host-card")

        vuln_block = None
        if vulns:
            vuln_block = html.Div([
                html.H5(t["vulnerabilities"]),
                html.Div([
                    html.Span(v, style={
                        "display": "inline-block", "margin": "3px",
                        "padding": "3px 8px", "background": f"{RED}22",
                        "border": f"1px solid {RED}55",
                        "color": RED, "fontSize": "10px", "borderRadius": "3px"
                    })
                    for v in vulns
                ])
            ], className="host-card")

        services = []
        for svc in data.get("data", [])[:10]:
            port      = svc.get("port", "?")
            transport = svc.get("transport", "tcp")
            product   = svc.get("product", "")
            version   = svc.get("version", "")
            banner    = (svc.get("data") or svc.get("banner") or "")[:300]
            services.append(html.Div([
                html.H5(f"PORT {port}/{transport.upper()} — {product} {version}".strip(" —")),
                html.Pre(banner, style={
                    "background": BG, "color": TEXT, "padding": "10px",
                    "fontSize": "10px", "fontFamily": "JetBrains Mono",
                    "overflowX": "auto", "whiteSpace": "pre-wrap",
                    "borderRadius": "4px", "border": f"1px solid {BORDER}",
                    "maxHeight": "160px", "overflowY": "auto",
                }) if banner else html.Span(t["no_banner"],
                                            style={"color": TEXTDIM, "fontSize": "11px"}),
            ], className="host-card"))

        children = [overview]
        if vuln_block:
            children.append(vuln_block)
        if services:
            children.append(html.Div([
                html.H5(t["services"], style={
                    "fontFamily": "'Noto Sans Georgian', Syne", "fontSize": "11px",
                    "letterSpacing": "3px", "color": TEXTDIM,
                    "textTransform": "uppercase", "marginBottom": "10px"
                }),
                *services,
            ]))

        return html.Div(children)

    except Exception as e:
        return html.Span(f"✗ {e}", style={"color": RED})


# ── Tab router ──────────────────────────────────────────
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
    Input("store-results", "data"),
    Input("store-facets", "data"),
    Input("store-lang", "data"),
    State("api-key", "value"),
)
def render_tab(tab, results, facets, lang, api_key):
    if tab == "tab-charts":
        return render_charts(facets, lang)
    elif tab == "tab-table":
        return render_table(results, lang)
    elif tab == "tab-map":
        return render_map(results, lang)
    elif tab == "tab-host":
        return render_host_lookup(api_key, lang)
    elif tab == "tab-history":
        return render_history_lookup(api_key, lang)
    elif tab == "tab-osint":
        return render_osint_tab(lang)
    return html.Div("Select a tab")


# ── Tab labels re-render on language change ─────────────
@app.callback(
    Output("tabs", "children"),
    Input("store-lang", "data"),
)
def update_tab_labels(lang):
    t = TRANSLATIONS[lang]
    return [
        dcc.Tab(label=t["tab_charts"],  value="tab-charts",  className="tab"),
        dcc.Tab(label=t["tab_results"], value="tab-table",   className="tab"),
        dcc.Tab(label=t["tab_map"],     value="tab-map",     className="tab"),
        dcc.Tab(label=t["tab_host"],    value="tab-host",    className="tab"),
        dcc.Tab(label=t["tab_history"], value="tab-history", className="tab"),
        dcc.Tab(label=t["tab_osint"],   value="tab-osint",   className="tab"),
    ]


# ── Host History tab ────────────────────────────────────
def render_history_lookup(api_key, lang="ka"):
    t = TRANSLATIONS[lang]
    return html.Div([
        html.Div([
            html.Div(t["history_label"], className="section-label"),
            html.Div([
                dcc.Input(
                    id="history-ip-input", type="text",
                    placeholder=t["history_ip_placeholder"],
                    className="stdinput", style={"flex": "1"}
                ),
                html.Button(t["history_btn"], id="btn-history-lookup", n_clicks=0,
                            style={
                                "background": PURPLE, "color": BG,
                                "border": "none", "borderRadius": "4px",
                                "padding": "8px 18px",
                                "fontFamily": "'Noto Sans Georgian', 'Syne', sans-serif",
                                "fontWeight": "700", "fontSize": "12px",
                                "letterSpacing": "1px", "cursor": "pointer",
                                "flexShrink": "0",
                            }),
            ], style={"display": "flex", "gap": "8px", "alignItems": "center"}),
        ], style={"padding": "16px", "borderBottom": f"1px solid {BORDER}"}),
        html.Div(id="history-lookup-result",
                 style={"padding": "16px", "overflowY": "auto",
                        "height": "calc(100vh - 240px)"}),
        dcc.Store(id="store-history-api-key-shadow"),
    ])


@app.callback(
    Output("history-lookup-result", "children"),
    Input("btn-history-lookup", "n_clicks"),
    State("history-ip-input", "value"),
    State("api-key", "value"),
    State("store-lang", "data"),
    prevent_initial_call=True
)
def do_history_lookup(n, ip, api_key, lang):
    t = TRANSLATIONS[lang]
    if not ip or not api_key:
        return html.Span(t["provide_key_ip"], style={"color": YELLOW})
    try:
        data = shodan_host_history(api_key, ip.strip())
        if "error" in data:
            return html.Span(f"✗ {data['error']}", style={"color": RED})

        scans = data.get("data", [])
        if not scans:
            return html.Span(t["history_empty"], style={"color": TEXTDIM})

        # Summary row
        header = html.Div([
            html.Div([
                html.Span(f"{data.get('ip_str','?')}",
                          style={"color": ACCENT, "fontWeight": "700", "fontSize": "14px",
                                 "fontFamily": "JetBrains Mono"}),
                html.Span(f"  —  {data.get('org','?')}",
                          style={"color": TEXTDIM, "fontSize": "11px"}),
            ]),
            html.Span(f"{len(scans)} {t['history_scanned']}",
                      style={"fontSize": "10px", "color": YELLOW,
                             "border": f"1px solid {YELLOW}44",
                             "padding": "2px 8px", "borderRadius": "3px",
                             "background": f"{YELLOW}11"}),
        ], style={"display": "flex", "justifyContent": "space-between",
                  "alignItems": "center",
                  "padding": "10px 0", "marginBottom": "12px",
                  "borderBottom": f"1px solid {BORDER}"})

        cards = []
        for svc in scans:
            port      = svc.get("port", "?")
            transport = svc.get("transport", "tcp")
            product   = svc.get("product", "") or ""
            version   = svc.get("version", "") or ""
            timestamp = svc.get("timestamp", "")[:19].replace("T", " ")
            banner    = (svc.get("data") or svc.get("banner") or "")[:400]
            vulns     = list((svc.get("vulns") or {}).keys())
            module    = svc.get("_shodan", {}).get("module", "")

            title_str = f"PORT {port}/{transport.upper()}"
            if product:
                title_str += f"  —  {product}"
                if version:
                    title_str += f" {version}"
            if module:
                title_str += f"  [{module}]"

            vuln_chips = []
            if vulns:
                for v in vulns[:8]:
                    vuln_chips.append(html.Span(v, style={
                        "display": "inline-block", "margin": "2px",
                        "padding": "2px 6px", "background": f"{RED}22",
                        "border": f"1px solid {RED}55", "color": RED,
                        "fontSize": "9px", "borderRadius": "3px",
                        "fontFamily": "JetBrains Mono",
                    }))

            cards.append(html.Div([
                html.Div([
                    html.Span(title_str,
                              style={"color": ACCENT, "fontSize": "11px",
                                     "letterSpacing": "1px", "fontWeight": "700",
                                     "fontFamily": "JetBrains Mono"}),
                    html.Span(timestamp,
                              style={"color": TEXTDIM, "fontSize": "10px",
                                     "fontFamily": "JetBrains Mono"}),
                ], style={"display": "flex", "justifyContent": "space-between",
                          "marginBottom": "8px"}),
                *([html.Div(vuln_chips, style={"marginBottom": "6px"})] if vuln_chips else []),
                html.Pre(banner, style={
                    "background": BG, "color": TEXT, "padding": "8px 10px",
                    "fontSize": "10px", "fontFamily": "JetBrains Mono",
                    "overflowX": "auto", "whiteSpace": "pre-wrap",
                    "borderRadius": "4px", "border": f"1px solid {BORDER}",
                    "maxHeight": "140px", "overflowY": "auto", "margin": "0",
                }) if banner else html.Span(t["no_banner"],
                                            style={"color": TEXTDIM, "fontSize": "10px"}),
            ], className="host-card"))

        return html.Div([header, *cards])

    except Exception as e:
        return html.Span(f"✗ {e}", style={"color": RED})


# ── OSINT DB tab ─────────────────────────────────────────
def render_osint_tab(lang="ka"):
    t = TRANSLATIONS[lang]
    return html.Div([
        # Top search bar
        html.Div([
            html.Div(t["osint_label"], className="section-label"),
            html.Div([
                dcc.Input(
                    id="osint-query-input", type="text",
                    placeholder=t["osint_query_placeholder"],
                    className="stdinput", style={"flex": "1"}
                ),
                html.Button(t["osint_search_btn"], id="btn-osint-search", n_clicks=0,
                            style={
                                "background": GREEN, "color": BG,
                                "border": "none", "borderRadius": "4px",
                                "padding": "8px 20px",
                                "fontFamily": "'Noto Sans Georgian', 'Syne', sans-serif",
                                "fontWeight": "700", "fontSize": "12px",
                                "letterSpacing": "1px", "cursor": "pointer",
                                "flexShrink": "0",
                            }),
            ], style={"display": "flex", "gap": "8px", "alignItems": "center",
                      "marginBottom": "10px"}),
            # DB path config
            html.Div([
                html.Span(t["osint_db_paths"], className="filter-label"),
                dcc.Input(
                    id="osint-db-paths", type="text",
                    placeholder=t["osint_db_placeholder"],
                    value="databases/gedb.txt,databases/gedb1.txt",
                    className="stdinput",
                ),
            ]),
        ], style={"padding": "16px", "borderBottom": f"1px solid {BORDER}"}),

        html.Div(id="osint-results",
                 style={"padding": "16px", "overflowY": "auto",
                        "height": "calc(100vh - 280px)"}),
    ])


@app.callback(
    Output("osint-results", "children"),
    Input("btn-osint-search", "n_clicks"),
    State("osint-query-input", "value"),
    State("osint-db-paths", "value"),
    State("store-lang", "data"),
    prevent_initial_call=True
)
def do_osint_search(n, query, db_paths_str, lang):
    t = TRANSLATIONS[lang]
    if not query or not query.strip():
        return html.Span(t["osint_empty"], style={"color": TEXTDIM})

    db_paths = [p.strip() for p in (db_paths_str or "").split(",") if p.strip()]
    if not db_paths:
        return html.Span(t["osint_no_db"], style={"color": YELLOW})

    # Check at least one db exists
    any_exists = any(os.path.exists(p) for p in db_paths)
    if not any_exists:
        return html.Div([
            html.Span(t["osint_no_db"], style={"color": YELLOW}),
            html.Div([
                html.Span("Checked: ", style={"color": TEXTDIM, "fontSize": "10px"}),
                html.Span(", ".join(db_paths),
                          style={"color": TEXTDIM, "fontSize": "10px",
                                 "fontFamily": "JetBrains Mono"}),
            ], style={"marginTop": "6px"}),
        ])

    try:
        results = osint_search(query.strip(), db_paths)
    except Exception as e:
        return html.Span(f"✗ {e}", style={"color": RED})

    if not results:
        return html.Div([
            html.Span(t["osint_no_result"],
                      style={"color": RED, "fontSize": "13px",
                             "fontFamily": "'Noto Sans Georgian', JetBrains Mono"}),
        ])

    # Build table rows
    table_rows = []
    for parts in results:
        saxeli = parts[0] if len(parts) > 0 else "—"
        gvari  = parts[1] if len(parts) > 1 else "—"
        piradi = parts[2] if len(parts) > 2 else "—"
        extra  = "  │  ".join(parts[3:]) if len(parts) > 3 else ""
        table_rows.append(html.Tr([
            html.Td(saxeli, style={"color": TEXTBR, "padding": "8px 12px",
                                   "fontFamily": "'Noto Sans Georgian', JetBrains Mono",
                                   "fontSize": "12px", "borderBottom": f"1px solid {BORDER}"}),
            html.Td(gvari,  style={"color": TEXTBR, "padding": "8px 12px",
                                   "fontFamily": "'Noto Sans Georgian', JetBrains Mono",
                                   "fontSize": "12px", "borderBottom": f"1px solid {BORDER}"}),
            html.Td(piradi, style={"color": ACCENT, "padding": "8px 12px",
                                   "fontFamily": "JetBrains Mono",
                                   "fontSize": "12px", "borderBottom": f"1px solid {BORDER}",
                                   "letterSpacing": "1px"}),
            html.Td(extra,  style={"color": TEXTDIM, "padding": "8px 12px",
                                   "fontFamily": "JetBrains Mono",
                                   "fontSize": "10px", "borderBottom": f"1px solid {BORDER}",
                                   "maxWidth": "340px", "wordBreak": "break-all"}),
        ]))

    header_style = {
        "color": TEXTDIM, "padding": "6px 12px",
        "fontSize": "9px", "letterSpacing": "3px",
        "textTransform": "uppercase", "textAlign": "left",
        "borderBottom": f"2px solid {BORDER2}",
        "background": BG2,
        "fontFamily": "'Noto Sans Georgian', JetBrains Mono",
    }

    return html.Div([
        html.Div([
            html.Span(f"{len(results)} {t['osint_results_count']}",
                      style={"color": GREEN, "fontWeight": "700", "fontSize": "13px",
                             "fontFamily": "JetBrains Mono"}),
            html.Span(f"  —  {query}",
                      style={"color": TEXTDIM, "fontSize": "11px"}),
        ], style={"marginBottom": "14px", "padding": "8px 0",
                  "borderBottom": f"1px solid {BORDER}"}),
        html.Div([
            html.Table([
                html.Thead(html.Tr([
                    html.Th(t["osint_col_name"],    style=header_style),
                    html.Th(t["osint_col_surname"], style=header_style),
                    html.Th(t["osint_col_id"],      style=header_style),
                    html.Th(t["osint_col_extra"],   style=header_style),
                ])),
                html.Tbody(table_rows),
            ], style={
                "width": "100%", "borderCollapse": "collapse",
                "background": PANEL, "border": f"1px solid {BORDER}",
                "borderRadius": "6px", "overflow": "hidden",
            }),
        ], style={"overflowX": "auto"}),
    ])


# ── CSV Download ─────────────────────────────────────────
@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    State("store-results", "data"),
    prevent_initial_call=True
)
def download_csv(n, results):
    if not results:
        return None
    df = matches_to_df(results)
    fname = f"shodan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return dcc.send_data_frame(df.to_csv, fname, index=False)


# ====================== ENTRY POINT ======================
if __name__ == "__main__":
    key_status = "✓ API გასაღები ჩაიტვირთა api.txt-დან" if DEFAULT_API_KEY else "⚠ api.txt ვერ მოიძებნა — შეიყვანეთ გასაღები ხელით"
    print("\n" + "━" * 62)
    print("  SHODAN EXPLORER PRO  —  ქართული / English")
    print(f"  {key_status}")
    print("  Open: http://127.0.0.1:8050")
    print("━" * 62 + "\n")
    app.run(debug=False, host="0.0.0.0", port=8050)
