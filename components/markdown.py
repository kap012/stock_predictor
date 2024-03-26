# img_to_bytes and img_to_html inspired from https://pmbaumgartner.github.io/streamlitopedia/sizing-and-images.html
import base64
from pathlib import Path
import streamlit as st


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def hyperlinked_img_to_html(img_path, link):
    #img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(img_to_bytes(img_path))
    img_html = f"<img src='data:image/png;base64,{img_to_bytes(img_path)}' class='img-fluid' width='30' height='30'  >"
    link_img_html = f"<a href={link}> {img_html} </a>"

    return link_img_html


# to use for custom icons
# unused for now
def custom_icon():
    fa_css = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <i class="fab fa-github"></i>
    ''' 
    #st.write(fa_css, unsafe_allow_html=True)


#another way to do it with svg
# arguably better than the option with png files - no need to connvert to bytes
    
def display_svg():
    #img = '<div class="header_svg_item"> <a href="https://google.com" target="_blank" rel="nofollow"> <svg enable-background="new 0 0 24 24" viewBox="0 0 24 24"> <path d="M23,12A11,11,0,1,0,10.279,22.865h0a11.08,11.08,0,0,0,3.436,0h0A10.952,10.952,0,0,0,23,12ZM10.859,21.935v-6.9a.5.5,0,0,0-.5-.5H8.193V12.5h2.166a.5.5,0,0,0,.5-.5V9.686c0-2.278,1.264-3.585,3.459-3.585a15.392,15.392,0,0,1,1.858.137V7.89h-.824l-.019,0a2,2,0,0,0-2.181,1.735,1.8,1.8,0,0,0-.011.4V12a.5.5,0,0,0,.5.5H15.97l-.312,2.035H13.641a.5.5,0,0,0-.5.5v6.9A10.124,10.124,0,0,1,10.859,21.935Zm3.282-.166V15.535h1.946a.5.5,0,0,0,.5-.425l.465-3.035a.5.5,0,0,0-.494-.575H14.141V10.016a1.267,1.267,0,0,1,.308-.821,1.218,1.218,0,0,1,.9-.3h1.324a.5.5,0,0,0,.5-.5V5.806a.5.5,0,0,0-.42-.494A16.661,16.661,0,0,0,14.325,5.1c-2.754,0-4.466,1.757-4.466,4.585V11.5H7.693a.5.5,0,0,0-.5.5v3.035a.5.5,0,0,0,.5.5H9.859v6.234a10,10,0,1,1,4.282,0Z"></path></svg> </a></div>'
    path = "assets\images\\facebook\logo.svg"
    #path = "assets\images\github_logos\github-mark-white.svg"
    img_string = Path(path).read_bytes()
    img = img_string.decode("utf-8") # to strip off the b''
    linked_img = f" <a href='https://google.com' > {img} </a>"

    st.markdown(linked_img, unsafe_allow_html=True)