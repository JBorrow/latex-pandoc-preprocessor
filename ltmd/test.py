import inputoutput as io
from parser import * 

input = io.GetTex('test.tex')

PreProcessed = PreProcess(input)
print(PreProcessed.ParsedText)
pandocced = io.RunPandoc(PreProcessed.ParsedText)
PostProcessed = PostProcess(pandocced, PreProcessed.ParsedData)

output = io.OutputMD('test.md', PostProcessed.ParsedText) 
