import click
from tagcounter.counter import count_tags, upload_to_db, retrieve_by_name, get_alias_dict
from tagcounter import gui
import runpy

@click.command()
@click.option('--get', help='getting tags by a domain name')
@click.option('--view', help='retrieving tags from data base by a domain name')
def run_counter(get, view):
    if get is not None:
        name = get
        aliases = get_alias_dict()
        name_by_alias = aliases.get(name)
        if name_by_alias is not None:
            name = name_by_alias
        result = count_tags(name)
        if result is not None:
            upload_to_db(domain_name=name, url=result['url'], date=result['date'], tagdict=result['tagdict'])
            for key, value in sorted(result['tagdict'].items()):
                print("{}: {} opening tags and {} closing tags\n".format(key, value[0], value[1]))
        else:
            print('Tags has not been obtained!')
    elif view is not None:
        name = view
        aliases = get_alias_dict()
        name_by_alias = aliases.get(name)
        if name_by_alias is not None:
            name = name_by_alias
        result = retrieve_by_name(domain_name=name)
        if result is not None:
            for key, value in sorted(result['tagdict'].items()):
                print("{}: {} opening tags and {} closing tags\n".format(key, value[0], value[1]))
        else:
            print('The source has not been found in database')
    else:
        runpy.run_module('gui', run_name='__main__')

if __name__=='__main__':
    run_counter()



