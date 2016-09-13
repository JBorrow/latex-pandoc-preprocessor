import ltmd

input = ltmd.GetTex('Nuclear.tex')

PreProcessed = ltmd.PreProcess(input)
pandocced = ltmd.RunPandoc(PreProcessed.ParsedText)
PostProcessed = ltmd.PostProcess(pandocced, PreProcessed.ParsedData)

output = ltmd.OutputMD('test.md', PostProcessed.ParsedText) 
