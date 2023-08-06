import math
from io import BytesIO
import collections
from typing import List, Tuple, Union, Callable

from PIL import Image, ImageDraw, ImageFont
from boxobj import Box, Pages, Coordinates


def _image_byte_count(image: Image) -> int:
    buff = BytesIO()
    image.save(buff, "PNG" if image.format is None else image.format)
    return len(buff.getvalue())


def _color_list():
    return [
        (44, 160, 44),
        (31, 119, 180),
        (255, 127, 14),
        (214, 39, 40),
        (148, 103, 189),
        (140, 86, 75),
        (227, 119, 194),
        (127, 127, 127),
        (188, 189, 34),
        (255, 152, 150),
        (23, 190, 207),
        (174, 199, 232),
        (255, 187, 120),
        (152, 223, 138),
        (197, 176, 213),
    ]


def _find_label_index(item, labels):
    if "label" in item:
        for idx, label in enumerate(labels):
            if label == item["label"]:
                return idx
    else:
        return 0


def generate_label(keys):
    key_list = keys

    def gen_label(idx, item):
        label = ""
        for key in key_list:
            if len(label) != 0:
                label = label + "\n"
            if key == "index":
                label = label + item.get(key, idx)
            else:
                label = item.get(key)
        return label


def tile_images(images: List[Image], max_width=3000) -> Image:
    # TODO: Add handling for variably sized images?
    (x, y) = images[0].size
    columns = min(max(math.floor(max_width / x), 1), len(images))
    rows = math.ceil(len(images) / columns)
    canvas = Image.new("RGB", (x * columns, y * rows), color="white")

    for idx, image in enumerate(images):
        row = math.floor(idx / columns)
        column = idx - (row * columns)
        canvas.paste(image, (column * x, row * y))
    return canvas


def join_images(
    images: List[Image], horizontal: bool = True
) -> Tuple[Image, List[Coordinates]]:
    width: int = 0
    height: int = 0
    indices: List[Coordinates] = []

    if horizontal:
        for image in images:
            (x, y) = image.size
            height = max(height, y)
            indices.append((width, 0, width + x, y))
            width += x
    else:
        for image in images:
            (x, y) = image.size
            width = max(width, x)
            indices.append((0, height, x, height + y))
            height += y

    canvas = Image.new("RGB", (width, height), color="white")
    for image, coordinates in zip(images, indices):
        canvas.paste(image, coordinates[:2])

    return canvas, indices


def join_images_as_pages(images: List[Image], horizontal: bool = False):
    image, indices = join_images(images, horizontal)
    return image, Pages.from_indices(indices)


def scale_image_to_size(
    image: Image, max_pixels: int = None, max_bytes: int = None
) -> Tuple[Image, Union[float, None]]:
    src_bytes = _image_byte_count(image)
    x, y = image.size
    src_pixels = x * y
    bytes_scalar = math.sqrt(max_bytes / src_bytes) if max_bytes else 1
    pixels_scalar = math.sqrt(max_pixels / src_pixels) if max_pixels else 1
    scalar = min(bytes_scalar, pixels_scalar)
    if scalar >= 1:
        return image, None
    else:
        new_x = int(scalar * x)
        new_y = int(scalar * y)
        new_image, scalar = image.resize((new_x, new_y), Image.BICUBIC), scalar
        if max_bytes and _image_byte_count(new_image) > max_bytes:
            return scale_image_to_size(
                image=image, max_pixels=max_pixels, max_bytes=int(max_bytes * 0.95)
            )
        else:
            return new_image, scalar


def render_boxes(
    boxes: List[Box],
    image: Image,
    color: Union[List, Callable] = None,
    width=None,
    label_size=24,
    label=None,
    annotation_filter=None,
    color_index=None,
    font=None,
):
    loaded_font = None

    def _font():
        nonlocal loaded_font
        if font:
            return font
        if not loaded_font:
            try:
                loaded_font = ImageFont.truetype("arial.ttf", size=label_size)
            except OSError:
                try:
                    loaded_font = ImageFont.truetype("DejaVuSans.ttf", size=label_size)
                except OSError:
                    loaded_font = ImageFont.load_default()
        return loaded_font

    # Change palette mode images to RGB so that standard palette colors can be drawn on them
    if image.mode == "P":
        image = image.convert(mode="RGB")
    else:
        image = image.copy()
    if color is None:
        color = _color_list()
    width = round(image.width / 512) + 1 if width is None else width
    label_size = 20 if label_size is None else label_size

    draw = ImageDraw.Draw(image)

    for idx, box in enumerate(boxes):
        if annotation_filter is None or annotation_filter(idx, box):

            # select a color to use with this box
            if isinstance(color, str):
                box_color = color
            elif isinstance(color, Callable):
                box_color = color(idx, box)
            elif color_index:
                # TODO: Fix array out of bounds issue
                box_color = color[color_index(idx, box)]
            else:
                box_color = "green"
            draw.rectangle(box.coordinates, outline=box_color, width=width)
            if label:
                if isinstance(label, str):
                    text = label
                else:
                    text = label(idx, box)
                size = draw.textsize(text, font=_font(), spacing=0)
                draw.multiline_text(
                    (box.left - size[0] - 4, box.top + 4),
                    text,
                    fill=box_color,
                    font=_font(),
                    spacing=0,
                    align="right",
                )
    return image


def render_boxes_from_objects(
    objects, accessor, image=None, labels=None, single_image=True, color=None
):
    if isinstance(objects, collections.Mapping):
        annotation = accessor(objects)
        if labels:
            return render_boxes(
                annotation,
                image=image,
                color=color,
                color_index=lambda idx, item: _find_label_index(item, labels),
            )
        else:
            return render_boxes(annotation, image=image, color=color)
    elif single_image:
        for idx, obj in enumerate(objects):
            annotation = accessor(obj)
            if callable(color):
                image = render_boxes(
                    annotation,
                    image=image,
                    color=lambda o_idx, e_idx, item: color(idx, e_idx, item),
                    color_index=lambda i, item: idx,
                )
            else:
                image = render_boxes(
                    annotation, image=image, color_index=lambda i, item: idx
                )
        return image
    else:
        images = []
        for idx, obj in enumerate(objects):
            annotation = accessor(obj)
            if callable(color):
                images.append(
                    render_boxes(
                        annotation,
                        image=image,
                        color=lambda e_idx, item: color(idx, e_idx, item),
                        color_index=lambda i, item: idx,
                    )
                )
            else:
                images.append(
                    render_boxes(
                        annotation, image=image, color_index=lambda i, item: idx
                    )
                )
        return images
