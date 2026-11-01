---
name: server-migration-infrastructure-replication
description: Multi-platform server migration, legacy reverse-engineering, and target-state infrastructure replication skill for Linux (CentOS/AlmaLinux) to Ansible. Use when auditing legacy server state, reverse-engineering Apache/EDL services, preserving auth stacks, or generating Ansible replication playbooks.
---

# Server Migration, Reverse-Engineering & Infrastructure Replication Skill

## 1. Purpose & Architectural Scope

This skill provides a deterministic, multi-phase methodology and technical standards catalogue for reverse-engineering legacy server infrastructure, preserving undocumented co-hosted services, and generating hardened target-state configuration automation.

While structured with explicit extension seams for multi-platform environments (Windows Server via PowerShell DSC, containerization via Docker/Podman, and Cloud-Init), this skill establishes the **Linux-to-Ansible** pipeline as its primary, fully realized reference standard:
- **Source State**: Legacy Linux environments (e.g., CentOS 7 EOL, RHEL 7/8, Ubuntu LTS) running legacy application runtimes (such as Apache `mod_php`), custom cron/timer jobs, co-hosted web endpoints, and mixed authentication.
- **Target State**: Modern, supported enterprise Linux distributions (specifically **AlmaLinux 9** or **RHEL 9**) orchestrated via parameterized **Ansible playbooks**, featuring hardened **PHP-FPM (≥ 8.2.35)**, enforced **SELinux** policies, and zero-downtime cutover verification.

---

## 2. Four-Phase Server Migration Methodology

