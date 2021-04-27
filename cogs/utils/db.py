import random

from pathlib import Path
from tinydb import TinyDB, Query
from datetime import datetime


db_path = str(Path(__file__).parent.absolute().joinpath('db.json'))
db_conn = TinyDB(db_path)

db = db_conn.table('commands')
whitelist = db_conn.table('whitelist')
entry = db_conn.table('entry')



def remove_command_attachments(cmd_type, fn):
    fp = Path(__file__).parent.parent.absolute().joinpath(cmd_type, fn)

    # missing_ok not in python 3.8
    if Path(fp).exists():
        Path(fp).unlink()


def add_command_to_db(guild_id, command_name, output, command_type, creator):
    timestamp = datetime.utcnow().timestamp()
    db.insert(
        {
            'guild_id': guild_id,
            'command': 
                {
                    'name': command_name,
                    'type': command_type,
                    'creator': creator,
                    'output': output, # Text or file if audio
                    'created': timestamp,
                    'count': 0
                }
        }
    )


# Note that this retunrs list with 1 element so res[0]
def get_command_from_db(guild_id, command_name):
    q = Query()
    
    res = db.search((q.guild_id == guild_id) & (q.command.name == command_name))
    return res or None


def command_exists(ctx, command_name):
    guild_id = ctx.guild.id

    q = Query()
    res = db.search((q.guild_id == guild_id) & (q.command.name == command_name))
    if res:
        return True
    else:
        return False

def incr_command_count(ctx, command_name):
    guild_id = ctx.guild.id
    q = Query()

    res = db.search((q.guild_id == guild_id) & (q.command.name == command_name))

    if res:
        res = res[0]
        res['command']['count'] += 1
        db.update(res, q.command.name == res["command"]["name"])

    else:
        return False


def remove_command_from_db(ctx, name):
    res = get_command_from_db(ctx.guild.id, name)

    if res is not None:
        output = res[0]['command']['output']
        cmd_type = res[0]['command']['type']
        
        # Text commands don't have attachements
        if cmd_type != 'text':
            remove_command_attachments(cmd_type, output)

    guild_id = ctx.guild.id

    q = Query()
    res = db.remove((q.guild_id == guild_id) & (q.command.name == name))


def get_all_commands_from_db(guild_id):
    q = Query()

    res = db.search(q.guild_id == guild_id)

    return [elem['command']['name'] for elem in res]


# Server hard coded due to commands being in db
# To avoid this all commands could be loaded on_ready
def get_random_command_name_from_db(guild_id=537996694512730123):
    q = Query()

    all_commands = db.search(q.guild_id == guild_id)

    pick = random.choice(all_commands)

    return pick['command']['name']
    

def get_top_x_commands_from_db(guild_id, amount=7):
    q = Query()

    all_commands = db.search(q.guild_id == guild_id)

    s = sorted(all_commands, key=lambda k: k['command']['count'], reverse=True)

    top = s[:amount]

    res = []

    for item in top:
        res.append((item['command']['name'], item['command']['count']))

    return res


def add_to_db_whitelist(member_id):
    whitelist.insert({'id': member_id})


def remove_from_db_whitelist(member_id):
    q = Query()
    whitelist.remove(q.id == member_id)
    

def upsert_to_entry(member, command):
    q = Query()
    guild_id = member.guild.id
    member_id = member.id

    # Check if valid command¨

    all_commands = get_all_commands_from_db(guild_id)

    if command not in all_commands:
        return False

    entry.upsert({'guild_id': guild_id, 'member_id': member_id, 'audio_fn': command}, (q.guild_id == guild_id) & (q.member_id == member.id))

    return True

def get_entry_from_db(member):
    q = Query()
    guild_id = member.guild.id
    member_id = member.id

    res = entry.search((q.guild_id == guild_id) & (q.member_id == member_id))

    if not res:
        return None
    else:
        return res[0]['audio_fn']

def remove_entry_from_db(member):
    q = Query()
    guild_id = member.guild.id
    member_id = member.id

    entry.remove((q.guild_id == guild_id) & (q.member_id == member_id))


def load_whitelist():
    # Add per guild
    res = whitelist.all()
    return [elem['id'] for elem in res]
