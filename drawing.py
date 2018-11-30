"""
This script contains all methods that do the drawing part
"""

def writeOnCluster(rovFile, objects, line):
    "This function write objects to their cluster on ROV.dot file"
    rovFile.write(line)

    for object in objects[:-1]:
        rovFile.write(object+",")
    rovFile.write(objects[-1]+";"+"\n")

def draw_relation(rovFile, object, to, noDuplicate):
    "This function draw an arrow between two objects"

    if not (to in noDuplicate[object]) and (to != object) :
        rovFile.write(object+" -> "+to+";\n")
        noDuplicate[object].append(to)


def draw_inheritance_relation(rovFile, object, to):
    rovFile.write(object+" -> "+to+";\n")

def draw_wrong_relation(rovFile, object, to, noDuplicate, num, message):
    "This function draw the wrong relation between two objects"
    print "\n WARNING:"
    print "\n",object, "is a Controller object, and in line", num, "it called", to, message
    if not (to in noDuplicate[object]):
        # draw the wrong relation with a dot line.
        rovFile.write(object+" -> "+to+"[style=dotted];\n")
        noDuplicate[object].append(to)
