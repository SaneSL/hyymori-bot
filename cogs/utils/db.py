from pathlib import Path
from tinydb import TinyDB, Query


db_path = str(Path(__file__).parent.absolute().joinpath('db.json'))
db_conn = TinyDB(db_path)

db = db_conn.table('commands')
whitelist = db_conn.table('whitelist')


def add_command_to_db(guild_id, command_name, output, command_type, creator):
    uses = 0
    db.insert(
        {
            'guild_id': guild_id,
            'command': 
                {
                    'name': command_name,
                    'type': command_type,
                    'creator': creator,
                    'uses': uses,
                    'output': output # Text or file if audio
                }
        }
    )


def get_command(ctx):
    guild_id = ctx.guild.id
    command_name = ctx.invoked_with

    q = Query()
    res = db.search((q.guild_id == guild_id) & (q.command.name == command_name))
    return res or None


def command_exists(ctx):
    guild_id = ctx.guild.id
    command_name = ctx.invoked_with

    q = Query()
    res = db.search((q.guild_id == guild_id) & (q.command.name == command_name))
    if res:
        return True
    else:
        return False


def remove_command_from_db(ctx, name):
    guild_id = ctx.guild.id

    q = Query()
    res = db.remove((q.guild_id == guild_id) & (q.command.name == name))


def add_to_db_whitelist(member_id):
    whitelist.insert({'id': member_id})


def remove_from_db_whitelist(member_id):
    q = Query()
    whitelist.remove(q.id == member_id)
    

def load_whitelist():
    res = whitelist.all()
    
    wl = []
    for d in res:
        wl.append(d['id'])

    return wl