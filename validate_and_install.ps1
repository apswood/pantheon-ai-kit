<#
.SYNOPSIS
    Automated validator and bootstrap installer for PANTHEON AI Agent and Skills Setup Kit.
.DESCRIPTION
    Validates kit file integrity, YAML frontmatter compliance, size boundaries, and executes
    credential and custom blocklist leak scans natively in PowerShell (compatible with PowerShell 5.1 and 7+).
    Zero reversible organization-specific text is stored in the upstream repository.
    Optionally builds a local custom $EncodedRules keyword library (.custom_blocklist.json, gitignored)
    and bootstraps the kit into a target Antigravity workspace directory.
.PARAMETER ValidateOnly
    Runs validation checks and exits without installing.
.PARAMETER TargetWorkspaceDir
    Target directory path where the starter kit will be installed. Alias: TargetWorkspace.
.PARAMETER Install
    Explicit flag indicating installation mode into TargetWorkspaceDir.
.PARAMETER Force
    Overwrites destination files during installation without confirmation.
.PARAMETER ConfigureCustomScanner
    Launches the interactive builder to add custom organization keywords/patterns to .custom_blocklist.json ($EncodedRules).
.PARAMETER SkipCustomScanner
    Skips the optional interactive prompt for configuring custom scanner keywords during setup.
.EXAMPLE
    pwsh -NoProfile -File validate_and_install.ps1 -ValidateOnly
.EXAMPLE
    pwsh -NoProfile -File validate_and_install.ps1 -ConfigureCustomScanner
.EXAMPLE
    pwsh -NoProfile -File validate_and_install.ps1 -TargetWorkspaceDir "C:\Projects\MySupportProject"
