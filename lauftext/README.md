# Installation

```
sudo apt install python3-virtualenv
virtualenv -ppython3 ./env
source ./env/bin/activate
pip install -r requirements.txt
```

# Usage

We have a display base image and we want to generate an
animation playing on said display - playing meaning
we have an object moving from right to left, e.g.
a text.

You need:
- base image (located in this folder)
- text image (the image you want to display)

The size of the text image depends on the base image
of course. **The default base image requires a
`Wx9` pixel sized text image.**

You can then run:

```
python lauftext.py
```

and it will generate `test_tile.png` which contains
all your animation tiles (each row is a time-step).

# What font to use?

I found `fixed_01` to work quite well. You can get it
[here](http://www.orgdot.com/aliasfonts/fixed_01.zip).

The font [5x8-lcd-hd44780u-a02](https://fontstruct.com/fontstructions/show/310233/5x8_lcd_hd44780u_a02)
works also quite nicely (since it is only 8px high).

# To do / nice to have

- wrap around (i.e. when reaching end of text image,
  use pixels from the end / beginning)

- 16x32 tiles maybe?

# Examples

```
python lauftext.py --base-image base_16p.png --text-image text_gol_5x8.png --wrap --max-rows=9
```
