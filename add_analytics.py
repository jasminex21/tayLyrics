import os
from bs4 import BeautifulSoup
import pathlib
import shutil
import streamlit as st

# Get multiple GA IDs, comma-separated (e.g., "G-MAIN,G-SUBAPP1")
GA_IDS = os.getenv("GA_IDS", "G-XXXXXXXXXX").split(',')

GA_SCRIPTS = "\n".join([
    f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script id='google_analytics_{ga_id}'>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_id}');
    </script>
    """
    for ga_id in GA_IDS
])

def inject_ga():
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    
    # Check if the scripts are already injected
    if not any(soup.find(id=f"google_analytics_{ga_id}") for ga_id in GA_IDS):
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)
        else:
            shutil.copy(index_path, bck_index)
        
        new_html = str(soup).replace('<head>', '<head>\n' + GA_SCRIPTS)
        index_path.write_text(new_html)

inject_ga()