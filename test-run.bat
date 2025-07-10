set "mode=Release"
@REM set "mode=Debug"

@REM Bin\x64\%mode%\Mogwai.exe --script=Source\Mogwai\Data\ReSTIRPTDemo.py
@REM Bin\x64\%mode%\Mogwai.exe --script=Source\Mogwai\Data\ReSTIRPT-Static.py

Bin\x64\%mode%\Mogwai.exe --script=Source\Mogwai\Data\RenderRefs.py
