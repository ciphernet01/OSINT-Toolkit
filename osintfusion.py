import requests
import socket
import whois
import dns.resolver

def get_ip_info(ip):
    print(f"\n[IP INFO for {ip}]")
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json").json()
        for k, v in res.items():
            print(f"{k.capitalize()}: {v}")
    except:
        print("Failed to fetch IP info")

def get_domain_info(domain):
    print(f"\n[WHOIS for {domain}]")
    try:
        w = whois.whois(domain)
        print(f"Registrar: {w.registrar}")
        print(f"Creation: {w.creation_date}")
        print(f"Expiry: {w.expiration_date}")
    except:
        print("WHOIS lookup failed.")

    print("\n[DNS Records]")
    try:
        for record in ['A', 'MX', 'NS', 'TXT']:
            answers = dns.resolver.resolve(domain, record)
            print(f"{record} Record:")
            for rdata in answers:
                print(f"  {rdata}")
    except:
        print("DNS lookup failed.")

def check_breach(email):
    print(f"\n[Checking Breaches for {email}]")
    url = f"https://haveibeenpwned.com/unifiedsearch/{email}"
    headers = {
        'User-Agent': 'OSINTFusion',
        'hibp-api-key': 'your_hibp_api_key_here'  # Replace with your API key
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            print("✅ Breach found!")
            print(r.json())
        elif r.status_code == 404:
            print("No breaches found.")
        else:
            print("Error or API key issue.")
    except Exception as e:
        print("Error checking breach:", e)

def username_lookup(username):
    print(f"\n[Checking social presence for {username}]")
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Reddit": f"https://reddit.com/u/{username}",
    }
    for site, url in platforms.items():
        r = requests.get(url)
        if r.status_code == 200:
            print(f"🟢 {site}: Found -> {url}")
        else:
            print(f"🔴 {site}: Not found")

if __name__ == "__main__":
    print("==== OSINT FUSION ====")
    target = input("Enter target (email, domain, or IP): ").strip()

    if "@" in target:
        check_breach(target)
    elif target.replace('.', '').isdigit():
        get_ip_info(target)
    else:
        get_domain_info(target)

    user = input("\nEnter username to search (optional): ").strip()
    if user:
        username_lookup(user)
