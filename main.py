def main():
    
    color_deficit = 'd'

    color_converter = ColorConverter(color_deficit)
    tuner = Tuner(color_converter)
    
    for x in xrange(1, 100000000):

        new_image = color_converter.convert()
        tuner.set_image(new_image)

    tuner.destroy_windows()