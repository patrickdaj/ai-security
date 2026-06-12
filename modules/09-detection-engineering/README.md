# Module 09 — Detection Engineering

Detection engineering is the discipline of turning attacker behavior into
reliable alerts. The bottlenecks are *authoring* good detections from threat
intel and *triaging* the alert firehose. AI helps with both: synthesizing Sigma
rules from a report, and adding judgment to alert triage.

## Tools you tour

- **Sigma** — a generic, vendor-neutral detection rule format that compiles to
  Splunk/Elastic/etc. via `sigma convert`. The lingua franca of detections.
- **Wazuh** — open-source SIEM/XDR; ingests logs, fires rules, manages alerts.
- **Zeek** (revisited) — as a detection source for network behaviors.

### Tour tasks

```bash
# Convert a Sigma rule to your backend's query language
sigma convert -t splunk rules/some_rule.yml
```

Read a few Sigma rules. They're structured: logsource + detection selection +
condition. That structure is generable from prose threat intel — and a model
that knows MITRE ATT&CK can map behavior → detection.

## AI augmentation: threat-intel → Sigma synthesizer + alert triage

Two builds:

1. **Sigma synthesizer.** Given a threat report or an ATT&CK technique
   description, generate a valid Sigma rule (typed fields → rendered YAML),
   including the right `logsource`, a tight `detection` block, and ATT&CK tags.
   Validate with `sigma check` and by converting to a backend.
2. **Alert triage.** Given an alert plus the surrounding events, have the model
   assess: true/false positive, severity in context, and the next
   investigative step — the analyst's "what do I do with this" call.

Define `SigmaRule` and `AlertTriage` schemas. For the synthesizer, the win is a
*precise* rule — push the model to avoid overbroad selections that would bury the
SOC in false positives (the same precision lesson as the Suricata module).

## Exercises

1. Synthesize a Sigma rule from an ATT&CK technique (e.g. T1059 command
   interpreters); validate it and convert to two backends.
2. Triage a batch of Wazuh alerts and confirm the model's FP calls match yours on
   a labeled set.
3. Close the loop: when a generated rule is too noisy on real logs, feed the FPs
   back and have the model tighten the selection.

## Done when

- You can turn a paragraph of threat intel into a validated Sigma rule that
  compiles to your SIEM, and add a judgment layer to alert triage that measurably
  cuts analyst time on a labeled alert set.
