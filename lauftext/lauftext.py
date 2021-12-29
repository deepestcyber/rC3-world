import numpy as np
from PIL import Image
from PIL import ImageDraw, ImageFilter
import matplotlib.pyplot as plt


def display_with_text(
    base_image,
    text_image,
    x_trans=0,
    wrap_around=True,
    display_size=(30, 10),
    display_border_width=1,
    text_y=3,
):
    x_trans += display_border_width

    if wrap_around:
        text_image_org = text_image
        text_w, text_h = text_image.size
        text_image = Image.new("RGBA", (text_w * 2, text_h), 0)
        text_image.paste(text_image_org, (0, 0), text_image_org)
        text_image.paste(text_image_org, (text_w, 0), text_image_org)

    text_image_trans = Image.new("RGBA", text_image.size, 0)
    text_image_trans.paste(text_image, (x_trans, 0), text_image)

    text_mask = Image.new("L", text_image.size, 0)
    text_mask.paste(text_image, (x_trans, 0), text_image)

    display_mask = Image.new("L", text_image.size, 0)
    # we fill an image that is as big as the text
    # with 255 values (otherwise 0) where the display
    # would be.
    draw = ImageDraw.Draw(display_mask)
    draw.rectangle(
        (display_border_width, 0,
         display_size[0], display_size[1]), fill=255)

    # mask is only those pixels that are used for text
    # and the display rectangle. we use the text image
    # alpha channel as text mask and combine it with the
    # rectangle.
    mask_array = np.array(display_mask)
    mask_array &= np.array(text_mask)
    # convert mask to pixel values (0/1 -> 0/255)
    mask_array = ((mask_array != 0) * 255).astype('uint8')
    comb_mask = Image.fromarray(mask_array)

    comb_image = base_image.copy()
    comb_image.paste(text_image_trans, (0, text_y), comb_mask)

    #import pdb; pdb.set_trace()

    #plt.imshow(comb_image)
    #plt.imshow(display_mask)
    #plt.imshow(text_mask)
    #plt.imshow(comb_mask)
    #plt.imshow(text_image_trans)
    #plt.show()

    return comb_image


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('--base-image', type=str, default='base.png')
    parser.add_argument('--text-image', type=str, default='text.png')
    parser.add_argument('--speed', type=int, default=-1,
        help='Move by this many pixels each frame')
    parser.add_argument('--max-rows', type=int, default=10,
        help='how many tile rows to have. Max. 10 possible.')
    parser.add_argument('--wrap', action="store_true",
        help="Hack to make a 'wrapped' appearance. Only works "
             "with negative speeds for now.")

    args = parser.parse_args()

    base_image = Image.open(args.base_image)
    text_image = Image.open(args.text_image)

    # we can only use 10x10 tiles, so our animation
    # cannot have more than 10**2 - 1 frames (-1
    # since we need to have a space for the animated
    # tile id)
    tile_width = 32
    tile_height = 32
    tile_image_size = (10 * tile_width, args.max_rows * 2 * tile_height)
    tile_image = Image.new('RGBA', tile_image_size, 0)

    for i in range(10 * args.max_rows):
        row = i // 10
        col = i % 10
        y_offset = row * tile_height
        x_offset = col * tile_width

        comb_image = display_with_text(
            base_image,
            text_image,
            x_trans=args.speed * i,
            wrap_around=args.wrap,
        )

        tile_image.paste(comb_image, (x_offset, y_offset))

    rows_filled = row + 1

    for i in range(10 * args.max_rows):
        row = rows_filled + i // 10
        col = i % 10
        y_offset = row * tile_height
        x_offset = col * tile_width

        comb_image = display_with_text(
            base_image,
            text_image,
            x_trans=args.speed * i,
            wrap_around=args.wrap,
        )

        tile_image.paste(comb_image, (x_offset, y_offset + 16))

    tile_image.save('test_tile.png')
