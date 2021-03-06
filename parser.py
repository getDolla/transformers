from display import *
from matrix import *
from draw import *

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single word that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix -
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix -
	 scale: create a scale matrix,
	    then multiply the transform matrix by the scale matrix -
	    takes 3 arguments (sx, sy, sz)
	 move: create a translation matrix,
	    then multiply the transform matrix by the translation matrix -
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
	 apply: apply the current transformation matrix to the
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""
def parse_file( fname, points, transform, screen, color ):
    two_line_fxns = [ "line", "scale", "move", "rotate", "save" ]
    one_line_fxns = [ "display", "apply", "ident" ]
    f = open(fname, 'r').readlines()

    i = 0
    while (i < len(f)):
        info_line = f[i].strip()

        if (info_line in two_line_fxns):
            i += 1
            function = info_line
            args = f[i].strip().split(" ")
            helper( function, args, points, transform, screen, color )

        elif (info_line in one_line_fxns):
            if (info_line == "display"):
                clear_screen( screen )
                draw_lines( points, screen, color)
                display(screen)
            elif (info_line == "apply"):
                matrix_mult( transform, points )
            else:
                ident(transform)

        elif (info_line == "quit"):
            return

        i += 1

def helper( function, args, points, transform, screen, color ):
    if (function == "line"):
        args = [int(x) for x in args]
        add_edge( points, args[0], args[1], args[2], args[3], args[4], args[5] )

    elif (function == "scale"):
        args = [int(x) for x in args]
        m = make_scale(args[0], args[1], args[2])
        matrix_mult( m, transform)

    elif (function == "move"):
        args = [int(x) for x in args]
        m = make_translate( args[0], args[1], args[2] )
        matrix_mult( m, transform)

    elif (function == "rotate"):
        if args[0].lower() == "x":
            m = make_rotX( int(args[1]) )
        elif args[0].lower() == "y":
            m = make_rotY( int(args[1]) )
        else:
            m = make_rotZ( int(args[1]) )
        matrix_mult( m, transform)

    elif (function == "save"):
	clear_screen( screen )
        draw_lines( points, screen, color)
        save_extension(screen, args[0])
