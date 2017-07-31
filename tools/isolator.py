import tensorflow as tf
import numpy as np
from shutil import copyfile
import argparse
import os
import json
import glob
import random
import collections
import math
import time



def load_paths_and_attributes(a, top_how_many):


    with open(os.path.join(a.input_dir, 'Anno/list_attr_img.txt'), 'rb') as attributes_file:

        def get_lines(a):
            for l in a:
                yield l

        line_gen = get_lines(attributes_file)

        paths = []

        attributes = np.zeros([a.input_size, 1000], dtype=np.int8)

        index = 0

        for line in line_gen:

            # print(index)

            line = line.strip().split()

            if index > 1:
                path = str(line[0])
                path = path.strip().split('/')
                path[2] = path[2].split('.')[0]
                path = path[1] + '-' + path[2] + '.png'
                path = os.path.join(a.input_dir, path)
                attr = np.array(line[1:1001], dtype=np.int8)

                paths.append(path)
                attributes[index - 2] = attr

            index += 1

        attributes = np.array(attributes, dtype=np.int8)
        attributes += 1
        attributes //= 2

        image_count = np.zeros([1000, 2])

        for i in range(1000):
            image_count[i][0] = i


        # for i in range(a.input_size):
        #     print("loop2 " + str(i))
        #     for j in range(1000):
        #         if attributes[i][j] == 1:
        #             image_count[j][1] += 1
        #
        # image_count_sorted = sorted(image_count, key=(lambda x: x[1]), reverse=True)
        #
        # print(image_count_sorted)

        image_count = np.sum(attributes, axis=0).reshape(1000, 1)
        indices = np.array(list(range(1000))).reshape(1000, 1)

        image_count = np.append(indices, image_count, axis=1)
        image_count_sorted = np.array(sorted(image_count, key=(lambda x: x[1]), reverse=True))

        top_attributes = [x[0] for x in image_count_sorted[0:top_how_many]]
        all_attr = list(range(1000))
        attributes_to_del = [x for x in all_attr if x not in top_attributes]
        attributes = np.delete(attributes, attributes_to_del, axis=1)

    with open(os.path.join(a.input_dir, 'Anno/list_attr_cloth.txt'), 'rb') as attributes_list:

        k = 0

        attribute_names = []

        for line in attributes_list:

            k+=1

            if k < 3:
                continue

            print(k)

            line = line.strip().split()
            line = [a.decode('utf-8') for a in line]

            attribute_names.append(' '.join(line[:-1]))


        print(attribute_names)

        print([(x, attribute_names[x]) for x in top_attributes])
        attributes = tf.constant(attributes)

        def gen_samples():

            if not os.path.exists('/home/sam/Desktop/samples_for_attributes'):
                os.makedirs('/home/sam/Desktop/samples_for_attributes')

            for j in range(top_how_many):

                count = 0

                for k in range(attributes.shape[0]):

                        print(k)

                        if count == 100:
                            break

                        if attributes[k][top_attributes[j]]:

                            dest_path = os.path.join('/home/sam/Desktop/samples_for_attributes', attribute_names[j])

                            if not os.path.exists(dest_path):
                                os.makedirs(dest_path)

                            copyfile(os.path.join(a.input_dir, paths[k]), dest_path)

                            count += 1


        return paths, attributes


class Tub:
    def __init__(self):
        self.input_dir = '/home/sam/Desktop/gan/fashion_clothing_and_category'
        self.input_size = 289222

a = Tub()


load_paths_and_attributes(a, 50)

