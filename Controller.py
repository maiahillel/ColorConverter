import ColorConverter
import Tuner

class Controller(object):

    def main(self, color_deficit):
        color_converter = ColorConverter.ColorConverter(color_deficit)
        self.tuner = Tuner.Tuner(color_converter)
    
        for x in xrange(1, 100000000):

            self.tuner.set_image(color_converter)



    def kill(self):
        self.tuner.destroy_windows()
