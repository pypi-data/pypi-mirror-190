from localstack.runtime import hooks
@hooks.on_infra_start()
def register_launchpad_api():from localstack.services.edge import ROUTER as A;from localstack_ext.bootstrap.pods.launchpad.api import LaunchPadApi as B;A.add_route_endpoints(B())