#>
[CmdletBinding()]
param(
    [switch]$ValidateOnly,

    [Alias('TargetWorkspace')]
    [string]$TargetWorkspaceDir,

    [switch]$Install,

    [switch]$Force,

    [switch]$ConfigureCustomScanner,

    [switch]$SkipCustomScanner
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  PANTHEON AI SETUP KIT - POWERSHELL VALIDATOR & BOOTSTRAP            " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Resolve Kit Root Directory
$KitRoot = $PSScriptRoot
if (-not $KitRoot -or -not (Test-Path -LiteralPath (Join-Path $KitRoot "GEMINI.md"))) {
    $KitRoot = (Get-Location).Path
}
if (-not (Test-Path -LiteralPath (Join-Path $KitRoot "GEMINI.md"))) {
    $subDir = Join-Path $KitRoot "Antigravity_Governance_Setup_Kit"
    if (Test-Path -LiteralPath (Join-Path $subDir "GEMINI.md")) {
        $KitRoot = $subDir
    }
}

Write-Host "Kit Root: $KitRoot`n" -ForegroundColor Gray

$CustomBlocklistFileName = ".custom_blocklist.json"

function Reverse-String ([string]$s) {
    $chars = $s.ToCharArray()
    [Array]::Reverse($chars)
    return (-join $chars)
}

function ConvertTo-ReversedBase64 ([string]$PlainText) {
    $rev = Reverse-String $PlainText
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($rev)
    return [System.Convert]::ToBase64String($bytes)
}

function Ensure-GitignoreEntry ([string]$WorkspaceDir, [string]$EntryName) {
    $giFile = Join-Path $WorkspaceDir ".gitignore"
    if (Test-Path -LiteralPath $giFile) {
        $giRaw = Get-Content -LiteralPath $giFile -Raw -Encoding UTF8
        if ($giRaw -notmatch [regex]::Escape($EntryName)) {
            $appendText = "`r`n# Local company-specific encoded leak scanner keyword library`r`n$EntryName`r`n"
            Add-Content -LiteralPath $giFile -Value $appendText -Encoding UTF8
            Write-Host "  [GITIGNORE] Added '$EntryName' to .gitignore ($giFile)" -ForegroundColor Green
        }
    } else {
        Set-Content -LiteralPath $giFile -Value ".env`r`n.venv/`r`n$EntryName`r`n" -Encoding UTF8
        Write-Host "  [GITIGNORE] Created .gitignore with '$EntryName'" -ForegroundColor Green
    }
}

function Invoke-CustomScannerSetup ([string]$WorkspaceDir) {
    $libPath = Join-Path $WorkspaceDir $CustomBlocklistFileName
    $existingRules = [System.Collections.Generic.List[object]]::new()
    if (Test-Path -LiteralPath $libPath) {
        try {
            $parsed = Get-Content -LiteralPath $libPath -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($null -ne $parsed) {
                foreach ($item in @($parsed)) {
                    if ($null -ne $item.NameB64 -and $null -ne $item.PatB64) {
                        $existingRules.Add(@{ NameB64 = [string]$item.NameB64; PatB64 = [string]$item.PatB64 })
                    }
                }
            }
        } catch {
            Write-Host "  [WARN] Could not parse existing $CustomBlocklistFileName; starting fresh list." -ForegroundColor Yellow
        }
    }

    Write-Host "`n----------------------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "  CUSTOM KEYWORD LEAK SCANNER BUILDER (`$EncodedRules Library)" -ForegroundColor Cyan
    Write-Host "----------------------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "  Currently loaded custom rules in ${CustomBlocklistFileName}: $($existingRules.Count)" -ForegroundColor Gray
    Write-Host "  Enter organization names, internal domains, colleague names, or" -ForegroundColor Gray
    Write-Host "  resource identifiers to build your local `$EncodedRules library." -ForegroundColor Gray
    Write-Host "  Each entry is Reversed UTF-8 + Base64 encoded into $CustomBlocklistFileName" -ForegroundColor Gray
    Write-Host "  and automatically added to .gitignore (never committed upstream)." -ForegroundColor Gray
    Write-Host "  Press Enter on an empty line when finished.`n" -ForegroundColor Gray

    $added = 0
    while ($true) {
        $label = Read-Host "  Keyword / Label to block (or press Enter to finish)"
        if ([string]::IsNullOrWhiteSpace($label)) { break }
        $label = $label.Trim()

        $customPat = Read-Host "  Optional custom regex (or press Enter to auto-generate word-boundary regex)"
        if ([string]::IsNullOrWhiteSpace($customPat)) {
            $escaped = [regex]::Escape($label) -replace '\\ ', '(?:\s+|\.)'
            $patStr = "\b$escaped\b"
        } else {
            $patStr = $customPat.Trim()
        }

        $nameB64 = ConvertTo-ReversedBase64 $label
        $patB64 = ConvertTo-ReversedBase64 $patStr
        $existingRules.Add(@{ NameB64 = $nameB64; PatB64 = $patB64 })
        $added++
        Write-Host "    + Added encoded rule (#$($existingRules.Count)): NameB64='$nameB64'" -ForegroundColor Green
    }

    if ($added -gt 0 -or (Test-Path -LiteralPath $libPath)) {
        $jsonOut = ConvertTo-Json -InputObject @($existingRules) -Depth 4
        Set-Content -LiteralPath $libPath -Value $jsonOut -Encoding UTF8
        Ensure-GitignoreEntry -WorkspaceDir $WorkspaceDir -EntryName $CustomBlocklistFileName
        Write-Host "  [OK] Saved $($existingRules.Count) encoded rule(s) to $libPath (gitignored)." -ForegroundColor Green
    } else {
        Write-Host "  [SKIP] No custom keywords added." -ForegroundColor Gray
    }
}

if ($ConfigureCustomScanner) {
    $targetForScanner = if ($TargetWorkspaceDir) { $TargetWorkspaceDir } else { $KitRoot }
    Invoke-CustomScannerSetup -WorkspaceDir $targetForScanner
}

# Upstream Generic Credential & Secret Patterns (Zero reversible company/personal text in upstream repo)
$GenericSecretRules = @(
    @{ Label = "PEM Private Key Header"; Pattern = '-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----' },
    @{ Label = "GitHub Personal Access Token"; Pattern = '\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,255}\b' },
    @{ Label = "AWS Access Key ID"; Pattern = '\b(?:AKIA|ASIA)[0-9A-Z]{16}\b' },
    @{ Label = "Slack API Token"; Pattern = '\bxox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*\b' },
    @{ Label = "Hardcoded OAuth Client Secret"; Pattern = '(?:client_secret|tenant_secret)\s*[:=]\s*[''"][A-Za-z0-9~._\-]{32,64}[''"]' }
)

# Local Custom Encoded Blocklist Rules ($EncodedRules) - Empty in upstream repo; populated from local .custom_blocklist.json if present
$EncodedRules = @()
$LocalBlocklistPath = Join-Path $KitRoot $CustomBlocklistFileName
if (Test-Path -LiteralPath $LocalBlocklistPath) {
    try {
        $loadedJson = Get-Content -LiteralPath $LocalBlocklistPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($null -ne $loadedJson) {
            foreach ($entry in @($loadedJson)) {
                if ($null -ne $entry.NameB64 -and $null -ne $entry.PatB64) {
                    $EncodedRules += @{ NameB64 = [string]$entry.NameB64; PatB64 = [string]$entry.PatB64 }
                }
            }
        }
    } catch {
        Write-Host "  [WARN] Could not parse local ${CustomBlocklistFileName}: $_" -ForegroundColor Yellow
    }
}

$Issues = [System.Collections.Generic.List[string]]::new()

# STAGE 1: File Existence and Byte Limit Check (24 canonical files)
Write-Host "[STAGE 1/4] Checking canonical file structure and byte limits..." -ForegroundColor Yellow
$RequiredFiles = @(
    "README.md",
    "ANTIGRAVITY_SETUP_GUIDE.md",
    "ANTIGRAVITY_DOCS.html",
    "GEMINI.md",
    ".env.template",
    ".gitignore",
    "setup.py",
    "build_docs.py",
    "validate_kit.py",
    "validate_and_install.ps1",
    ".agents/agents/aegis_best_practice/agent.md",
    ".agents/agents/atlas_architecture/agent.md",
    ".agents/agents/sage_governance/agent.md",
    ".agents/agents/sentinel_security/agent.md",
    ".agents/agents/spark_disruptor/agent.md",
    ".agents/skills/infrastructure-best-practice-analyser/SKILL.md",
    ".agents/skills/productivity-workload-governance/SKILL.md",
    ".agents/skills/quality-audit-governance/SKILL.md",
    ".agents/skills/support-team-governance-analytics-coaching/SKILL.md",
    ".agents/skills/teams-standup-digest-notifier/SKILL.md",
    ".agents/skills/ticket-backlog-governance/SKILL.md",
    "Governance_Framework/AEGIS_Agent_System_Prompt.md",
    "Governance_Framework/SAGE_Agent_System_Prompt.md",
    ".agents/rules/sage-governance-prompt.md"
)

foreach ($relPath in $RequiredFiles) {
    $fullPath = Join-Path $KitRoot $relPath
    if (-not (Test-Path -LiteralPath $fullPath)) {
        $Issues.Add("Missing required file: $relPath")
    } else {
        $item = Get-Item -LiteralPath $fullPath
        if ($item.Length -eq 0) {
            $Issues.Add("File is empty (0 bytes): $relPath")
        }
    }
}

# GEMINI.md boundary test (strictly under 24,000 bytes)
$geminiFile = Join-Path $KitRoot "GEMINI.md"
if (Test-Path -LiteralPath $geminiFile) {
    $geminiLen = (Get-Item -LiteralPath $geminiFile).Length
    if ($geminiLen -ge 24000) {
        $Issues.Add("GEMINI.md exceeds 24,000 byte limit: $geminiLen bytes (max: 23,999)")
    }
}

if ($Issues.Count -eq 0) {
    Write-Host "  [PASS] All 24 canonical files exist and GEMINI.md size is within limits." -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Detected $($Issues.Count) structure/size issue(s)." -ForegroundColor Red
}

# STAGE 2: YAML Frontmatter Verification
Write-Host "`n[STAGE 2/4] Verifying agent and skill YAML frontmatter schemas..." -ForegroundColor Yellow
$agentsDir = Join-Path $KitRoot ".agents"
$mdCount = 0

if (Test-Path -LiteralPath $agentsDir) {
    $agentFiles = Get-ChildItem -Path (Join-Path $agentsDir "agents") -Recurse -Filter "*.md" -File
    $skillFiles = Get-ChildItem -Path (Join-Path $agentsDir "skills") -Recurse -Filter "*.md" -File
    $allMd = @($agentFiles) + @($skillFiles)

    foreach ($file in $allMd) {
        $mdCount++
        $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
        if ($content -match '^---\s*[\r\n]+([\s\S]*?)[\r\n]+---\s*([\s\S]*)$') {
            $fmBlock = $matches[1]
            $body = $matches[2].Trim()

            if ($fmBlock -notmatch 'name:\s*\S+') {
                $Issues.Add("$($file.Name): Missing 'name' in YAML frontmatter.")
            }
            if ($fmBlock -notmatch 'description:\s*\S+') {
                $Issues.Add("$($file.Name): Missing 'description' in YAML frontmatter.")
            }
            if ($body.Length -lt 40) {
                $Issues.Add("$($file.Name): Instruction body content after frontmatter is too short or empty.")
            }
        } else {
            $Issues.Add("$($file.Name): Missing valid opening/closing '---' frontmatter delimiters.")
        }
    }
    Write-Host "  [PASS] Verified $mdCount agent and skill markdown definitions." -ForegroundColor Green
} else {
    $Issues.Add("Missing .agents directory in kit root.")
    Write-Host "  [FAIL] Missing .agents directory." -ForegroundColor Red
}

# STAGE 3: De-Identification & Secret Leak Scan
Write-Host "`n[STAGE 3/4] Scanning for live credentials and custom blocklist leaks ($($GenericSecretRules.Count) built-in secret rules + $($EncodedRules.Count) local custom rule(s))..." -ForegroundColor Yellow
$AllFiles = Get-ChildItem -Path $KitRoot -Recurse -File | Where-Object {
    $_.Name -ne "validate_and_install.ps1" -and
    $_.Name -ne "validate_kit.py" -and
    $_.Name -ne $CustomBlocklistFileName -and
    $_.Name -ne ".leak_blocklist.json" -and
    $_.Extension -ne ".zip" -and
    $_.Extension -ne ".pyc" -and
    $_.FullName -notmatch '[\\/]\.git([\\/]|$)' -and
    $_.FullName -notmatch '[\\/]\.venv([\\/]|$)' -and
    $_.FullName -notmatch '[\\/]__pycache__([\\/]|$)'
}

$decodedRules = @()
foreach ($r in $EncodedRules) {
    $tokRaw = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($r.NameB64))
    $patRaw = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($r.PatB64))
    $tok = Reverse-String $tokRaw
    $pat = Reverse-String $patRaw
    $decodedRules += @{ Token = $tok; Pattern = $pat }
}

