import http.client

def is_website_blocked(url, timeout):
    try:
        conn = http.client.HTTPSConnection(url, timeout=timeout)
        conn.request("HEAD", "/")
        response = conn.getresponse()
        conn.close()

        if response.status == 200:
            print("✅")
            return False
        else:
            print("👎")
            return True
    except (http.client.HTTPException, OSError):
        print("👎")
        return True
    except UnicodeError: 
        print("🤡")
        return True

def test_domains(input_file, output_file, timeout):
    blocked_domains = []

    with open(input_file, 'r') as f:
        domains = f.read().splitlines()

    for domain in domains:
        print("Testing https://"+domain)
        domain
        if is_website_blocked(domain, timeout):
            blocked_domains.append(domain)

    with open(output_file, 'w') as f:
        for blocked_domain in blocked_domains:
            f.write(blocked_domain + '\n')

    print("Blocked domains have been saved to", output_file)

# Provide the input and output file paths
input_file = 'domain-gfwlist.txt'
output_file = 'domain-gfwlist-blocked.txt'
timeout = 10  # Timeout value in seconds

test_domains(input_file, output_file, timeout)
