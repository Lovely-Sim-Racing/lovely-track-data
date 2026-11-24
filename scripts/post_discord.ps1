# Posts a summary of a push to v2.0.0 to Discord: new tracks, fixes, pit loss updates and the contributors to thank.
# Run by .github/workflows/discord-post.yml; works in Windows PowerShell 5.1 and pwsh 7.
#   ./scripts/post_discord.ps1 -Before <sha> -After <sha> [-DryRun]
# Env: DISCORD_WEBHOOK_URL (no webhook = print only), DISCORD_ROLE_ID (optional, a role to ping),
#      GITHUB_TOKEN (optional, for the GitHub API),
#      GITHUB_REPOSITORY (defaults to Lovely-Sim-Racing/lovely-track-data), GIT (git executable, defaults to "git").
param(
    [string]$Before,
    [Parameter(Mandatory = $true)][string]$After,
    [string]$Branch = "v2.0.0",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$git = if ($env:GIT) { $env:GIT } else { "git" }
$repo = if ($env:GITHUB_REPOSITORY) { $env:GITHUB_REPOSITORY } else { "Lovely-Sim-Racing/lovely-track-data" }
$color = 0x2B98FB # Lovely Blue
$dot = [string][char]0x00B7      # middle dot (kept out of the file so it stays ASCII for Windows PowerShell)
$ellipsis = [string][char]0x2026

$simNames = @{
    "assettocorsa"             = "AC"
    "assettocorsacompetizione" = "ACC"
    "automobilista2"           = "AMS2"
    "f12024"                   = "F1 24"
    "f12025"                   = "F1 25"
    "iracing"                  = "iRacing"
    "lmu"                      = "LMU"
}

function Invoke-Git([string[]]$GitArgs) {
    $out = & $git @GitArgs
    if ($LASTEXITCODE -ne 0) { throw "git $($GitArgs -join ' ') failed" }
    return $out
}

function Get-GitHub([string]$Path) {
    $headers = @{ "User-Agent" = "lovely-track-data-discord"; "Accept" = "application/vnd.github+json" }
    if ($env:GITHUB_TOKEN) { $headers["Authorization"] = "Bearer $($env:GITHUB_TOKEN)" }
    return Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/$Path" -Headers $headers
}

function Get-TrackName([string]$Ref, [string]$Path) {
    try {
        $raw = (& $git show "${Ref}:$Path") -join "`n"
        $name = ($raw | ConvertFrom-Json).name
        if ($name) { return $name }
    } catch { }
    return [System.IO.Path]::GetFileNameWithoutExtension($Path)
}

function Limit-Text([string]$Text, [int]$Max) {
    if ($Text.Length -le $Max) { return $Text }
    $cut = $Text.Substring(0, $Max - 2)
    $nl = $cut.LastIndexOf("`n")
    if ($nl -gt 0) { $cut = $cut.Substring(0, $nl) }
    return "$cut`n$ellipsis"
}

# The range this push brought in. A new branch or a force push has no usable "before": fall back to the last commit.
$zero = "0000000000000000000000000000000000000000"
$haveBefore = $false
if ($Before -and $Before -ne $zero) {
    & $git cat-file -e "$Before^{commit}" 2>$null
    if ($LASTEXITCODE -eq 0) {
        & $git merge-base --is-ancestor $Before $After
        $haveBefore = ($LASTEXITCODE -eq 0)
    }
}
if (-not $haveBefore) { $Before = "$After~1" }
$Before = (Invoke-Git @("rev-parse", "$Before^{commit}"))
$After = (Invoke-Git @("rev-parse", "$After^{commit}"))

# Track files that changed (the manifest is generated, so it's left out).
$changes = @()
foreach ($line in (Invoke-Git @("diff", "--no-renames", "--name-status", $Before, $After, "--", "data"))) {
    $parts = $line -split "`t"
    $status = $parts[0].Substring(0, 1)
    $path = $parts[1]
    if ($path -notmatch '^data/([^/]+)/[^/]+\.json$') { continue }
    $sim = $Matches[1]
    $ref = if ($status -eq "D") { $Before } else { $After }
    $changes += [pscustomobject]@{
        Status = $status
        Path   = $path
        Sim    = $sim
        SimName = $(if ($simNames.ContainsKey($sim)) { $simNames[$sim] } else { $sim })
        Name   = Get-TrackName $ref $path
    }
}
if ($changes.Count -eq 0) { Write-Host "No track files changed: nothing to post."; exit 0 }

# Pull requests in the range: merge commits ("Merge pull request #N from ...") and squash merges ("Title (#N)").
$prNumbers = @()
foreach ($subject in (Invoke-Git @("log", "--format=%s", "$Before..$After"))) {
    if ($subject -match '^Merge pull request #(\d+) ') { $prNumbers += [int]$Matches[1] }
    elseif ($subject -match '\(#(\d+)\)$') { $prNumbers += [int]$Matches[1] }
}
$prs = @()
foreach ($n in ($prNumbers | Sort-Object -Unique)) {
    try {
        $pr = Get-GitHub "pulls/$n"
        $files = @(Get-GitHub "pulls/$n/files?per_page=100" | ForEach-Object { $_.filename })
        $fromFork = ($pr.head.repo -eq $null) -or ($pr.head.repo.full_name -ne $repo)
        $prs += [pscustomobject]@{
            Number  = $n
            Url     = $pr.html_url
            Login   = $pr.user.login
            Profile = $pr.user.html_url
            IsBot   = ($pr.user.type -eq "Bot") -or ($pr.user.login -like "*[bot]")
            PitLoss = $pr.head.ref -like "pit-loss/*"
            Fork    = $fromFork
            Files   = $files
        }
    } catch {
        Write-Host "::warning::Couldn't read pull request #${n}: $($_.Exception.Message)"
    }
}

function Format-PrLinks($List) {
    if (-not $List) { return "" }
    return " " + (($List | ForEach-Object { "[#$($_.Number)]($($_.Url))" }) -join " ")
}

# Sort each change into the sections. A file the pit loss PR touched is a pit loss update; anything else a contributor
# (or a direct commit) changed is a new track, a fix or a removal.
$newLines = @(); $fixLines = @(); $removedLines = @(); $pitChanges = @(); $pitPrs = @()
foreach ($c in ($changes | Sort-Object SimName, Name)) {
    $touching = @($prs | Where-Object { $_.Files -contains $c.Path })
    $pit = @($touching | Where-Object { $_.PitLoss })
    $other = @($touching | Where-Object { -not $_.PitLoss })
    if ($pit.Count -gt 0) { $pitChanges += $c; $pitPrs += $pit }
    if ($pit.Count -gt 0 -and $other.Count -eq 0) { continue }
    $line = "$($c.SimName) $dot $($c.Name)$(Format-PrLinks $other)"
    switch ($c.Status) {
        "A" { $newLines += $line }
        "D" { $removedLines += $line }
        default { $fixLines += $line }
    }
}

$fields = @()
if ($newLines.Count -gt 0) {
    $title = if ($newLines.Count -eq 1) { "New track" } else { "New tracks" }
    $fields += [ordered]@{ name = $title; value = (Limit-Text ($newLines -join "`n") 1024); inline = $false }
}
if ($fixLines.Count -gt 0) {
    $fields += [ordered]@{ name = "Fixes"; value = (Limit-Text ($fixLines -join "`n") 1024); inline = $false }
}
if ($pitChanges.Count -gt 0) {
    $bySim = $pitChanges | Group-Object SimName | Sort-Object Name
    $lines = @($bySim | ForEach-Object { "**$($_.Name)** " + (($_.Group | ForEach-Object { $_.Name }) -join ", ") })
    $links = Format-PrLinks ($pitPrs | Sort-Object Number -Unique)
    $value = (Limit-Text ($lines -join "`n") (1020 - $links.Length)) + "`n" + $links.Trim()
    $count = $pitChanges.Count
    $title = if ($count -eq 1) { "Pit loss updated on 1 track" } else { "Pit loss updated on $count tracks" }
    $fields += [ordered]@{ name = $title; value = $value; inline = $false }
}
if ($removedLines.Count -gt 0) {
    $fields += [ordered]@{ name = "Removed"; value = (Limit-Text ($removedLines -join "`n") 1024); inline = $false }
}
$thanks = @($prs | Where-Object { $_.Fork -and -not $_.IsBot } | Sort-Object Login -Unique |
    ForEach-Object { "[$($_.Login)]($($_.Profile))" })
if ($thanks.Count -gt 0) {
    $fields += [ordered]@{ name = "Thanks to"; value = (Limit-Text ($thanks -join ", ") 1024); inline = $false }
}

$footer = if ($pitChanges.Count -gt 0) { "Pit loss comes from drivers' online races $dot $Branch" } else { $Branch }
$when = (Invoke-Git @("show", "-s", "--format=%cI", $After))
$embed = [ordered]@{
    author      = [ordered]@{ name = ($repo -replace '/', ' / '); url = "https://github.com/$repo" }
    title       = "Track data updated"
    url         = "https://github.com/$repo/compare/$($Before.Substring(0, 12))...$($After.Substring(0, 12))"
    description = "Live now. The plugin picks up the new files the next time it loads a track."
    color       = $color
    fields      = @($fields)
    footer      = [ordered]@{ text = $footer }
    timestamp   = $when
}
# DISCORD_ROLE_ID: a role to ping with the post (mentions inside an embed never ping, so it goes in the content).
$payload = [ordered]@{}
if ($env:DISCORD_ROLE_ID -match '^\d+$') {
    $payload["content"] = "<@&$($env:DISCORD_ROLE_ID)>"
    $payload["embeds"] = @($embed)
    $payload["allowed_mentions"] = [ordered]@{ parse = @(); roles = @($env:DISCORD_ROLE_ID) }
} else {
    $payload["embeds"] = @($embed)
    $payload["allowed_mentions"] = [ordered]@{ parse = @() }
}
$json = ConvertTo-Json -InputObject $payload -Depth 10

if ($DryRun -or -not $env:DISCORD_WEBHOOK_URL) {
    if (-not $DryRun) { Write-Host "::notice::DISCORD_WEBHOOK_URL not set: printing the post instead of sending it" }
    Write-Output $json
    exit 0
}

$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
Invoke-RestMethod -Method Post -Uri $env:DISCORD_WEBHOOK_URL -ContentType "application/json; charset=utf-8" `
    -Headers @{ "User-Agent" = "lovely-track-data-discord" } -Body $bytes | Out-Null
Write-Host "Posted to Discord: $($changes.Count) track file(s), $($prs.Count) pull request(s)."
