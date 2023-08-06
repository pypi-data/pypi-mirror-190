import sys
import click
from charsi import __version__
from charsi.strings import StringTable
from charsi.recipe import Recipe


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli():
    """A command-line tool to help game modders build string resources for Diablo II: Resurrected."""


@cli.command('build', help='Build a string table with recipe.')
@click.option('--recipe-file', help='Path of recipe file.', metavar='FILE', type=click.File(mode='r', encoding='utf-8-sig'), required=True)
@click.argument('stbl-file', metavar='FILE', type=click.File(mode='r', encoding='utf-8-sig'), required=True)
def build_command(recipe_file, stbl_file):
    recipe = Recipe()
    recipe.load(recipe_file)

    stbl = StringTable()
    stbl.load(stbl_file)

    recipe.build(stbl)

    stbl.dump(sys.stdout)


if __name__ == '__main__':
    cli()
