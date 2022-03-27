$srcpath = $MyInvocation.MyCommand.Path
$workdir = Split-Path -Path $srcpath
$mpath = Join-Path -Path $workdir -ChildPath "mstm.m"

matlab -nodisplay -nosplash -nodesktop -r "run('$mpath'); exit;"