Every server migration conducted under this framework follows a rigorous four-phase pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│               SERVER MIGRATION & REPLICATION PIPELINE                  │
├─────────────────┬──────────────────┬─────────────────┬─────────────────┤
│    Phase 1:     │     Phase 2:     │    Phase 3:     │    Phase 4:     │
│   Discovery &   │     Reverse      │  Target-State   │ Verification &  │
│    Redaction    │   Engineering    │   Replication   │ Cutover Gates   │
├─────────────────┼──────────────────┼─────────────────┼─────────────────┤
│ • POSIX bash    │ • Apache vhosts  │ • Parameterized │ • Pre-cutover   │
│   collector     │ • EDL pipelines  │   Ansible roles │   test suite    │
│ • Zero mutation │ • Auth stacks    │ • PHP-FPM pool  │ • rsync data    │
│ • Regex edge    │ • Runtime diffs  │ • SELinux rules │ • DNS / proxy   │
│   redaction     │ • CVE exposure   │ • Jinja2 vhosts │ • <3 min rollback│
└─────────────────┴──────────────────┴─────────────────┴─────────────────┘
```

---

## 3. Phase 1: Zero-Dependency Source Discovery & Edge Redaction

Source host discovery must execute using a single, zero-dependency, read-only POSIX/Bash collector (`scripts/linux_server_discovery.sh`) without modifying host state.

### 3.1 Collector Discovery Checklist
The discovery script systematically inspects:
1. **Operating System & Kernel**: `/etc/os-release`, `uname -r`, installed package manifests (`rpm -qa` or `dpkg -l`).
2. **Network & Listening Sockets**: `ss -tulpn` or `netstat -tulpn`, routing table `ip route`, active firewall rules (`iptables-save`, `nft list ruleset`, `firewall-cmd --list-all`).
3. **Web Server Topology**:
   - Virtual host mapping: `httpd -S` or `apache2ctl -S`.
   - Complete configuration tree: `/etc/httpd/conf/httpd.conf`, `/etc/httpd/conf.d/*.conf`, `/etc/nginx/conf.d/*.conf`.
   - SSL/TLS certificate metadata: `openssl x509 -in <cert> -noout -subject -issuer -dates`.
   - `.htaccess` overrides and rewrite rules in web document roots.
4. **Co-Hosted Services & External Dynamic Lists (EDL)**:
   - Cron schedules: `/etc/crontab`, `/etc/cron.*`, `/var/spool/cron/*`.
   - Systemd units & timers: `systemctl list-timers --all`, `/etc/systemd/system/*.timer`.
   - Custom utility scripts: `/usr/local/bin/`, `/usr/local/sbin/`, `/opt/`, `/root/bin/`.
   - File modification timestamps and ownership across `/var/www/` and data directories.
   - Access and error logs: inspect recent request patterns for firewall user-agents, IP addresses, and polling frequency.
5. **Authentication & Identity**:
   - OpenSSH configuration: `/etc/ssh/sshd_config`, authorized keys permissions.
   - PAM configuration: `/etc/pam.d/*` (password-auth, system-auth).
   - Directory integration: `/etc/sssd/sssd.conf`, `/etc/openldap/`, `/etc/krb5.conf`.
   - Local users and groups: `/etc/passwd`, `/etc/group`, `/etc/sudoers`, `/etc/sudoers.d/*`.
   - Web basic auth user databases: `.htpasswd`, `/var/www/*.passwd`.
6. **Application State & Storage**:
   - Application configuration: `/opt/zendto/config/preferences.php`, `zendto.conf`.
   - Databases: SQLite paths (`/var/zendto/zendto.sqlite`), MySQL/MariaDB connection configs.
   - Storage directories: `/var/zendto/drop-offs`, `/var/zendto/library`.
   - Antivirus & scanners: `clamd` status, `/etc/clamd.d/scan.conf`, FreshClam updates.
   - SELinux state: `getenforce`, `sestatus`, custom boolean overrides (`getsebool -a | grep on`).

### 3.2 Mandatory Edge Redaction Rules (`<REDACTED>`)
The collector script must pass all harvested streams through regex filters before writing to disk or stdout:
- **Private Keys**: Strip blocks matching `BEGIN ... PRIVATE KEY` $\rightarrow$ `<REDACTED>`.
- **Password Hashes**: Replace `$6$...` (SHA-512), `$y$...` (yescrypt), `$1$...` (MD5), and Apache htpasswd entries $\rightarrow$ `<REDACTED>`.
- **Database & Application Passwords**: Replace MySQL passwords, PostgreSQL credentials, and PHP configuration arrays (`'password' => '...'`) $\rightarrow$ `<REDACTED>`.
- **Directory Bind Credentials**: Scrub LDAP/Active Directory bind credentials in `sssd.conf`, `preferences.php`, and PAM configs $\rightarrow$ `<REDACTED>`.
- **Shared Secrets & Tokens**: Redact API keys, Cloudflare tokens, and HMAC secrets $\rightarrow$ `<REDACTED>`.

---

## 4. Phase 2: Reverse-Engineering Undocumented Co-Hosted Services

Enterprise servers frequently accrue undocumented auxiliary functions over time. The migration specialist must reverse-engineer all co-hosted services rather than assuming a single application footprint.

### 4.1 Apache Multi-Vhost Reverse-Engineering Matrix
Using `httpd -S` as the baseline topology, map all virtual hosts across port 80 (HTTP) and port 443 (HTTPS):

| Host Header / ServerName | Port | DocumentRoot / Target | Critical Directives & Modules | Discovered Role |
| :--- | :--- | :--- | :--- | :--- |
| `_default_` (`default-nothing.conf`) | 80, 443 | `/var/www/html` | Default catch-all, reject unmatched Host headers | Anti-scanning baseline |
| `portal.example.co.uk` (`zendto.conf`, `zendto-ssl.conf`) | 80, 443 | `/opt/zendto/www` | `php-fpm` proxy handler, TLS cert, drop-off upload limits | Primary ZendTo Web Portal |
| `lists.example.net` (`zz-lists.conf`) | 80 | `/var/www/lists.example.net` | `Options Indexes FollowSymLinks`, `mod_rewrite` empty `%{HTTP_HOST}` redirect to `https://portal.example.co.uk/$1` | Firewall EDL Feed (HTTP) |
| `lists.example.net` (`zz-lists.conf`) | 443 | `/var/www/lists.example.net` | `SSLEngine on`, Cloudflare certs (`cloudflare-example.net.crt`), `Alias /library /var/zendto/library`, WebDAV `<Location /library>` with `AuthType Basic` | Firewall EDL Feed (HTTPS) & WebDAV Storage |

### 4.2 Firewall External Dynamic List (EDL) Reverse-Engineering
When an auxiliary endpoint (such as `lists.example.net`) serves threat intelligence, IP blocklists, or dynamic firewall address objects:
1. **Identify the File Generator**:
   - Check crontabs for curl/wget pipelines, Python scripts, or Threat Intelligence feeds updating `/var/www/lists.example.net/*.txt`.
   - Inspect `/etc/systemd/system/*.service` and `*.timer` for automated list generation.
   - Check file mtime: `ls -lt /var/www/lists.example.net` to ascertain update frequency (hourly, daily, ad-hoc).
2. **Access Patterns & Firewall Consumers**:
   - Analyze Apache access logs for IP addresses querying list files (e.g. Palo Alto PAN-OS, FortiGate FortiOS, or Check Point external dynamic list pullers).
   - Note specific User-Agents (e.g. `PanOS-EDL/1.0`, `FortiGate-Feed`) and request intervals.
3. **Target Replication Requirement**:
   - The document root, update jobs, directory indexing options (`Indexes FollowSymLinks`), and file permissions must be preserved on the target host to prevent firewall rule drops or connectivity timeouts.

### 4.3 WebDAV `/library` Reverse-Engineering
- Directive: `Alias /library /var/zendto/library`
- Scope: `<Location /library>`
  - `DAV on`
  - `AuthType Basic`
  - `AuthName "ZendTo Library"`
  - `AuthUserFile /var/www/library.passwd`
  - `Require valid-user`
- Action: Preserve basic authentication database, directory write permissions, and SELinux boolean `httpd_unified` / contexts on `/var/zendto/library`.

---

## 5. Short-Term Exposure Mitigations for PHP2Shell (CVE-2026-109618 / 109619)

When legacy servers run vulnerable PHP runtimes (such as `mod_php 8.2.20` on CentOS 7 where packages cannot be updated beyond Remi EL7 limits), apply four immediate mitigation layers prior to full cutover:

1. **Cloudflare WAF / Reverse Proxy Rule**:
   - Enforce an edge WAF rule blocking HTTP requests containing malicious multipart boundary payloads, PHP serialization headers, or suspicious query arguments targeted at PHP2Shell exploits.
   - Restrict origin traffic to Cloudflare IP ranges (`cf-connecting-ip` verification).
2. **Apache Request Header & Path Filtering (`mod_rewrite`)**:
   - Deploy emergency rewrite rules in `/etc/httpd/conf.d/00-cve-mitigation.conf`:
     ```apache
     RewriteEngine On
     RewriteCond %{HTTP_USER_AGENT} (php2shell|vulnerability-scanner|sqlmap) [NC,OR]
     RewriteCond %{QUERY_STRING} (auto_prepend_file|allow_url_include|disable_functions) [NC]
     RewriteRule .* - [F,L]
     ```
3. **Hardened `php.ini` Settings**:
   - Ensure `allow_url_fopen = Off`, `allow_url_include = Off`, `expose_php = Off`.
   - Set `disable_functions = exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source`.
4. **Target Migration Prioritisation**:
   - Rapidly transition to AlmaLinux 9 running official PHP-FPM (≥ 8.2.35) where the vulnerability is cleanly patched upstream.

---

## 6. Phase 3: Target-State Replication Architecture (AlmaLinux 9 & Ansible)

The target infrastructure must be provisioned and configured using an idempotent Ansible replication suite (`ReplicationAnsible/`).

### 6.1 System Architecture & Package Baselines
- **Operating System**: AlmaLinux 9.x (Kernel 5.14+, systemd 252+).
- **Web Server**: Apache HTTP Server 2.4.57+ (Event MPM).
- **PHP Runtime**: PHP-FPM 8.2.35+ via Remi EL9 repository (`remi-8.2` or AppStream module). Legacy `mod_php` (`httpd-mmn`) is strictly removed/uninstalled.
- **Application**: ZendTo 6.15-8 via official RPM installer.
- **Antivirus**: ClamAV 1.0+ (`clamd@scan`, `clamd-update`).
- **SELinux**: `Enforcing` mode throughout.

### 6.2 Ansible Role Decomposition
```
ReplicationAnsible/
├── ansible.cfg
├── inventory/
│   └── hosts.ini
├── group_vars/
│   ├── all.yml
│   └── web_servers.yml
├── playbook.yml
└── roles/
    ├── common/          # Baseline packages, chrony, firewalld, sysctl
    ├── httpd/           # Apache installation, event MPM, vhost templates
    ├── php_fpm/         # Remi repository, PHP-FPM 8.2.35+, pools, upload limits
    ├── zendto/          # Official installer, preferences.php, sqlite/mysql, drop-offs
    ├── clamav/          # clamd@scan, clamd-update, SELinux clamd booleans
    ├── selinux/         # SELinux contexts, fcontexts, booleans
    └── lists_edl/       # /var/www/lists.example.net, EDL generator jobs, timers
```

### 6.3 SELinux Policy & Booleans for Target Host
- **Required Booleans**:
  - `setsebool -P httpd_can_network_connect 1` (Allows ZendTo to communicate with LDAP/AD and SMTP relays).
  - `setsebool -P httpd_can_sendmail 1` (Allows PHP-FPM to send drop-off notification emails).
  - `setsebool -P antivirus_can_scan_system 1` (Allows ClamAV to inspect uploaded drop-offs in `/var/zendto/drop-offs`).
- **File Contexts (`semanage fcontext`)**:
  - `/var/zendto(/.*)?` $\rightarrow$ `system_u:object_r:httpd_sys_rw_content_t:s0`
  - `/var/www/lists\.enterprisecloud\.net(/.*)?` $\rightarrow$ `system_u:object_r:httpd_sys_content_t:s0`
  - `/var/www/library\.passwd` $\rightarrow$ `system_u:object_r:httpd_sys_content_t:s0`

---

## 7. Phase 4: Pre-Cutover Verification & Cutover Runbook

Prior to traffic migration, execute automated validation gates.

### 7.1 Pre-Cutover Validation Checklist
1. **ZendTo Authentication & UI**:
   - Web interface loads on `https://portal.example.co.uk/` with valid TLS.
   - Local administrator authentication succeeds.
   - Directory authentication (LDAP/AD/SSSD) binds and validates test credentials.
2. **File Drop-Off & ClamAV Integration**:
   - Upload clean test file $\rightarrow$ Verify drop-off created in `/var/zendto/drop-offs` and SQLite index updated.
   - Upload EICAR test string $\rightarrow$ Verify ClamAV (`clamd@scan`) triggers and rejects upload.
   - Download test drop-off with claim ID $\rightarrow$ Verify payload checksum matches.
3. **WebDAV `/library` Service**:
   - `curl -u <user>:<pass> https://portal.example.co.uk/library/` returns HTTP 200/207.
   - Unauthenticated request returns HTTP 401 Unauthorized.
4. **Firewall External Dynamic List (EDL) Retrieval**:
   - `curl -s -k https://lists.example.net/blocked-ips.txt` returns HTTP 200 with address list.
   - Empty `Host` header request redirects with HTTP 301 to `https://portal.example.co.uk/`.
   - Automated EDL generator crontab/timer executes successfully and updates lists.

### 7.2 Cutover Execution & Rollback Procedure
- **Cutover Window (T-0)**:
  1. Freeze legacy drop-offs (`preferences.php` maintenance mode).
  2. Final rsync of `/var/zendto/drop-offs`, `/var/zendto/zendto.sqlite`, and `/var/www/lists.example.net`.
  3. Update DNS record / Cloudflare origin IP to point to the new AlmaLinux 9 host.
  4. Perform post-cutover smoke tests.
- **Guaranteed < 3-Minute Rollback Plan**:
  1. Revert Cloudflare origin IP / DNS A-record to `legacy-web-01.corp.example.com` IP.
  2. Unfreeze maintenance mode on legacy host.
  3. Verify legacy web traffic resumes.

---

## 8. Multi-Platform Extension Seams

To extend this skill to non-Linux or non-Ansible targets, implement adapters at the following clean seams:
1. **Windows Server Target**:
   - Discovery: `scripts/windows_server_discovery.ps1` using CIM/WMI.
   - Target Automation: PowerShell DSC configurations or `ansible.windows` playbooks.
   - IIS Reverse Engineering: `Get-WebVirtualDirectory`, `Get-WebBinding`, Application Pool identity extraction.
2. **Container Target (Docker / Podman / Kubernetes)**:
   - Target Automation: Containerfile/Dockerfile with multi-stage builds.
   - Ingestion: Extract static vhosts to Nginx/Caddy container configs, wrap PHP application in standard FPM base image.
3. **Cloud-Init / Immutable Target**:
   - Target Automation: `#cloud-config` user-data templates executing automated bootstrap.
