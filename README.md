# ai-103-foundry-learning-lab

This repository is for hands-on practice and ai-103 certification study only.

## Prerequisites

- Python 3.11+
- Azure CLI
- Azure AI Foundry project
- Two model deployments, for example `gpt-4.1` and `gpt-4.1-mini`
- Access to the Foundry resource with Microsoft Entra ID auth

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Environment Configuration

Create the ignored `.env` file from the committed template and replace the placeholders:

```shell
cp .env.example .env
```

Every demo loads this repository-root file automatically. Authenticate separately with Azure CLI:

```shell
az login --tenant <tenant-id>
```

The demos use `AzureCliCredential` and do not read authentication credentials from `.env`.

## Self-Test

```powershell
python .\labs\01-basic-responses-api\src\responses_api_demo.py
python .\labs\02-model-compare\src\model_comparison_demo.py
python .\labs\03-fluency-evaluator\src\fluency_eval_demo.py
python .\labs\04-responses-api-features\src\responses_features_demo.py
python .\labs\05-tool-use\src\tool_use_demo.py
python .\labs\06-agent-config-tooling\src\agent_config_tooling_demo.py
```