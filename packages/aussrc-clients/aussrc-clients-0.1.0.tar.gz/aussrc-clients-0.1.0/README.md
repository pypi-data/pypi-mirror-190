# AusSRC Client APIs

## Workflow Module

Remotely deploy workflows and control jobs via Python REST API to https://workflows.aussrc.org

### Example

``` python
import asyncio
from aussrc.workflow import workflow


async def deploy():
    username = "test"
    password = "test"

    async with workflow.Workflow(username, password) as work:
        # get pipeline
        pipeline = await work.get_pipelines(host='setonix', search_values=['parallel'])
        # deploy preconfigured pipeline
        params = {"num_process": "test"}
        job = await pipeline[0].deploy(params)
        # wait for job to end
        resp = await job.wait()
        #get log
        resp = await job.log()
        print(resp.decode())

asyncio.run(deploy())
```