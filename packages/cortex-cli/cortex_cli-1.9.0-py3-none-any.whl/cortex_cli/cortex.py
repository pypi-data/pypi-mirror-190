from plumbum import cli
from cortex_cli.configure import ConfigureCli
from cortex_cli.clients import ClientsCli
from cortex_cli.inferences import InferencesCli
from cortex_cli.models import ModelsCli
from cortex_cli.pipelines import PipelinesCli
from cortex_cli.generic_get import GetCli

class CortexCli(cli.Application):
    VERSION = '1.9.0'


def main():
    CortexCli.subcommand('configure', ConfigureCli)
    CortexCli.subcommand('clients', ClientsCli)
    CortexCli.subcommand('inferences', InferencesCli)
    CortexCli.subcommand('models', ModelsCli)
    CortexCli.subcommand('pipelines', PipelinesCli)

    CortexCli.run()


if __name__ == '__main__':
    main()
