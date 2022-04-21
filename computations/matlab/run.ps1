$srcpath = $MyInvocation.MyCommand.Path
$workdir = Split-Path -Path $srcpath
$mpath = Join-Path -Path $workdir -ChildPath "mstm3D.m"

matlab -nosplash -nodesktop -r "run('$mpath'); exit;"