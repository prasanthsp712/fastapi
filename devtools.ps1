param([string]$command)

if (!(Test-Path "devtools.json")) {
    Write-Host "ERROR: devtools.json not found"
    exit
}

$config = Get-Content devtools.json | ConvertFrom-Json

$image       = $config.imageName
$container   = $config.containerName
$cPort       = $config.containerPort
$hPort       = $config.defaultPort
$debugPort   = $config.debugPort

$runCmd      = $config.runCommand
$debugCmd    = $config.debugCommand
$testCmd     = $config.testCommand
$reqFile     = $config.appRequirementFilePath

# Replace dynamic variables
$runCmd   = $runCmd   -replace "\$\{containerPort\}", $cPort
$debugCmd = $debugCmd -replace "\$\{containerPort\}", $cPort
$debugCmd = $debugCmd -replace "\$\{debugPort\}", $debugPort

# Dependency install command
$installCmd = ""

if ($reqFile -and (Test-Path $reqFile)) {
    $installCmd = "pip install -r $reqFile && "
}

# Remove existing container
docker rm -f $container *> $null

switch ($command) {

"init" {

    Write-Host "Pulling Docker image: $image"
    docker pull $image

    Write-Host ""
    Write-Host "Environment initialized successfully."
    Write-Host "Use '.\devtools.ps1 run' to start the application."
}

"run" {

    docker run -it `
        -p $hPort`:$cPort `
        -v ${PWD}:/app `
        -w /app `
        --name $container `
        $image `
        bash -c "$installCmd$runCmd"
}

"debug" {

    # Create VSCode launch config
    if (!(Test-Path ".vscode")) {
        New-Item -ItemType Directory -Path ".vscode" | Out-Null
    }

    $launch = @{
        version="0.2.0"
        configurations=@(
            @{
                name="Docker Python Debug"
                type="python"
                request="attach"
                connect=@{
                    host="localhost"
                    port=$debugPort
                }
                pathMappings=@(
                    @{
                        localRoot='${workspaceFolder}'
                        remoteRoot="/app"
                    }
                )
            }
        )
    }

    $launch | ConvertTo-Json -Depth 5 | Out-File ".vscode/launch.json"

    Write-Host "Generated .vscode/launch.json"

    docker run -it `
        -p $hPort`:$cPort `
        -p $debugPort`:$debugPort `
        -v ${PWD}:/app `
        -w /app `
        --name $container `
        $image `
        bash -c "$installCmd$debugCmd"
}

"test" {

    docker run -it `
        -v ${PWD}:/app `
        -w /app `
        --name $container `
        $image `
        bash -c "$installCmd$testCmd"

    if (Test-Path "htmlcov/index.html") {
        Write-Host "Opening coverage report..."
        Start-Process "htmlcov/index.html"
    }
}

"help" {

    Write-Host ""
    Write-Host "DevTools Commands"
    Write-Host ""
    Write-Host ".\devtools.ps1 init   -> Pull docker image"
    Write-Host ".\devtools.ps1 run    -> Run application"
    Write-Host ".\devtools.ps1 debug  -> Run with debugger"
    Write-Host ".\devtools.ps1 test   -> Run tests with coverage"
    Write-Host ".\devtools.ps1 help   -> Show help"
    Write-Host ""
}

default {

    Write-Host "Invalid command."
    Write-Host "Use: .\devtools.ps1 help"
}

}