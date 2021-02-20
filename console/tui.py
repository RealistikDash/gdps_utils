# Text-based UI elements
from typing import Callable
from helpers.common import paginate_list, dict_keys, trunc_name, int_str
from colorama import Fore, Back, init
import shutil

init()

# Calculate the console size.
con_size = shutil.get_terminal_size((80, 20))

# Local Constants
CON_W = con_size[0]
CON_H = con_size[1]
CON_CLS = Fore.WHITE + Back.BLACK

def out_title(text: str) -> None:
    """Prints out a styled console title.
    
    Args:
        text (str): The name of the title.
    """

    # Calc padding size.
    t_len = len(text)

    pad = ((CON_W - t_len) // 2) - 2

    final_str = ""
    final_str += "-" * pad
    final_str += f"{Fore.WHITE}{Back.BLUE}[{text.title()}]{CON_CLS}"
    final_str += "-" * pad
    print(final_str)

class ConUIElem:
    """Base console UI element."""

    def init(self) -> None: return
    def out(self) -> None: return

class ListSelection(ConUIElem):
    """A user interactive selection list."""

    def __init__(self, title: str):
        """Configures the selection element."""

        self.page: int = 0
        self.page_len: int = 15
        self.elements: dict = {}
        self.title: str = title
    
    @property
    def all_elems(self) -> tuple:
        """Tuple of the names of all the
        registered elements."""

        return dict_keys(self.elements)
    
    @property
    def _current_page_elems(self):
        """Shows the names of the current
        page names."""

        return paginate_list(self.all_elems, self.page, self.page_len - 2)
    
    @property
    def max_pages(self):
        """MAx page."""

        return (len(self.all_elems) // self.page_len -2) + 1
    
    def add_page_elem(self, name: str, handler: Callable):
        """Adds a page element to the
        list."""

        self.elements[name] = handler
    
    def _next_page(self) -> None:
        """Moves to the next page list."""

        if self.page == self.max_pages: return
        self.page += 1

    def _prev_page(self) -> None:
        """Moves to the prev page list."""

        if self.page == 0: return
        self.page -= 1
    
    def out(self):
        """Prints the element to console."""

        # Title
        out_title(self.title)
        print(f"{Fore.RED}Page ({int_str(self.page + 1, 2)}/{int_str(self.max_pages, 2)})" + CON_CLS)

        txt = ""
        pre = "# "

        for num, elem in enumerate(self.all_elems):
            txta = pre + f"{Fore.WHITE}{Back.RED}[{int_str(num + 1)}]{CON_CLS} - "
            e_name = trunc_name(elem, 15)
            txta += e_name + (" " * (15 -len(e_name))) + " "
            txta += f"| {Fore.YELLOW}"
            txta += trunc_name(self.elements[elem].__doc__, CON_W - len(txta)) + CON_CLS
            txt += txta +"\n"
        
        print(txt)
    
    def _handle_input(self, input: str)


def display(elem: ConUIElem) -> None:
    """Displays a console UI element."""

    elem.init()
    elem.out()

out_title("Hello there!")

b = ListSelection("Bruh")
b.add_page_elem("A thing", display)
b.add_page_elem("Another thing", display)
b.add_page_elem("Your Great grand father", display)
display(b)
