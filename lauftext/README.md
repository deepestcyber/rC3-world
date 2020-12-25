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

You can then run:

```
python lauftext.py
```

and it will generate `test_tile.png` which contains
all your animation tiles (each row is a time-step).

# To do / nice to have

- wrap around (i.e. when reaching end of text image,
  use pixels from the end / beginning)

- 16x32 tiles maybe?
