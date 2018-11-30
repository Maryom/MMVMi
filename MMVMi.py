#!/usr/bin/env python

import os
import re
import sys
import drawing as draw
from termcolor import colored
from terminaltables import SingleTable


def check_relations(filename, extLen, noDuplicate, rovFile, objects, current_list, path):
    "This function check relations between clusters"

    noDuplicate[filename[:-extLen]] = []
    with open(os.path.join(path, filename),'r') as f:
        scan(rovFile, f, filename[:-extLen], objects, current_list, noDuplicate)

def scan(rovFile, file, filename, objects, cluster_objects, noDuplicate):

    # This pattern check inheritance relations between objects in the same cluster
    inheritance_pattern = re.compile(filename+": \\b(?=(" + "|".join(map(re.escape, cluster_objects)) + ")\\b {)")

    for num, line in enumerate(file, 1):
        for object in objects:
            # No warning message
            if objects[object] == "" :
                for match in re.finditer(object, line):
                    draw.draw_relation(rovFile, filename, match.group(1), noDuplicate)
            else:
                for match in re.finditer(object, line):
                    draw.draw_wrong_relation(rovFile, filename, match.group(1), noDuplicate, num, objects[object])


def main():

    print colored('Welcome to MVC & MVVM Validation Model for iOS (MMVMi)', 'cyan')
    print colored('Phase one Massive Controller detector (MCD): ', 'cyan')

    controllers =['UIViewController', 'UITabBarController', 'UITableViewController', 'UICollectionViewController', 'UIActivityViewController', 'UICloudSharingController', 'UIDocumentInteractionController', 'UIDocumentMenuViewController', 'UIDocumentPickerViewController', 'UIDocumentPickerExtensionViewController', 'UIImagePickerController', 'UIInputViewController', 'UINavigationController', 'UIPageControl', 'UIPageViewController', 'UIPopoverController', 'UIPopoverPresentationController', 'UIPresentationController', 'UIPrinterPickerController', 'UIPrintInteractionController', 'UIReferenceLibraryViewController', 'UIRefreshControl', 'UISearchContainerViewController', 'UISearchController', 'UISearchDisplayController', 'UISplitViewController', 'GLKViewController', 'AVPlayerViewController']

    views = ['UIView', 'UICollectionView', 'UICollectionReusableView', 'UITableView', 'UICollectionViewCell', 'UITableViewCell', 'UILabel', 'UIActivityIndicatorView', 'UIButton', 'UIProgressView', 'UIStackView', 'UIImageView', 'UITextView', 'UIScrollView', 'UIPickerView', 'UIVisualEffectView', 'MKMapView', 'MTKView', 'GLKView', 'ARSCNView', 'WKWebView', 'UINavigationBar', 'UIToolbar', 'UITabBar', 'UISearchBar', 'UIContainerView']

    extension = ".swift"
    extLen = len(extension)

    anotherCheck = []
    allControllers = []
    controllers_list = []
    view_list = []

    path  = raw_input(colored("Please enter your project path: ", 'white'))

    # replace the white space at the end of the project path with '/'
    project_path = path.replace(' ', '/')

    controller_pattern = re.compile("class .*: (?=(" + "|".join(map(re.escape, controllers)) + "))")

    view_pattern = re.compile("class .*: \\b(?=(" + "|".join(map(re.escape, views)) + ")\\b)")

    for path, subdirs, files in os.walk(project_path):
       for filename in files:
           if filename[len(filename)-extLen:] == '.swift' :
               # open the file to read it
               current_file = open(os.path.join(path, filename))

               for line in current_file:
                   for match in re.finditer(view_pattern, line):
                       view_list.append(filename[:-extLen])

                   for match in re.finditer(controller_pattern, line):
                       # count # of lines for each controller object
                       num_lines = sum(1 for theLine in open(os.path.join(path, filename)) if theLine.split() and not '//' in theLine)

                       controllers_list.append(filename[:-extLen])
                       allControllers.append((filename[:-extLen], num_lines))

               if not(filename[:-extLen] in controllers_list or filename[:-extLen] in view_list):
                   anotherCheck.append((filename[:-extLen], os.path.join(path, filename)))


    # another check is needed to check if a class is a subclass of controller classes
    project_controllers = re.compile("class .*: \\b(?=(" + "|".join(map(re.escape, controllers_list)) + ")\\b)")

    for theFile, thePath in anotherCheck:
        currentFile = open(thePath)

        for line in currentFile:
            for match in re.finditer(project_controllers, line):

                num_linesy = sum(1 for theLiney in open(thePath) if theLiney.split() and not '//' in theLiney)
                allControllers.append((theFile, num_linesy))
                controllers_list.append(theFile)

    total_controllers = len(allControllers)

    print colored('\nThis project has', 'white'), colored('%d', 'magenta') % total_controllers, colored('controllers. \n', 'white')

    sorted_controllers = sorted(allControllers, key=lambda x: x[1], reverse=True)


    TABLE_DATA = (
        ('\nController Name', '\nTotal number of lines', '\nController status'),
    )

    for controller_name, lines in sorted_controllers:
        if lines > 300:
            TABLE_DATA += (controller_name, lines, "Massive Controller"),
        elif lines < 150:
            TABLE_DATA += (controller_name, lines, "Thin Controller"),
        elif lines >= 150 or lines <= 300 :
            TABLE_DATA += (controller_name, lines, "Take care"),


    title = 'Massive Controller Detection'

    # SingleTable.
    table_instance = SingleTable(TABLE_DATA, title)
    table_instance.justify_columns[2] = 'left'
    print(table_instance.table)

    print colored('Welcome to phase two: Object Relations Validation (ORV)', 'cyan')

    model_objects = raw_input(colored("Please enter your Model files name: ", 'cyan'))
    model_list = model_objects.split() # splits the input string on spaces

    modelView_objects = raw_input(colored("Please enter your Model View files name: ", 'cyan'))
    modelView_list = modelView_objects.split() # splits the input string on spaces

    rovFile = open("ROV.dot", "w")

    modelsPattern = re.compile("[^\"]\\b(?=(" + "|".join(map(re.escape, model_list)) + ")\\b)")
    modelViewPattern = re.compile("[^\"]\\b(?=(" + "|".join(map(re.escape, modelView_list)) + ")\\b)")
    controllersPattern = re.compile("[^\"]\\b(?=(" + "|".join(map(re.escape, controllers_list)) + ")\\b)")
    viewsPattern = re.compile("[^\"]\\b(?=(" + "|".join(map(re.escape, view_list)) + ")\\b)")

    noDuplicate = {}

    with open('ROVtemplate.dot','r') as f:
        for line in f:
            if "Controller" in line:
                draw.writeOnCluster(rovFile, controllers_list, line)

            elif "label = \"View Model\"" in line:
                draw.writeOnCluster(rovFile, modelView_list, line)

            elif "label = \"View\"" in line:
                draw.writeOnCluster(rovFile, view_list, line)

            elif "label = \"Model\"" in line:
                draw.writeOnCluster(rovFile, model_list, line)

            else:
                rovFile.write(line)

        for path, subdirs, files in os.walk(project_path):
           for filename in files:
               # check all the relations between modelView objects and other objects
               if filename[:-extLen] in modelView_list:
                   modelView_objects = { modelsPattern: "", controllersPattern: "", viewsPattern: "which is a view object. Please fix this forbidden relation. \n" }
                   check_relations(filename, extLen, noDuplicate, rovFile, modelView_objects, modelView_list, path)

               # check all the relations between model objects and other objects
               if filename[:-extLen] in model_list:
                   model_objects = { modelViewPattern: "", controllersPattern: "which is a controller object. Please fix this forbidden relation. \n", viewsPattern: "which is a view object. Please fix this forbidden relation. \n" }
                   check_relations(filename, extLen, noDuplicate, rovFile, model_objects, model_list, path)

               # check all the relations between controllers objects and other objects
               if filename[:-extLen] in controllers_list:
                   controller_objects = { modelsPattern: "which is a model object. Please fix this forbidden relation. \n", modelViewPattern: "", viewsPattern: "" }
                   check_relations(filename, extLen, noDuplicate, rovFile, controller_objects, controllers_list, path)

               # check all the relations between view objects and other objects
               if filename[:-extLen] in view_list:
                   view_objects = { modelsPattern: "which is a model object. Please fix this forbidden relation. \n", modelViewPattern: "", controllersPattern: "" }
                   check_relations(filename, extLen, noDuplicate, rovFile, view_objects, view_list, path)

    rovFile.write("}")

    f.close()
    rovFile.close()

if __name__ == "__main__":
    main()
