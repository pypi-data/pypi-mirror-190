# Library Created By Webraft on 9/2/22
import csv


def create_model(name):
    global model_name
    model_name = name


def importerror(filename):
    pass


def nameerror(name):
    global model_name
    if model_name == name:
        return
    else:
        print("Error 1: Model Not Found")
        exit()


def dataset(filepath, input, label, model):
    global model_name
    nameerror(model)
    filename = open(filepath, 'r')
    file = csv.DictReader(filename)
    global words_list1
    global words_list2
    words_list1 = []
    words_list2 = []
    # creating dictreader object
    for col in file:
        words_list1.append(col[input])
        words_list2.append(col[label])


def add_data(model, input, label):
    global words_list1
    global words_list2
    nameerror(model)
    words_list1.append(input)
    words_list2.append(label)


def model_run(word, model):
    global words_list1
    global words_list2
    nameerror(model)

    closest_index = -1
    closest_distance = float("inf")
    for i, w in enumerate(words_list1):
        distance = abs(len(word) - len(w))
        if distance < closest_distance:
            closest_index = i
            closest_distance = distance

    return words_list2[closest_index]


def model_load(input, model):
    global words_list1
    global words_list2
    global model_name

    nameerror(model)
    model_run(input, words_list1, words_list2)



