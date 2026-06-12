"""Schema sanity checks. These run without an API key.

The point: keep the normalized schemas stable, because every module's adapters
depend on them. (Tests that exercise the model live behind a key-gated marker.)
"""

from aug.models import Finding, Severity, Triage, TriageVerdict


def test_finding_minimal():
    f = Finding(
        tool="grype",
        rule_id="CVE-2021-44228",
        title="Log4Shell",
        severity=Severity.critical,
        location="log4j-core@2.14.1",
    )
    assert f.severity is Severity.critical
    assert f.context == ""
    assert f.raw == {}


def test_triage_confidence_bounds():
    t = Triage(
        verdict=TriageVerdict.true_positive,
        adjusted_severity=Severity.high,
        confidence=0.9,
        rationale="Reachable from an unauthenticated endpoint.",
    )
    assert 0.0 <= t.confidence <= 1.0
