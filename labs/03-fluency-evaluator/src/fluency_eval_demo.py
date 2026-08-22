import os
import time
from pathlib import Path
from pprint import pprint

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
)

load_dotenv(Path(__file__).resolve().parents[3] / ".env")


def extract_text(response):
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text

    parts = []
    for item in getattr(response, "output", []):
        for content in getattr(item, "content", []):
            text = getattr(content, "text", None)
            if text:
                parts.append(text)
    return "\n".join(parts)


def main() -> None:
    project_endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model_deployment_name = os.environ["FOUNDRY_MODEL_NAME"]

    prompt = "Write one short sentence answering: What is the capital of France?"

    with (
        AzureCliCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as client,
    ):
        response = client.responses.create(model=model_deployment_name, input=prompt)
        response_text = extract_text(response)

        print("MODEL RESPONSE")
        print(response_text)

        data_source_config = DataSourceConfigCustom(
            type="custom",
            item_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "response": {"type": "string"},
                },
                "required": ["response"],
            },
            include_sample_schema=True,
        )

        testing_criteria = [
            TestingCriterionAzureAIEvaluator(
                type="azure_ai_evaluator",
                name="fluency",
                evaluator_name="builtin.fluency",
                initialization_parameters={"deployment_name": model_deployment_name},
                data_mapping={"query": "{{item.query}}", "response": "{{item.response}}"},
            )
        ]

        evaluation = client.evals.create(
            name="Fluency evaluator lab",
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,
        )

        run = client.evals.runs.create(
            eval_id=evaluation.id,
            name="fluency_run",
            metadata={"lab": "03-fluency-evaluator"},
            data_source=CreateEvalJSONLRunDataSourceParam(
                type="jsonl",
                source=SourceFileContent(
                    type="file_content",
                    content=[SourceFileContentContent(item={"query": prompt, "response": response_text})],
                ),
            ),
        )

        while True:
            current_run = client.evals.runs.retrieve(run_id=run.id, eval_id=evaluation.id)
            if current_run.status in ("completed", "failed"):
                output_items = list(
                    client.evals.runs.output_items.list(run_id=current_run.id, eval_id=evaluation.id)
                )

                print("EVAL STATUS")
                print(current_run.status)
                print("EVAL REPORT URL")
                print(current_run.report_url)
                print("EVAL OUTPUT ITEMS")
                pprint(output_items)
                break

            time.sleep(5)
            print("Waiting for eval run to complete...")


if __name__ == "__main__":
    main()