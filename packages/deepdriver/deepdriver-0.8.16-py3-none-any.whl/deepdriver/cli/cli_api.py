from typing import Dict

from deepdriver.sdk.config import Config

import deepdriver
from deepdriver.sdk.data_types.run import Run, set_run
from deepdriver.sdk.interface import interface
from urllib.parse import urljoin

# TODO : deepdriver 패키지를 import 하지 않고, cli를 위한 api 만들기
def init(exp_name: str = "", team_name: str = "", run_name: str = "", config: Dict = None, http_ip="") -> Run:
    """ # 실행과 실험환경을 만드는 함수 """

    rsp = interface.init(exp_name, team_name, run_name, config)
    run_url = urljoin(f"http://{http_ip}:9111", rsp['runUrl'])
    run = Run(rsp["teamName"], rsp["expName"], rsp["runName"], rsp["runId"], run_url)

    set_run(run)

    # init pytoch Log (delete for lazyload)
    # set_torch_log(TorchLog())

    # init config
    deepdriver.config = Config()
    if config:
        for key, value in config.items():
            setattr(deepdriver.config, key, value)

    return run