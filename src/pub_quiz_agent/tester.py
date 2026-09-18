from pathlib import Path
import sys
import json

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from pub_quiz_agent.pub_quiz_agent_models import Question

def main():
    schema_str = json.dumps(Question.model_json_schema(), indent=2)
    print(schema_str)

if __name__ == "__main__":
    main()
