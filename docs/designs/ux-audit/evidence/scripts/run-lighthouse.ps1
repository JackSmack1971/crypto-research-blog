$ErrorActionPreference = 'Continue'
$outDir = Join-Path (Get-Location) 'docs/designs/ux-audit/evidence/lighthouse'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$urls = @(
  @{ name = 'home'; url = 'https://independent-market-notes.netlify.app/' },
  @{ name = 'bitcoin-buying-imbalance'; url = 'https://independent-market-notes.netlify.app/bitcoin-buying-imbalance/' },
  @{ name = 'newest-token-unlock'; url = 'https://independent-market-notes.netlify.app/token-unlock-liquidity-illusion-90-day-calendar/' }
)
$chrome = Get-ChildItem "$env:LOCALAPPDATA\ms-playwright" -Recurse -Filter chrome.exe -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName
$results = @()
foreach ($target in $urls) {
  foreach ($mode in @('mobile', 'desktop')) {
    $output = Join-Path $outDir "$($target.name)-$mode.json"
    if (Test-Path $output) { $results += [pscustomobject]@{ name=$target.name; mode=$mode; result='exists_skipped'; output=$output }; continue }
    $cliArgs = @('--yes','--package=lighthouse@12','lighthouse',$target.url,'--output=json',"--output-path=$output",'--quiet','--only-categories=performance,accessibility,best-practices,seo',"--chrome-path=$chrome")
    if ($mode -eq 'desktop') { $cliArgs += '--preset=desktop' }
    & npx @cliArgs 2>&1 | Tee-Object -FilePath (Join-Path $outDir "$($target.name)-$mode.log")
    $code = $LASTEXITCODE
    $results += [pscustomobject]@{ name=$target.name; mode=$mode; result=if ($code -eq 0 -and (Test-Path $output)) {'complete'} else {'failed'}; exit_code=$code; output=$output }
  }
}
$results | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $outDir '_run-index.json') -Encoding utf8
$results | Format-Table -AutoSize
if ($results.result -contains 'failed') { exit 1 }
