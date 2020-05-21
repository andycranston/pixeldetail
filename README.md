# pixeldetail

Create a new image from an existing image which shows the detail of every pixel.

## Running the `pixeldetail.py` Python 3 program

You need the Pillow module for Python installed in your environment. This should
be as simple as:

```
pip install -U Pillow
```

To create a detailed image from an existing image called `pd.bmp` type:

```
python pixeldetail.py pd.bmp
```

You should get output similar to:

```
Reading image file "pd.bmp"
Creating new image of 27985 pixels
Copying pixels to new image
Drawing horizontal separator lines
Drawing vertical separator lines
Putting RGB values into each pixel box
Saving new image to file "pd-detail.bmp"
Done
```

The program will have created the file `pd-detail.bmp` and it should look like:

[pd-detail.bmp](https://raw.githubusercontent.com/andycranston/pixeldetail/master/pd-detail.bmp)

If possible try and open the above link in a new tab or window so you
can keep reading here.

For each pixel in the original image a larger "pixel box" is created which
measures (by default) 48 pixels wide by 48 pixels tall. In the top left of
the pixel boxes the RGB values of the pixel colour is displayed. Each
individual value is in decimal with leading zeroes for values less than
100. For example:

```
087
003
255
```

Some boxes may have only one value like this:

```
077
```

This happens when the pixel colour is a greyscale colour - that is each
of the three numbers in the RGB value are the same.

Finally a pixel which has the RGB value (0,0,0) is just an empty black
pixel box and a pixel which has the RGB value (255,255,255)
is an empty white pixel box.

Note that the new file name is based on the original file name - the
string `-detail` is inserted so:

```
filename.bmp
```

gives:

```
filename-detail.bmp
```

Be warned that if a file called `filename-detail.bmp` already exists it
will be overwritten without warning.

## Command line option `--wide`

The width of the pixel boxes can be changed from the default 48 pixels
to any reasonable value. For example:

```
python pixeldetail.py --wide 64
```

will create pixel boxes that are 64 pixels wide.

You cannot specify a width less than 23 pixels.

## Command line option `--tall`

The height of the pixel boxes can be changed from the default 48 pixels
to any reasonable value. For example:

```
python pixeldetail.py --tall 64
```

will create pixel boxes that are 64 pixels tall.

You cannot specify a value less than 33 pixels for the `--tall` command
line option.

You can supply both the `--wide` and `--tall` command line options at
the same time.

## What is this for?

I would like to say "Art" but I would be lying :-] You can get some
quite arty effects though especially when you experiment with
the `--wide` and `--tall` command line arguments.

I actually wrote this so I could take a screen shot, crop it to the
part of the screen I was interested in and then "blow up" the image to
see the exact pixel layout along with the RGB values.

## It is really slow - I mean "S...L...O...W...!"

Each pixel in the original image is copied 2304 times - more if
the `--wide` and/or `--tall` command line arguments are used with
values greater than 48. There might be optimisations to be had
here and there but this is just the way the program works.

Only use it to expand moderately sized images. Trying to expand
a full high definition screenshot is probably not going to work
because it will take a `VERY` long time or the program will run
out of memory.

---------------------------------------------------

End of README.md
