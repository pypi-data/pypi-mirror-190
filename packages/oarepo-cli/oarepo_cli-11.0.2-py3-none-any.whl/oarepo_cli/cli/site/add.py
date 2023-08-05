import click

from oarepo_cli.cli.utils import with_config

from ...ui.wizard import Wizard
from ...utils import to_python_name
from .step_01_install_site import InstallSiteStep
from .step_02_check_requirements import CheckRequirementsStep
from .step_03_fixup_code import FixupSiteCodeStep
from .step_04_start_containers import StartContainersStep
from .step_05_create_pipenv import CreatePipenvStep
from .step_06_install_invenio import InstallInvenioStep
from .step_07_init_database import InitDatabaseStep
from .step_08_next_steps import NextStepsStep


@click.command(
    name="add",
    help="""Generate a new site.  Required arguments:
    <name>   ... name of the site. The recommended pattern for it is <something>-site""",
)
@click.argument("name")
@with_config(config_section=lambda name, **kwargs: ["sites", name])
@click.pass_context
def add_site(ctx, cfg=None, name=None, **kwargs):
    cfg["site_package"] = to_python_name(name)
    cfg["site_dir"] = f"sites/{name}"

    initialize_wizard = Wizard(
        InstallSiteStep(pause=True),
        CheckRequirementsStep(),
        FixupSiteCodeStep(),
        StartContainersStep(pause=True),
        CreatePipenvStep(),
        InstallInvenioStep(pause=True),
        InitDatabaseStep(),
        NextStepsStep(pause=True),
    )
    initialize_wizard.run(cfg)
