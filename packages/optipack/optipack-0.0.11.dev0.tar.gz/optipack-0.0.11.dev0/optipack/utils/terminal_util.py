def logo_loader(img_dir: str, terminal_size: tuple, term_scale: float = 1.0) -> str:
    
    from PIL import Image
    import os

    term_width, term_height = terminal_size

    term_width = int(term_width*term_scale)
    # term_height= int(term_height*term_scale)
    
    img = Image.open(img_dir)
    img_width, img_height = img.size
    scale = img_width / term_width
    term_height = int(img_height / scale)
    term_height = term_height + 1 if term_height % 2 != 0 else term_height
    img = img.resize((term_width, term_height))
    output = ""
    
    for y in range(0, term_height, 2):
        for x in range(term_width):
            r, g, b, _ = img.getpixel((x, y))
            output = output + f"[on rgb({r},{g},{b})] [/]"

        output = output + "\n"

    return output

def start_cli():

    import os 
    import rich
    from rich.console import Console
    from rich.panel import Panel 
    from rich.align import Align
    from utils.file_util import load_text

    terminal_size = os.get_terminal_size()
    logo_path = os.environ.get('LARGE_LOGO_PATH')
    scale = 1.0
    if terminal_size[0]<90:
        logo_path = os.environ.get('SMALL_LOGO_PATH')
        scale = 0.5

    if terminal_size[0]>100:
        scale = 0.7

    rich_console = Console()
    optipack_path = os.environ.get('OPTIPACK_PATH', '')
    img_path = os.path.join(
        optipack_path, 
        logo_path
    )
    message_path = os.path.join(
        optipack_path, 
        os.environ.get('MESSAGE_PATH', '')
    )

    if not img_path: 
        rich_console.print(f'Invalid logo path {img_path}', style = 'bold red')
    else: 
        image_str = logo_loader(img_path, terminal_size, scale)
        rich_console.print(Align.center(image_str))

    if not message_path: 
        print(f'Invalid message path {message_path}')
        return 
    
    rich_console.rule('Welcome to Optip⍙ck')
    msg = load_text(message_path)
    rich_console.print(Align.center(Panel.fit(msg), style= 'bold yellow'))


