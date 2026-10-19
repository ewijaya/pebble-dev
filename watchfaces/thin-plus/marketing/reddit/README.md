# Thin+ Reddit carousel

Three generated promotional mockups, in this order:

1. `generated/01-heritage.png` — The Thin you love. More ways to make it yours.
2. `generated/02-personal-choice.png` — How minimal is your minimal?
3. `generated/03-seven-moods.png` — One face. Seven moods.

The final images and suggested Reddit copy are packaged in
`thin-plus-reddit-carousel.zip`. `reddit-post.txt` contains the title, body,
suggested Face flair, and carousel order. Nothing has been posted to Reddit.

## Generation and references

Generated with the built-in imagegen tool. The tool does not expose a selectable
model version; no claim is made that a specific "2.5" model was used.

The final prompt set is in `prompt-01.txt`, `prompt-02.txt`, `prompt-03.txt`,
and their corresponding `*-refinement.txt` files. The last theme-color pass is
in `prompt-03-final-colors.txt`. Images ending in `-v1.png` or `-v2.png` are
earlier drafts, excluded from the upload bundle.

Official hardware references supplied by the user are preserved in `references/`;
their URLs are recorded in `references/sources.json`. The images are generated
product mockups, not photographs of a physical watch. Native screen references
come from the released Thin+ 1.1.0 PBW and earlier approved store screenshots.

`screens/provenance.json` records nine native Emery captures, using a persistent
emulator connection to set a consistent demonstration time. Battery and step
values are simulated. `capture-screens.py` reproduces those references using the
SDK screenshot processing used by the Pebble CLI. The originals remain separate
from the generated compositions.

The app binary and live store listing were not changed by this artwork task.
The required credit in each image and the post is:

Based on Thin by Chris Lewis.
