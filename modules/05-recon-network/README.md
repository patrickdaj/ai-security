# Module 05 — Recon & Network Analysis

Network tooling produces *volume*: port-scan output, hours of flow logs,
gigabytes of packets. Humans drown. The AI augmentation here is summarization
and rule-drafting — turning raw telemetry into "here's what's interesting and
here's a detection for it."

## Tools you tour

- **nmap** — host/port/service discovery; the `-oX` XML and NSE scripts.
- **Zeek** — turns packet captures into rich, structured logs (conn, dns, http,
  ssl, files). The analyst's workhorse.
- **Suricata** — IDS/IPS that matches traffic against signatures; you'll draft
  rules for it.

### Tour tasks

```bash
nmap -sV -oX scratch/nmap.xml 127.0.0.1
zeek -r sample.pcap            # produces conn.log, dns.log, http.log, ...
suricata -r sample.pcap -l scratch/suricata/
```

Read Zeek's `conn.log` and `dns.log`. They're already normalized — perfect
`.context` for a model. Notice how much narrative ("this host beaconed to a rare
domain every 60s") is latent in the rows.

## AI augmentation: capture summarizer + detection-rule drafter

Build a tool that ingests Zeek logs (and nmap XML) and produces:

1. A **triage summary** — top talkers, rare/long-lived connections, suspicious
   DNS (DGA-looking, rare TLDs), and a plain-language "what stands out."
2. A **detection rule draft** — given a described behavior ("beaconing to
   `evil.example` every 60s"), emit a Suricata rule (or a Zeek detection script
   stub) the model believes will match, which you then test against the pcap.

Summarize Zeek logs into a `CaptureSummary` schema (entities + findings +
narrative). For rules, generate the typed rule fields and render the Suricata
syntax, then validate with `suricata -T`.

## Exercises

1. Feed a benign + a malicious pcap and confirm the summary flags the difference.
2. Draft a Suricata rule from a behavior description; validate it loads and fires
   on the malicious pcap but not the benign one (precision matters — overbroad
   rules are worse than none).
3. Have the model explain *why* a given connection is suspicious, grounded in the
   log fields, so an analyst can trust or reject it.

## Done when

- You can drop a pcap in and get back a defensible "what's interesting" summary
  plus at least one Suricata rule that validates and fires only on the bad
  traffic.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [Nmap reference guide](https://nmap.org/book/man.html)
- [Zeek docs](https://docs.zeek.org/)
- [Suricata docs](https://docs.suricata.io/)
- [Malware-Traffic-Analysis (sample pcaps)](https://www.malware-traffic-analysis.net/)
