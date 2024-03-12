import argparse 
import os
import OCR 
import Linguist

def main():
    """
    Handles Command line arguments and begins the real time OCR by calling OCR_stream().A path to tesseract cmd root is required, but all other params are optional.
    Example Command-line use: python3 Main.py -t  python3 Main.py -t usr/local/Cellular/tesseract/4.1.1/bin/tesseract
    optional arguments:
    -h, --help          show this message help and exact
    -c, --crop          crop OCR area in pixels(two vals required): width height
    -v, --view_mode     view mode for OCR boxes displat
    -sv, --short_views  show the available view modes and description
    -l, --language      code for tesseract language, use + to add multiple(ex: chi_sim + chi_tra)
    -sl, --show_langs   show list of tesseract (4.0+) supported langs

    required named arguments:
    -t , --tess_path   path to the cmd root of tesseract install (see docs for further help)
    """
    parser = argparse.ArgumentParser()


    #Required
    requiredNamed = parser.add_argument_group('required named arguments')

    required.add_argument('-t','--tess_path',
                          help = 'path to the cmd root of the tesseract',
                          metavar='', required = True)

    #Optional
    
    parser.add_argument('-c','--crop',
                        help = 'crop OCR area in pixels',
                        nargs = 2, metavar = '', type = int)
    
    parser.add_argument('-v','--view', 
                        help = 'view mode for OCR boxes display',
                        deafault=1, type = int, metavar = '')
    
    parser.add_argument('-sv','--show_views',
                        help = 'show the available view modes',
                        action = 'store_true')
    
    parser.add_argument('-l','--language',
                        help = 'code for tesseract language',
                        metavar = '', default = None)
    
    parser.add_argument("-sl", "--show_langs", 
                        help="show list of tesseract (4.0+) supported langs",
                        action="store_true")

    parser.add_argument("-s", "--src", 
                         help="SRC video source for video capture",
                        default=0, type=int)

    args = parser.parse_args()

    if args.show_langs:
         Linguist.show_codes()

    if args.show_views:
        print(OCR.views.__doc__)

    tess_path = os.path.normpath(args.tesspath)

    #This is where OCR is started
    OCR.tesseract_location(tess_path)
    OCR.ocr_stream(view_mode = args.view_mode, source = args.src, crop = args.crop, language = args.language)

    if __name__ == '__main__':
        main()

        app.run(debug=True)

    # tess_path = '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract' 
    # view_mode = 1
    # source = 0
    # crop = [100, 100]
    # language = "en"
    # OCR.ocr_stream(view_mode=view_mode, source=source, crop=crop, language=language)




