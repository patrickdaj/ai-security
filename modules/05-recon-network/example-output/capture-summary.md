<!-- Example output — illustrative deliverable of module 05. -->

# Capture Summary — `sample.pcap` (via Zeek)

**Narrative:** Traffic is mostly internal HTTP to the app tier. One host
(`10.0.2.15`) stands out: it opens a 1-byte connection to `185.203.x.x:443`
every 60 seconds for 40 minutes — textbook C2 beaconing — and just before, it
made a DNS request for a 28-char random-looking domain (likely DGA).

**Top talkers:** `10.0.1.10` (app), `10.0.1.20` (db), `10.0.2.15` (suspect).

**Suspicious:**
- `10.0.2.15 → 185.203.x.x:443` — periodic 60s beacon, near-zero bytes.
- DNS `xq3p... .info` — high-entropy domain, rare TLD.

## Drafted Suricata rule (validated `suricata -T`)
```
alert tls $HOME_NET any -> $EXTERNAL_NET 443 (msg:"Possible C2 beacon - periodic tiny TLS to rare host"; flow:established; threshold:type both,track by_src,count 5,seconds 600; sid:1000001; rev:1;)
```
Fires on the suspect's beacon, silent on the benign capture.
