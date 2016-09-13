import inputoutput as io
from parser import * 

input = io.GetTex('Nuclear.tex')

PreProcessed = PreProcess(input)
pandocced = io.RunPandoc(PreProcessed.ParsedText)
PostProcessed = PostProcess(pandocced, PreProcessed.ParsedData)

output = io.OutputMD('test.md', PostProcessed.ParsedText) 
