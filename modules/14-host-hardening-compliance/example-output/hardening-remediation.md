<!-- Example output — illustrative deliverable of module 14. -->

# Host Hardening Remediation — `web-01`

Lynis: 31 warnings → remediations. 22 auto-apply (low risk), 9 review.

## AUTO — disable core dumps (CIS 1.5.1, low risk)
controls: CIS-1.5.1, SOC2-CC6.1
```yaml
- name: Disable core dumps via limits
  ansible.posix.sysctl:
    name: fs.suid_dumpable
    value: "0"
    state: present
    reload: true
```

## AUTO — enforce SSH protocol hardening (CIS 5.2, low risk)
controls: CIS-5.2.x
```yaml
- name: Harden sshd
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: "^#?PermitRootLogin"
    line: "PermitRootLogin no"
  notify: restart sshd
```

## REVIEW — disable unused service `rpcbind` (high risk)
controls: CIS-2.2.x · held: may break NFS dependents — confirm first.

**Outcome:** 31 findings → idempotent Ansible mapped to controls; safe ones
auto-apply and clear on re-scan, risky ones gated.
