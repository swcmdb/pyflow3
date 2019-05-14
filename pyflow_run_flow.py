import sys
import json

sys.path.append('/home/pyflow/src')

from fbp import run_flow
import fbp.repository

def run_pyflow(flow_name, repo_path):
    # Load Pyflow repository json file
    repository = fbp.repository()
    repository.loads(repo_path)
    # Load flow spec
    with open(repo_path, 'r') as f:
        repo = json.loads(f.read())
    flow_spec = repo["flow"][flow_name] 
    # Run Pyflow with flow_spec
    return json.dumps(run_flow(flow_spec), indent=2)

if __name__ == '__main__':
    REPO_PATH = '/tmp/repo_input.json'
    FLOW_NAME = 'pyflow.sample.input'
    print(run_pyflow(FLOW_NAME, REPO_PATH))
