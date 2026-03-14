$RepoDir = Split-Path $PSScriptRoot -Parent
$AddonDir = Join-Path $RepoDir "repository.fentastic"
$AddonXml = Join-Path $AddonDir "addon.xml"

[xml]$Xml = Get-Content $AddonXml
$Version = $Xml.addon.version

if (-not $Version) {
    Write-Error "Could not read version from $AddonXml"
    exit 1
}

$ZipName = "repository.fentastic-$Version.zip"
$OutputPath = Join-Path $RepoDir $ZipName

Compress-Archive -Path $AddonDir -DestinationPath $OutputPath -Force
