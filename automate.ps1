while ($true) {
    Get-ChildItem -Path .\renderer\.godot\ -Include *.* -File -Recurse | ForEach-Object { $_.Delete() }
    Get-ChildItem -Path .\renderer\data\ -Include *.* -File -Recurse | ForEach-Object { $_.Delete() }
    python .\Main.py AskReddit false
    Write-Output "python finished"
    Set-Location .\renderer
    Write-Output "in renderer"
    Start-Job -Name godot -ScriptBlock { godot --editor }
    Write-Output "godot opened"
    Start-Sleep -Seconds (30)
    Stop-Process -Name godot
    Write-Output "godot closed"
    Start-Job -Name godot -ScriptBlock { godot --editor }
    Write-Output "godot opened second time"
    Start-Sleep -Seconds (30)
    Stop-Process -Name godot
    Write-Output "godot closed second time"
    Start-Job -Name godot -ScriptBlock { godot --editor }
    Write-Output "godot opened third time"
    Start-Sleep -Seconds (30)
    Stop-Process -Name godot
    Write-Output "godot closed third time"
    Start-Job -Name godot -ScriptBlock { godot --editor }
    Write-Output "godot opened fourth time"
    Start-Sleep -Seconds (30)
    Stop-Process -Name godot
    Write-Output "godot closed fourth time"
    godot --write-movie AskReddit.avi .\scenes\main\main.tscn --fixed-fps 60 --resolution 1920x1080 | Out-Null
    Write-Output "movie rendered"
    ffmpeg -y -i .\AskReddit.avi -crf 15 AskReddit.mp4 | Out-Null
    Write-Output "movie compressed"
    Set-Location ..
    Write-Output "back in main folder"
    python.exe .\YouTube\AskReddit\Upload_ask.py
    Write-Output "Youtube posted"
    Write-Output "First post sucsecdssss"

    python .\Main.py AskReddit true
    Write-Output "python finished 3"
    Set-Location .\shorts
    Write-Output "in renderer 3"
    npm run build
    Write-Output "renderered 3"
    Set-Location ..
    Write-Output "back in main folder 3"
    python .\YouTube\AskRedditShorts\Upload_ask_shorts.py
    Write-Output "Youtube posted 3"
    Write-Output "Short post sucsecdssss"

    Get-ChildItem -Path .\renderer\.godot\ -Include *.* -File -Recurse | ForEach-Object { $_.Delete() }
    Get-ChildItem -Path .\renderer\data\ -Include *.* -File -Recurse | ForEach-Object { $_.Delete() }
    python .\Main.py AmItheAsshole false
    Write-Output "python finished 2"
    Set-Location .\renderer
    Write-Output "in renderer 2"
    Start-Job -Name godot -ScriptBlock { godot --editor }
    Write-Output "godot opened 2"
    Start-Sleep -Seconds (30)
    Stop-Process -Name godot
    Write-Output "godot closed 2"
    Start-Job -Name godot -ScriptBlock { godot --editor }
    Write-Output "godot opened second time 2"
    Start-Sleep -Seconds (30)
    Stop-Process -Name godot
    Write-Output "godot closed second time 2"
    Start-Job -Name godot -ScriptBlock { godot --editor }
    Write-Output "godot opened third time 2"
    Start-Sleep -Seconds (30)
    Stop-Process -Name godot
    Write-Output "godot closed third time 2"
    Start-Job -Name godot -ScriptBlock { godot --editor }
    Write-Output "godot opened fourth time 2"
    Start-Sleep -Seconds (30)
    Stop-Process -Name godot
    Write-Output "godot closed fourth time 2"
    godot --write-movie AmItheAsshole.avi .\scenes\main\main.tscn --fixed-fps 60 --resolution 1920x1080 | Out-Null
    Write-Output "movie rendered 2"
    ffmpeg -y -i .\AmItheAsshole.avi -crf 15 AmItheAsshole.mp4 | Out-Null
    Write-Output "movie compressed 2"
    Set-Location ..
    Write-Output "back in main folder 2"
    python.exe .\YouTube\AmItheAsshole\Upload_aita.py
    Write-Output "Youtube posted 2"
    Write-Output "Second post sucsecdssss"

    python .\Main.py AmItheAsshole true
    Write-Output "python finished 4"
    Set-Location .\shorts
    Write-Output "in renderer 4"
    npm run build
    Write-Output "renderered 4"
    Set-Location ..
    Write-Output "back in main folder 4"
    python .\YouTube\AmItheAssholeShorts\Upload_aita_shorts.py
    Write-Output "Youtube posted 4"
    Write-Output "Short post sucsecdssss"

    python .\Main.py MrReddit true
    Write-Output "python finished 5"
    Set-Location .\shorts
    Write-Output "in renderer 5"
    npm run build
    Write-Output "renderered 5"
    Set-Location ..
    Write-Output "back in main folder 5"
    python .\YouTube\MrReddit\Upload_mr_reddit.py
    Write-Output "Youtube posted 5"
    Write-Output "mrReddit sucsecdssss"

    Start-Sleep -Seconds (4 * 60 * 60)
}
