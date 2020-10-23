from pathlib import Path
from tinydb import TinyDB, Query


db_path = str(Path(__file__).parent.absolute().joinpath('db.json'))
db = TinyDB(db_path)
db = db.table('guilds')


def add_command_to_db(guild, command_name, output):
    command_type = "string"

    db.insert(
        {
            guild: 
                {
                    'commands': 
                        {
                            command_name: 
                                {
                                    'output': output,
                                    'type': command_type
                                }
                        }
                }
        }
    )


# Lisää komennon käyttömäärä ja ketä luonu
# guilds -> {guild(id) : {commands: {{command {name: name, output: output, type: type}}}}}
# {command {name: name, output: output, type: type}}

#add_command_to_db('guildi', 'juttu', 'XD')

# Cmds = Query()

# res = db.table('guildi')

# print(res)