$leakCount = 0
foreach ($file in $AllFiles) {
    $lines = Get-Content -LiteralPath $file.FullName -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($null -eq $lines) { continue }

    $lineNum = 1
    foreach ($line in $lines) {
        $lineLower = $line.ToLower()
        foreach ($gRule in $GenericSecretRules) {
            if ($line -cmatch $gRule.Pattern) {
                $leakCount++
                $rel = $file.FullName.Substring($KitRoot.Length).TrimStart('\', '/')
                $snippet = $line.Trim()
                if ($snippet.Length -gt 80) { $snippet = $snippet.Substring(0, 80) }
                $Issues.Add("LEAK: $rel : line $lineNum matched generic rule ($($gRule.Label)) -> $snippet")
            }
        }
        for ($i = 0; $i -lt $decodedRules.Count; $i++) {
            $rule = $decodedRules[$i]
            $hasMatch = $lineLower.Contains($rule.Token.ToLower()) -or ($line -match $rule.Pattern)
            if ($hasMatch) {
                $leakCount++
                $rel = $file.FullName.Substring($KitRoot.Length).TrimStart('\', '/')
                $snippet = $line.Trim()
                if ($snippet.Length -gt 80) { $snippet = $snippet.Substring(0, 80) }
                $Issues.Add("LEAK: $rel : line $lineNum matched custom rule #$($i + 1) -> $snippet")
            }
        }
        $lineNum++
    }
}

if ($leakCount -eq 0) {
    Write-Host "  [PASS] Zero credential or blocklisted leaks detected across $($AllFiles.Count) files." -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Detected $leakCount sensitive leak occurrence(s)." -ForegroundColor Red
}

# STAGE 4: Configuration Hygiene
Write-Host "`n[STAGE 4/4] Verifying configuration templates and .gitignore..." -ForegroundColor Yellow
$giPath = Join-Path $KitRoot ".gitignore"
if (Test-Path -LiteralPath $giPath) {
    $giText = Get-Content -LiteralPath $giPath -Raw -Encoding UTF8
    if ($giText -notmatch '\.env') { $Issues.Add(".gitignore must contain '.env'") }
    if ($giText -notmatch '\.venv' -and $giText -notmatch 'venv') { $Issues.Add(".gitignore must contain '.venv'") }
    if ($giText -notmatch '\.custom_blocklist') { $Issues.Add(".gitignore must contain '.custom_blocklist.json'") }
} else {
    $Issues.Add("Missing .gitignore file in kit root.")
}

$tplPath = Join-Path $KitRoot ".env.template"
if (Test-Path -LiteralPath $tplPath) {
    $tplText = Get-Content -LiteralPath $tplPath -Raw -Encoding UTF8
    if ($tplText -notmatch '<' -or $tplText -notmatch '>') {
        $Issues.Add(".env.template should use bracketed placeholders like <YOUR_VALUE>")
    }
} else {
    $Issues.Add("Missing .env.template file in kit root.")
}

# Summary Verdict
Write-Host "`n======================================================================" -ForegroundColor Cyan
if ($Issues.Count -gt 0) {
    Write-Host "VALIDATION FAILED with $($Issues.Count) issue(s):" -ForegroundColor Red
    foreach ($iss in $Issues) {
        Write-Host "  - $iss" -ForegroundColor Red
    }
    Write-Host "======================================================================" -ForegroundColor Cyan
    exit 1
}

Write-Host "ALL VALIDATION CHECKS PASSED! (Exit Code 0)" -ForegroundColor Green
Write-Host "Status: OK - The kit is clean, fully de-identified, and structurally valid." -ForegroundColor Green

# Installation / Bootstrap Phase
$isInstall = ($Install -or ($TargetWorkspaceDir -and -not $ValidateOnly))

if ($isInstall) {
    if (-not $TargetWorkspaceDir) {
        Write-Host "Error: Target workspace directory must be specified for installation." -ForegroundColor Red
        exit 1
    }

    Write-Host "`n======================================================================" -ForegroundColor Cyan
    Write-Host " [BOOTSTRAP] Installing Starter Kit into: $TargetWorkspaceDir" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Cyan

    if (-not (Test-Path -LiteralPath $TargetWorkspaceDir)) {
        New-Item -ItemType Directory -Path $TargetWorkspaceDir -Force | Out-Null
        Write-Host "  Created target workspace directory." -ForegroundColor Green
    }

    $ItemsToCopy = @(
        ".agents",
        "Governance_Framework",
        "GEMINI.md",
        ".env.template",
        ".gitignore",
        "ANTIGRAVITY_SETUP_GUIDE.md",
        "ANTIGRAVITY_DOCS.html",
        "README.md",
        "setup.py",
        "build_docs.py",
        "validate_kit.py",
        "validate_and_install.ps1"
    )

    foreach ($item in $ItemsToCopy) {
        $srcPath = Join-Path $KitRoot $item
        $dstPath = Join-Path $TargetWorkspaceDir $item
        if (Test-Path -LiteralPath $srcPath) {
            if ($Force) {
                Copy-Item -Path $srcPath -Destination $dstPath -Recurse -Force
            } else {
                Copy-Item -Path $srcPath -Destination $dstPath -Recurse
            }
            Write-Host "  Copied: $item" -ForegroundColor Green
        }
    }

    # Instantiate .env from template if missing
    $destEnv = Join-Path $TargetWorkspaceDir ".env"
    $destTpl = Join-Path $TargetWorkspaceDir ".env.template"
    if ((Test-Path -LiteralPath $destTpl) -and (-not (Test-Path -LiteralPath $destEnv))) {
        Copy-Item -Path $destTpl -Destination $destEnv
        Write-Host "  Created initial .env from template (configure credentials before running)." -ForegroundColor Green
    }

    # Optional & Skippable Custom Keyword Leak Scanner Setup ($EncodedRules)
    if (-not $SkipCustomScanner -and -not $ConfigureCustomScanner -and [Environment]::UserInteractive) {
        Write-Host "`n[OPTIONAL] Would you like to set up a custom organization/keyword leak scanner" -ForegroundColor Yellow
        $ans = Read-Host "           to build a library of custom `$EncodedRules (.custom_blocklist.json)? [y/N - Press Enter to skip]"
        if ($ans -match '^(y|yes)$') {
            Invoke-CustomScannerSetup -WorkspaceDir $TargetWorkspaceDir
        } else {
            Write-Host "  [SKIP] Skipped custom keyword scanner setup (run with -ConfigureCustomScanner anytime)." -ForegroundColor Gray
        }
    }

    Write-Host "`nInstallation Completed Successfully!" -ForegroundColor Green
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Open target workspace in Google Antigravity." -ForegroundColor Gray
    Write-Host "  2. Populate instance credentials in .env." -ForegroundColor Gray
    Write-Host "  3. Invoke AEGIS, ATLAS, SAGE, SENTINEL, or SPARK advisory agents." -ForegroundColor Gray
}

Write-Host "======================================================================" -ForegroundColor Cyan
exit 0
