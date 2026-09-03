param(
    [string]$SkillName = "game-replica",
    [string]$CodexHome = "$HOME\.codex"
)

$ErrorActionPreference = "Stop"

$source = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsDir = Join-Path $CodexHome "skills"
$target = Join-Path $skillsDir $SkillName
$resolvedSkillsDir = [System.IO.Path]::GetFullPath($skillsDir)
$resolvedTarget = [System.IO.Path]::GetFullPath($target)

if (-not $resolvedTarget.StartsWith($resolvedSkillsDir, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to install outside skills directory: $resolvedTarget"
}

New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null

if (Test-Path -LiteralPath $target) {
    Remove-Item -LiteralPath $target -Recurse -Force
}

$exclude = @(".git", "__pycache__", ".pytest_cache", ".mypy_cache")
$excludeExtensions = @(".zip")

function Copy-SkillItem {
    param(
        [string]$From,
        [string]$To
    )

    $name = Split-Path -Leaf $From
    $extension = [System.IO.Path]::GetExtension($From)
    if ($exclude -contains $name) {
        return
    }
    if ($excludeExtensions -contains $extension) {
        return
    }

    if (Test-Path -LiteralPath $From -PathType Container) {
        New-Item -ItemType Directory -Force -Path $To | Out-Null
        Get-ChildItem -LiteralPath $From | ForEach-Object {
            Copy-SkillItem -From $_.FullName -To (Join-Path $To $_.Name)
        }
    } else {
        Copy-Item -LiteralPath $From -Destination $To
    }
}

Copy-SkillItem -From $source -To $target

Write-Host "Installed $SkillName to $target"
Write-Host 'Invoke it with: Use $game-replica to analyze and replicate this game project.'
