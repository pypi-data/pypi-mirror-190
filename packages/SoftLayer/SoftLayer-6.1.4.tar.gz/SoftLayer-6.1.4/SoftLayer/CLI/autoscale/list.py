"""List Autoscale groups."""
# :license: MIT, see LICENSE for more details.

import click

from SoftLayer.CLI.command import SLCommand as SLCommand
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer.managers.autoscale import AutoScaleManager
from SoftLayer import utils


@click.command(cls=SLCommand)
@environment.pass_env
def cli(env):
    """List all Autoscale Groups on your account."""

    autoscale = AutoScaleManager(env.client)
    groups = autoscale.list()

    table = formatting.Table(["Id", "Name", "Status", "Min/Max", "Running"])
    table.align['Name'] = 'l'
    for group in groups:
        status = utils.lookup(group, 'status', 'name')
        min_max = "{}/{}".format(group.get('minimumMemberCount'), group.get('maximumMemberCount'))
        table.add_row([
            group.get('id'), group.get('name'), status, min_max, group.get('virtualGuestMemberCount')
        ])

    env.fout(table)
