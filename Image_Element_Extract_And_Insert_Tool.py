


New_IMG_Elements_filepath = '/image/'

def ExtractImageElement():
    # nextElementSiblingInnerHTML
    # don't forget to strip ruby
    # but keep both ruby and without ruby version
    """ example:
    <p>xyz</p>
    <p>mno</p>
    <image width="1080" height="1500" xlink:href="../../image/hik/cover.jpg"/>
    <p>abc</p>
    <p>def</p>
    """
    {"img_name": 'cover.jpg', "next_txt_lines": ["abc", "def"], "previous_txt_lines": ["mno", "xyz"]}

    pass

def InsertImageElement():
    pass
