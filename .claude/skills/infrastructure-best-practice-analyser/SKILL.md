---
name: infrastructure-best-practice-analyser
description: Multi-platform infrastructure best-practice assessment and Test Library 1.1.0 standards catalogue for Palo Alto (PAN-OS), FortiGate (FortiOS), Juniper (Junos), Windows Server, and Linux Server. Use when auditing device configs, mapping findings to NIST/NCSC/UKFS-01..06, or checking licensed placeholder rules (ISO/CIS/PCI/SWIFT).
---

# Infrastructure Best-Practice Analyser & Standards Catalogue (`AEGIS` Skill)

## 1. Purpose & Architectural Scope

This skill provides a deterministic, multi-platform best-practice assessment methodology and **Standards Catalogue** (`Test Library 1.1.0`) for evaluating enterprise network and server estates across five core technology platforms:
1. **Palo Alto Networks Firewalls (`PAN-OS`)**
2. **Fortinet FortiGate Firewalls (`FortiOS`)**
3. **Juniper Networks Routers (`Junos OS`)**
4. **Microsoft Windows Servers (`Windows Server 2019 / 2022 / 2025`)**
5. **Enterprise Linux Servers (`RHEL / Rocky / AlmaLinux / Ubuntu LTS / Debian`)**

The skill uses **public NIST, NCSC, and official vendor documentation** as its primary technical sources, alongside **UK financial-services regulator papers (FCA / PRA)** for operational resilience outcomes (`UKFS-01` to `UKFS-06`). Licensed standards (**ISO/IEC 27001 & 27002**, **CIS Benchmarks**, **PCI DSS**, and **SWIFT CSCF**) appear **strictly as reference numbers or topic placeholders** until licensed copies are supplied by an authorised licence holder.

---

## 2. Master Standards Catalogue (Applied on Every Assessment)

| Source | Version | What the Skill Uses |
| :--- | :--- | :--- |
| **NIST SP 800-41 Rev. 1**, *Guidelines on Firewalls and Firewall Policy* | Sept 2009 | Section-level references for firewall policy, stateful inspection, rule-base hygiene, and perimeter/internal segmentation across network firewalls (PAN-OS, FortiOS), router packet filters (Junos `lo0` and transit ACLs), and host firewalls (Windows Defender Firewall, Linux `nftables`/`firewalld`/`ufw`). |
| **NIST SP 800-53 Rev. 5** | Update 1 | **21 controls**: `SC-7` (Boundary Protection), `AC-4` (Information Flow Enforcement), `AC-6` (Least Privilege), `AC-7` (Unsuccessful Logon Attempts), `AC-12` (Session Termination), `AC-17` (Remote Access), `AU-2` (Event Logging), `AU-8` (Time Stamps), `AU-12` (Audit Record Generation), `CM-2` (Baseline Configuration), `CM-3` (Configuration Change Control), `CM-6` (Configuration Settings), `CM-7` (Least Functionality), `CM-8` (System Component Inventory), `CP-9` (System Backup), `IA-2` (Identification and Authentication), `SC-8` (Transmission Confidentiality and Integrity), `SC-13` (Cryptographic Protection), `SI-2` (Flaw Remediation), `SI-3` (Malicious Code Protection), `SI-4` (System Monitoring). |
| **NIST Cybersecurity Framework (CSF) 2.0** | Feb 2024 | **11 subcategories**: `PR.IR-01`, `PR.AA-03`, `PR.AA-05`, `PR.PS-01`, `PR.PS-02`, `PR.PS-04`, `PR.DS-02`, `PR.DS-11`, `DE.CM-01`, `ID.AM-03`, `ID.RA-01`. |
| **NCSC Guidance** | As published | • *10 Steps to Cyber Security: Network security*<br/>• *10 Steps to Cyber Security: Vulnerability management*<br/>• *Preventing lateral movement*<br/>• *Security architecture anti-patterns*<br/>• *Secure system administration*<br/>• *Introduction to logging for security purposes* |
| **Fortinet Document Library** | Matches the FortiOS release assessed | *FortiOS Administration Guide*, *Best Practices*, and *"Hardening your FortiGate"*. |
| **Multi-Vendor Hardening Libraries** | Matches the OS / NOS release assessed | • **Palo Alto Networks**: *PAN-OS Administrator's Guide*, *Best Practices for Securing Administrative Access*, *Day 1 / IronSkillet Hardening Guidance*<br/>• **Juniper Networks**: *Junos OS Day One: Hardening Junos Devices*, *Routing Engine Protection & Firewall Filters*<br/>• **Microsoft**: *Windows Server Security Baselines*, *Defender Firewall with Advanced Security*, *Secured-Core Server Guidance*<br/>• **Linux**: *RHEL / Ubuntu LTS Security Hardening Guides*, *OpenSSH / systemd / auditd / kernel `sysctl` Documentation* |
| **UK Financial-Services View (`UKFS-01` to `UKFS-06`)** | Organisation's own wording | Six outcome statements (`UKFS-01` to `UKFS-06`) drawing on **FCA PS21/3** (*Building operational resilience*), **PRA PS6/21** and **SS1/21** (*Operational resilience: Impact tolerances for important business services*), and **PRA SS2/21** (*Outsourcing and third-party risk management*). |

