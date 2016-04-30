import ColorConverter
import Tuner

if __name__ == '__main__':
    
    color_deficit = 't'
    color_converter = ColorConverter.ColorConverter(color_deficit)
    tuner = Tuner.Tuner(color_converter)
    
    for x in xrange(1, 100000000):

        new_image = color_converter.convert()
        tuner.set_image(color_converter)


    tuner.destroy_windows()