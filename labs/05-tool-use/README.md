# Tool use lab.

Use the Responses API with built-in `file_search` and `web_search` tools.

This lab creates a temporary vector store, uploads sample Margie's Travel brochure files, asks the model to answer from those files, then asks a follow-up that can use web search for current public context.

```powershell
python .\labs\05-tool-use\src\tool_use_demo.py
```

The lab deletes the vector store at the end so repeated runs do not leave extra resources behind. To inspect the vector store after a run, set:

```powershell
$env:FOUNDRY_KEEP_VECTOR_STORE = "1"
```

If your Foundry model or region does not support the `web_search` tool, the script retries the same request with `file_search` only and prints a note.