### 2.1 UK Financial-Services Operational Resilience View (`UKFS-01` to `UKFS-06`)

> [!IMPORTANT]
> **Regulatory Clarification**: The FCA and PRA do **not** prescribe specific firewall rules, router filters, server registry/kernel settings, or technical tools. Instead, the six outcome statements below (`UKFS-01` to `UKFS-06`), phrased in the organisation's own wording, map how technical infrastructure controls support operational resilience obligations:

| Outcome ID | Outcome Statement (Organisation's Own Wording) | Regulatory Basis | How Technical Estate Controls Map to This Outcome |
| :--- | :--- | :--- | :--- |
| **`UKFS-01`** | **Important business services and their supporting technology** | FCA PS21/3, PRA PS6/21, PRA SS1/21 | Accurate component inventory (`CM-8`, `ID.AM-03`), clear zone/VLAN/VRF mapping, interface descriptions, and documented data flows (`AC-4`, `SC-7`) identifying which firewalls, routers, and servers underpin important business services. |
| **`UKFS-02`** | **Impact tolerances** | FCA PS21/3, PRA PS6/21, PRA SS1/21 | High-availability (HA) state synchronisation, DoS/Zone protection profiles, Routing Engine (`lo0`) policing, resource limits, and verified system backups (`CP-9`, `PR.DS-11`) so estates remain within maximum tolerable disruption thresholds. |
| **`UKFS-03`** | **Technology risk** | FCA PS21/3, PRA SS1/21 | Hardened baseline configurations (`CM-2`, `CM-6`), least functionality (`CM-7`), strong cryptography (`SC-8`, `SC-13`), lateral movement prevention (NCSC), and host anti-malware/EDR (`SI-3`, `SI-4`). |
| **`UKFS-04`** | **Change governance** | FCA PS21/3, PRA SS1/21 | Configuration change control (`CM-3`), named rule comments/ticket references on firewall and router rules, commit-confirm / revision history tracking, and elimination of unapproved emergency rules. |
| **`UKFS-05`** | **Third-party assurance** | PRA SS2/21, FCA PS21/3 | Segregated third-party/vendor remote access (`AC-17`), MFA enforcement (`IA-2`, `PR.AA-03`), jump-host isolation, explicit session termination (`AC-12`), and full audit logging of external support activity (`AU-2`, `AU-12`). |
| **`UKFS-06`** | **Remediation of weaknesses** | FCA PS21/3, PRA SS1/21 | Continuous vulnerability and OS/NOS patch management (`SI-2`, `ID.RA-01`, NCSC *Vulnerability management*), removal of shadowed/legacy rules, and tracked remediation of audit findings. |

---

## 3. Licensed Standards: Reference Numbers & Placeholders Only

To maintain strict copyright and licensing compliance, **no control titles, benchmark prose, or proprietary check descriptions** from the following standards are stored or reproduced in this skill:

1. **ISO/IEC 27001:2022 and 27002:2022**:
   - **16 Annex A references only** (no control titles or text):
     `A.5.9`, `A.5.15`, `A.8.2`, `A.8.5`, `A.8.7`, `A.8.8`, `A.8.9`, `A.8.13`, `A.8.15`, `A.8.16`, `A.8.17`, `A.8.20`, `A.8.22`, `A.8.23`, `A.8.24`, `A.8.32`.
2. **CIS Benchmarks**:
   - **No CIS content at all.** Three topic placeholders (`policy`, `admin`, `system`) per platform wait for recommendation IDs from an authorised reviewer with CIS access:
     - **CIS Fortinet FortiGate Benchmark**: `[CIS-FGT-POLICY-TBD]`, `[CIS-FGT-ADMIN-TBD]`, `[CIS-FGT-SYSTEM-TBD]`
     - **CIS Palo Alto Firewall Benchmark**: `[CIS-PAN-POLICY-TBD]`, `[CIS-PAN-ADMIN-TBD]`, `[CIS-PAN-SYSTEM-TBD]`
     - **CIS Juniper Junos Benchmark**: `[CIS-JUNOS-POLICY-TBD]`, `[CIS-JUNOS-ADMIN-TBD]`, `[CIS-JUNOS-SYSTEM-TBD]`
     - **CIS Microsoft Windows Server Benchmark**: `[CIS-WIN-POLICY-TBD]`, `[CIS-WIN-ADMIN-TBD]`, `[CIS-WIN-SYSTEM-TBD]`
     - **CIS Linux Distribution Benchmark**: `[CIS-LNX-POLICY-TBD]`, `[CIS-LNX-ADMIN-TBD]`, `[CIS-LNX-SYSTEM-TBD]`
3. **PCI DSS 4.0.1 Requirement 1**:
   - Requirement numbers only (`1.2.2` to `1.4.2`), flagged *to be confirmed against the official PCI SSC document*.
4. **SWIFT Customer Security Controls Framework (CSCF)**:
   - Indicative IDs only (`1.1`, `2.3`, `4.2`, `6.4`), flagged *for an authorised SWIFT user to confirm*.

---

## 4. Switched On Per Customer (Opt-In Assessment Overlays)

When initiating an assessment, ask or check which optional customer overlays apply:
- [ ] **PCI DSS 4.0.1** (Requirement `1.2.2` to `1.4.2` reference numbers)
- [ ] **NCSC Cyber Assessment Framework (CAF)** (`B2` Identity & Access Control, `B4` System Security, `C1` Security Monitoring)
- [ ] **SWIFT CSCF** (Indicative IDs `1.1`, `2.3`, `4.2`, `6.4`)
- [ ] **Customer-Specific Security Policies / Contractual Schedules** (supplied in workspace)

---

## 5. Cross-Platform Technical Check Catalogue (`Test Library 1.1.0`)

Each platform is assessed across three standardised topics (**Policy**, **Admin**, **System**) and mapped to the core public catalogue plus licensed reference numbers/placeholders:

### 5.1 Palo Alto Networks Firewalls (`PAN-OS`)

| Check ID & Topic | Technical Assessment Check | NIST 800-53 / 800-41 / CSF 2.0 | NCSC & Vendor Guidance | UKFS / ISO 27001 Ref / CIS Placeholder |
| :--- | :--- | :--- | :--- | :--- |
| **`PAN-POL-01`**<br/>*(Policy)* | **App-ID, User-ID & Service Enforcement**: Security rules specify explicit App-IDs and `application-default` (or explicit ports) rather than `any` application or `any` service; rules lacking Threat Prevention profiles (AV, Anti-Spyware, Vulnerability, URL, WildFire) or session-end logging are flagged. | `SC-7`, `AC-4`, `AU-2`, `AU-12`, `CM-7`, `SI-3`, `SI-4`<br/>NIST 800-41 §4.1–4.3<br/>`PR.IR-01`, `DE.CM-01` | NCSC *Network security* & *Preventing lateral movement*;<br/>PAN-OS *Best Practices for Policy* | `UKFS-01`, `UKFS-03`, `UKFS-04`<br/>ISO: `A.8.7`, `A.8.15`, `A.8.20`, `A.8.22`, `A.8.23`<br/>CIS: `[CIS-PAN-POLICY-TBD]` |
| **`PAN-POL-02`**<br/>*(Policy)* | **Zone Protection, Packet Buffer & DoS Profiles**: All ingress/untrusted zones attach a Zone Protection Profile mitigating SYN/ICMP/UDP floods, reconnaissance scans, and IP spoofing (`strict-ip-check`). | `SC-7`, `SI-4`<br/>NIST 800-41 §4.2<br/>`PR.IR-01`, `DE.CM-01` | NCSC *Security architecture anti-patterns*;<br/>PAN-OS *Zone Protection Guide* | `UKFS-02`, `UKFS-03`<br/>ISO: `A.8.16`, `A.8.20`<br/>CIS: `[CIS-PAN-POLICY-TBD]` |
| **`PAN-ADM-01`**<br/>*(Admin)* | **Management Plane Isolation & MFA**: MGT interface and Management Profiles restrict HTTPS/SSH to authorised jump hosts (`Permitted IP Addresses`); HTTP/Telnet disabled; MFA/SAML/RADIUS/TACACS+ enforced; idle timeout <= 10m; failed login lockout configured. | `AC-6`, `AC-7`, `AC-12`, `AC-17`, `CM-7`, `IA-2`, `SC-8`<br/>`PR.AA-03`, `PR.AA-05` | NCSC *Secure system administration*;<br/>PAN-OS *Securing Administrative Access* | `UKFS-03`, `UKFS-05`<br/>ISO: `A.5.15`, `A.8.2`, `A.8.5`<br/>CIS: `[CIS-PAN-ADMIN-TBD]` |
| **`PAN-SYS-01`**<br/>*(System)* | **Telemetry, Crypto, Backups & Patch Currency**: Authenticated NTP (`AU-8`); TLS syslog / Panorama forwarding (`SC-8`); SNMPv3 only; minimum TLS 1.2; scheduled config export (`CP-9`); PAN-OS & Dynamic Updates current (`SI-2`). | `AU-8`, `CM-2`, `CM-3`, `CM-6`, `CP-9`, `SC-13`, `SI-2`<br/>`PR.PS-01`, `PR.PS-02`, `PR.PS-04`, `PR.DS-02`, `PR.DS-11` | NCSC *Vulnerability management* & *Logging for security purposes*;<br/>PAN-OS *Admin Guide* | `UKFS-02`, `UKFS-04`, `UKFS-06`<br/>ISO: `A.8.8`, `A.8.9`, `A.8.13`, `A.8.17`, `A.8.24`, `A.8.32`<br/>CIS: `[CIS-PAN-SYSTEM-TBD]` |

### 5.2 Fortinet FortiGate Firewalls (`FortiOS`)

| Check ID & Topic | Technical Assessment Check | NIST 800-53 / 800-41 / CSF 2.0 | NCSC & Fortinet Guidance | UKFS / ISO 27001 Ref / CIS Placeholder |
| :--- | :--- | :--- | :--- | :--- |
| **`FGT-POL-01`**<br/>*(Policy)* | **Firewall Policy Hygiene & UTM Inspection**: Eliminate permissive `ALL` service / `all` address rules; enforce UTM profiles (IPS, AV, Web/DNS filter, SSL inspection); enable `logtraffic all` on pass/deny rules (`AU-2`, `AU-12`); configure `local-in-policy` to restrict control-plane services; purge shadowed/unused rules (`CM-7`). | `SC-7`, `AC-4`, `AU-2`, `AU-12`, `CM-3`, `CM-7`, `SI-3`, `SI-4`<br/>NIST 800-41 §4.1–4.3<br/>`PR.IR-01`, `PR.PS-04`, `DE.CM-01` | NCSC *Network security* & *Preventing lateral movement*;<br/>Fortinet *FortiOS Admin Guide* & *Best Practices* | `UKFS-01`, `UKFS-03`, `UKFS-04`, `UKFS-06`<br/>ISO: `A.8.7`, `A.8.15`, `A.8.20`, `A.8.22`, `A.8.23`, `A.8.32`<br/>CIS: `[CIS-FGT-POLICY-TBD]` |
| **`FGT-ADM-01`**<br/>*(Admin)* | **Trusted Hosts, MFA & Management Hardening**: Configure `trusthost` on every `system admin` account; enforce MFA (`two-factor`); disable HTTP/Telnet (`set allowaccess`); set `admintimeout <= 10`, `admin-lockout-threshold`, and `admin-lockout-duration`. | `AC-6`, `AC-7`, `AC-12`, `AC-17`, `CM-7`, `IA-2`, `SC-8`<br/>`PR.AA-03`, `PR.AA-05` | NCSC *Secure system administration*;<br/>Fortinet *"Hardening your FortiGate"* | `UKFS-03`, `UKFS-05`<br/>ISO: `A.5.15`, `A.8.2`, `A.8.5`<br/>CIS: `[CIS-FGT-ADMIN-TBD]` |
| **`FGT-SYS-01`**<br/>*(System)* | **Strong Crypto, HA, Time, Logging & FortiOS PSIRT**: Enforce `set strong-crypto enable` (`SC-13`); authenticated NTP (`AU-8`); encrypted FortiAnalyzer / syslog (`SC-8`); HA group authentication/encryption; automated configuration backups (`CP-9`); FortiOS PSIRT remediation (`SI-2`). | `AU-8`, `CM-2`, `CM-6`, `CM-8`, `CP-9`, `SC-13`, `SI-2`<br/>`PR.PS-01`, `PR.PS-02`, `PR.DS-02`, `PR.DS-11`, `ID.AM-03`, `ID.RA-01` | NCSC *Vulnerability management* & *Logging for security purposes*;<br/>Fortinet *"Hardening your FortiGate"* | `UKFS-01`, `UKFS-02`, `UKFS-06`<br/>ISO: `A.5.9`, `A.8.8`, `A.8.9`, `A.8.13`, `A.8.17`, `A.8.24`<br/>CIS: `[CIS-FGT-SYSTEM-TBD]` |

### 5.3 Juniper Networks Routers (`Junos OS`)

| Check ID & Topic | Technical Assessment Check | NIST 800-53 / 800-41 / CSF 2.0 | NCSC & Vendor Guidance | UKFS / ISO 27001 Ref / CIS Placeholder |
| :--- | :--- | :--- | :--- | :--- |
| **`JUN-POL-01`**<br/>*(Policy)* | **Routing Engine (`lo0.0`) Filter, Anti-Spoofing & BGP Security**: Loopback `lo0.0` filter restricts and polices SSH, NETCONF, SNMP, BGP, OSPF, and ICMP; transit anti-spoofing (`rpf-check`) and bogon filtering active; BGP peers authenticate via TCP-AO or MD5 (`SC-8`, `SC-13`) with `prefix-limit` protection. | `SC-7`, `AC-4`, `SC-8`, `SC-13`, `SI-4`<br/>NIST 800-41 §2.2, §4.2<br/>`PR.IR-01`, `PR.DS-02`, `DE.CM-01` | NCSC *Network security* & *Security architecture anti-patterns*;<br/>Juniper *Hardening Junos Devices* | `UKFS-01`, `UKFS-02`, `UKFS-03`<br/>ISO: `A.8.16`, `A.8.20`, `A.8.22`, `A.8.24`<br/>CIS: `[CIS-JUNOS-POLICY-TBD]` |
| **`JUN-ADM-01`**<br/>*(Admin)* | **SSHv2, Root Login Denial & AAA**: Enforce `ssh protocol-version v2` and `root-login deny`; strong SSH ciphers/MACs; TACACS+/RADIUS authentication with role-based login classes (`AC-6`, `IA-2`); configure `retry-options` lockout (`AC-7`) and CLI idle-timeout (`AC-12`). | `AC-6`, `AC-7`, `AC-12`, `AC-17`, `IA-2`, `SC-8`, `SC-13`<br/>`PR.AA-03`, `PR.AA-05` | NCSC *Secure system administration*;<br/>Juniper *Hardening Junos Devices* | `UKFS-03`, `UKFS-05`<br/>ISO: `A.5.15`, `A.8.2`, `A.8.5`, `A.8.24`<br/>CIS: `[CIS-JUNOS-ADMIN-TBD]` |
| **`JUN-SYS-01`**<br/>*(System)* | **Unused Services, Rescue Config, Archival & Junos SIRT**: Disable Telnet, FTP, Finger, HTTP, and clear-text XNM (`CM-7`); configure `system rescue-configuration` and `system archival configuration` (`CP-9`); authenticated NTP (`AU-8`); remote syslog (`AU-2`, `AU-12`); Junos SIRT patch currency (`SI-2`). | `AU-2`, `AU-8`, `AU-12`, `CM-2`, `CM-3`, `CM-6`, `CM-7`, `CP-9`, `SI-2`<br/>`PR.PS-01`, `PR.PS-02`, `PR.PS-04`, `PR.DS-11` | NCSC *Vulnerability management* & *Logging for security purposes*;<br/>Juniper *Hardening Junos Devices* | `UKFS-02`, `UKFS-04`, `UKFS-06`<br/>ISO: `A.8.8`, `A.8.9`, `A.8.13`, `A.8.15`, `A.8.17`, `A.8.32`<br/>CIS: `[CIS-JUNOS-SYSTEM-TBD]` |

### 5.4 Microsoft Windows Servers (`2019 / 2022 / 2025`)

| Check ID & Topic | Technical Assessment Check | NIST 800-53 / 800-41 / CSF 2.0 | NCSC & Microsoft Guidance | UKFS / ISO 27001 Ref / CIS Placeholder |
| :--- | :--- | :--- | :--- | :--- |
| **`WIN-POL-01`**<br/>*(Policy)* | **Host Firewall Profiles & Legacy Protocol Removal**: Windows Defender Firewall enabled across Domain, Private, and Public profiles with default inbound block and logging; SMBv1, LLMNR, and NetBIOS over TCP/IP disabled (`CM-7`). | `SC-7`, `AC-4`, `CM-7`<br/>NIST 800-41 §2.3<br/>`PR.IR-01`, `PR.PS-01` | NCSC *Preventing lateral movement* & *Network security*;<br/>Microsoft *Windows Server Security Baselines* | `UKFS-01`, `UKFS-03`<br/>ISO: `A.8.9`, `A.8.20`, `A.8.22`<br/>CIS: `[CIS-WIN-POLICY-TBD]` |
| **`WIN-ADM-01`**<br/>*(Admin)* | **LAPS, Credential Guard, Kerberos & Remote Access**: Windows LAPS active; LSASS `RunAsPPL` & VBS Credential Guard enabled; NTLMv1/LM disabled & Kerberos AES enforced (`SC-13`); RDP NLA + MFA/jump-host restriction (`AC-17`, `IA-2`); account lockout (`AC-7`) and session timeouts (`AC-12`). | `AC-6`, `AC-7`, `AC-12`, `AC-17`, `IA-2`, `SC-8`, `SC-13`<br/>`PR.AA-03`, `PR.AA-05`, `PR.DS-02` | NCSC *Secure system administration* & *Preventing lateral movement*;<br/>Microsoft *Secured-Core Server* | `UKFS-03`, `UKFS-05`<br/>ISO: `A.5.15`, `A.8.2`, `A.8.5`, `A.8.24`<br/>CIS: `[CIS-WIN-ADMIN-TBD]` |
| **`WIN-SYS-01`**<br/>*(System)* | **Audit Policy, ScriptBlock Logging, EDR, Backups & Patching**: Advanced Audit Policy + PowerShell ScriptBlock (`Event ID 4104`) forwarded to SIEM (`AU-2`, `AU-12`); synchronized Domain/NTP time (`AU-8`); Defender AV/EDR tamper protection (`SI-3`, `SI-4`); verified backups (`CP-9`); cumulative update currency (`SI-2`). | `AU-2`, `AU-8`, `AU-12`, `CM-2`, `CM-6`, `CP-9`, `SI-2`, `SI-3`, `SI-4`<br/>`PR.PS-02`, `PR.PS-04`, `PR.DS-11`, `DE.CM-01` | NCSC *Vulnerability management* & *Logging for security purposes*;<br/>Microsoft *Security Baselines* | `UKFS-02`, `UKFS-04`, `UKFS-06`<br/>ISO: `A.8.7`, `A.8.8`, `A.8.9`, `A.8.13`, `A.8.15`, `A.8.16`, `A.8.17`<br/>CIS: `[CIS-WIN-SYSTEM-TBD]` |

### 5.5 Enterprise Linux Servers (`RHEL / Rocky / Ubuntu LTS / Debian`)

| Check ID & Topic | Technical Assessment Check | NIST 800-53 / 800-41 / CSF 2.0 | NCSC & Linux Vendor Guidance | UKFS / ISO 27001 Ref / CIS Placeholder |
| :--- | :--- | :--- | :--- | :--- |
| **`LNX-POL-01`**<br/>*(Policy)* | **Host Firewall (`nftables`/`firewalld`/`ufw`) & Kernel `sysctl` Network Hardening**: Host firewall active with default-deny ingress; `sysctl` enforces `rp_filter=1`, `tcp_syncookies=1`, disables IPv4/IPv6 source routing, ICMP redirects, and packet forwarding (unless acting as a router). | `SC-7`, `AC-4`, `CM-6`, `CM-7`<br/>NIST 800-41 §2.3<br/>`PR.IR-01`, `PR.PS-01` | NCSC *Preventing lateral movement* & *Network security*;<br/>RHEL / Ubuntu *Security Hardening Guides* | `UKFS-01`, `UKFS-03`<br/>ISO: `A.8.9`, `A.8.20`, `A.8.22`<br/>CIS: `[CIS-LNX-POLICY-TBD]` |
| **`LNX-ADM-01`**<br/>*(Admin)* | **OpenSSH Hardening, `sudo` Least Privilege & PAM Lockout**: `sshd_config` sets `PermitRootLogin no`, key-based auth + MFA, `AllowUsers`/`AllowGroups`, strong ciphers/MACs (`SC-8`, `SC-13`), idle timeout (`ClientAliveInterval`); `sudo` requires `use_pty` and `logfile`; `pam_faillock` enforces lockout (`AC-7`). | `AC-6`, `AC-7`, `AC-12`, `AC-17`, `IA-2`, `SC-8`, `SC-13`<br/>`PR.AA-03`, `PR.AA-05`, `PR.DS-02` | NCSC *Secure system administration*;<br/>RHEL / Ubuntu *OpenSSH & PAM Hardening* | `UKFS-03`, `UKFS-05`<br/>ISO: `A.5.15`, `A.8.2`, `A.8.5`, `A.8.24`<br/>CIS: `[CIS-LNX-ADMIN-TBD]` |
| **`LNX-SYS-01`**<br/>*(System)* | **MAC (`SELinux`/`AppArmor`), `auditd`, FIM, Crypto & Patching**: `SELinux` (`enforcing`) or `AppArmor` active; `auditd` immutable rules (`-e 2`) + remote TLS syslog (`AU-2`, `AU-12`, `SC-8`); `chronyd` authenticated NTP (`AU-8`); `AIDE` integrity monitoring (`SI-4`); unused filesystems/services disabled (`CM-7`); automated security updates (`SI-2`); verified backups (`CP-9`). | `AU-2`, `AU-8`, `AU-12`, `CM-2`, `CM-6`, `CM-7`, `CP-9`, `SC-13`, `SI-2`, `SI-3`, `SI-4`<br/>`PR.PS-02`, `PR.PS-04`, `PR.DS-11`, `DE.CM-01` | NCSC *Vulnerability management* & *Logging for security purposes*;<br/>RHEL / Ubuntu *Hardening Guides* | `UKFS-02`, `UKFS-04`, `UKFS-06`<br/>ISO: `A.8.7`, `A.8.8`, `A.8.9`, `A.8.13`, `A.8.15`, `A.8.16`, `A.8.17`<br/>CIS: `[CIS-LNX-SYSTEM-TBD]` |

---

## 6. What Was Not Used & Mandatory Caveats

### 6.1 What Was Not Used
- **No Nipper Material**: All checks in this catalogue were written independently from public standards and official vendor documentation. Where a Nipper comparison is requested, it compares final assessment results only.
- **No ISO or CIS Text Reproduced**: ISO/IEC 27001/27002 and CIS Benchmark references appear strictly as control numbers or topic placeholders.

### 6.2 Mandatory Assessment Caveats (Include in Every Output Report)
1. **Not Checked Line-by-Line Against Source Documents**: The mappings were compiled while the skill was built from the public sources listed above. Nobody has yet checked them line-by-line against the primary documents, and **Test Library `1.1.0` is marked as `Awaiting Engineer Approval`**.
2. **External Links Need Confirming**: The NCSC and Bank of England (PRA) / FCA publication URLs must be confirmed as current at the time each assessment is executed.
3. **Pre-Customer Sign-Off Gate**: Before any assessment report or output goes to a customer, a qualified firewall/network/systems engineer must verify the technical mappings, and someone with valid **CIS and ISO licences** (plus PCI DSS / SWIFT access where switched on) must replace the placeholders.
