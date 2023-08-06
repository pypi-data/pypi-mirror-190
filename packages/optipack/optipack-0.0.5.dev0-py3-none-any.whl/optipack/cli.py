import typer 

""" 
Optipack can be used in 2 ways: 
    - init via cli: optipack init --env <dev/staging/prod> --project <project_name> 
    - setup in code: 

        import optipack 
        optipack.setup(env, project_name) 
"""

app = typer.Typer()

@app.command(help = 'Initialize project structure')
def init(
    env: str = '', 
    project_name: str = '', 
    parent_dir: str = '', 
    structure_dir: str = '.config/project_structure.yaml', 
): 
    import optipack
    optipack.init(
        env = env, 
        project_name = project_name, 
        parent_dir=parent_dir, 
        structure_dir= structure_dir
    )

@app.command(help='Setup')
def setup(

): 
    ...

def run(): 
    app()

if __name__ == '__main__': 
    app()