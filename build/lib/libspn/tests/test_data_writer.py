#!/usr/bin/env python3

# ------------------------------------------------------------------------
# Copyright (C) 2016-2017 Andrzej Pronobis - All Rights Reserved
#
# This file is part of LibSPN. Unauthorized use or copying of this file,
# via any medium is strictly prohibited. Proprietary and confidential.
# ------------------------------------------------------------------------

from context import libspn as spn
from test import TestCase
import os
import tensorflow as tf
import numpy as np


class TestDataWriter(TestCase):

    def test_csv_data_writer(self):
        # Write
        path = self.out_path(self.cid() + ".csv")
        writer = spn.CSVDataWriter(path)

        arr1 = np.array([1, 2, 3, 4])
        arr2 = np.array([[1 / 1, 1 / 2],
                         [1 / 3, 1 / 4],
                         [1 / 5, 1 / 6],
                         [1 / 7, 1 / 8]])
        writer.write(arr2, arr1)
        writer.write(arr2, arr1)

        # Read
        dataset = spn.CSVFileDataset(path,
                                     num_vals=[None] * 2,
                                     defaults=[[1], [1.0], [1.0]],
                                     num_epochs=1,
                                     batch_size=10,
                                     shuffle=False,
                                     num_labels=1,
                                     min_after_dequeue=1000,
                                     num_threads=1,
                                     allow_smaller_final_batch=True)
        data = dataset.read_all()

        # Compare
        np.testing.assert_array_almost_equal(np.concatenate((arr2, arr2)),
                                             data[0])
        np.testing.assert_array_equal(np.concatenate((arr1, arr1)),
                                      data[1].flatten())

    def test_csv_csv_writeall_singletensor(self):
        # Read&write
        dataset1 = spn.CSVFileDataset(self.data_path("data_int1.csv"),
                                      num_vals=[255] * 5,
                                      defaults=[[101], [102], [103], [104], [105]],
                                      num_epochs=2,
                                      batch_size=4,
                                      shuffle=False,
                                      num_labels=0,
                                      min_after_dequeue=1000,
                                      num_threads=1,
                                      allow_smaller_final_batch=True)
        path = self.out_path(self.cid() + ".csv")
        writer = spn.CSVDataWriter(path)
        data1 = dataset1.read_all()
        dataset1.write_all(writer)

        # Read again
        dataset2 = spn.CSVFileDataset(path,
                                      num_vals=[255] * 5,
                                      defaults=[[201], [202], [203], [204], [205]],
                                      num_epochs=1,
                                      batch_size=4,
                                      shuffle=False,
                                      num_labels=0,
                                      min_after_dequeue=1000,
                                      num_threads=1,
                                      allow_smaller_final_batch=True)
        data2 = dataset2.read_all()

        # Compare
        np.testing.assert_array_equal(data1, data2)

    def test_csv_csv_writeall_tensorlist(self):
        # Read&write
        dataset1 = spn.CSVFileDataset(self.data_path("data_int1.csv"),
                                      num_vals=[None] * 3,
                                      defaults=[[101], [102], [103.0],
                                                [104.0], [105.0]],
                                      num_epochs=2,
                                      batch_size=4,
                                      shuffle=False,
                                      num_labels=2,
                                      min_after_dequeue=1000,
                                      num_threads=1,
                                      allow_smaller_final_batch=True)
        path = self.out_path(self.cid() + ".csv")
        writer = spn.CSVDataWriter(path)
        data1 = dataset1.read_all()
        dataset1.write_all(writer)

        # Read again
        dataset2 = spn.CSVFileDataset(path,
                                      num_vals=[None] * 3,
                                      defaults=[[201], [202], [203.0],
                                                [204.0], [205.0]],
                                      num_epochs=1,
                                      batch_size=4,
                                      shuffle=False,
                                      num_labels=2,
                                      min_after_dequeue=1000,
                                      num_threads=1,
                                      allow_smaller_final_batch=True)
        data2 = dataset2.read_all()

        # Compare
        np.testing.assert_array_almost_equal(data1[0], data2[0])
        np.testing.assert_array_equal(data1[1], data2[1])

    def test_image_gray_float_image_gray_writeall(self):
        # Read and write
        dataset1 = spn.ImageDataset(
            image_files=self.data_path("img_dir1/*-{*}.png"),
            format=spn.ImageFormat.FLOAT,
            num_epochs=1, batch_size=2, shuffle=False,
            ratio=1, crop=0, accurate=True,
            allow_smaller_final_batch=True)
        writer = spn.ImageDataWriter(
            path=self.out_path(self.cid(), "img%n-%l.png"),
            shape=dataset1.shape,
            normalize=False,
            num_digits=1)

        os.makedirs(self.out_path(self.cid()), exist_ok=True)
        data1 = dataset1.read_all()
        dataset1.write_all(writer)

        # Re-read
        dataset2 = spn.ImageDataset(
            image_files=self.out_path(self.cid(), "*-{*}.png"),
            format=spn.ImageFormat.FLOAT,
            num_epochs=1, batch_size=2, shuffle=False,
            ratio=1, crop=0, accurate=True,
            allow_smaller_final_batch=True)
        data2 = dataset2.read_all()

        # Compare
        np.testing.assert_allclose(data1[0], data2[0])
        np.testing.assert_array_equal(data1[1], data2[1])

    def test_image_rgb_rgbfloat_image_rgb_writeall(self):
        # Read and write
        dataset1 = spn.ImageDataset(
            image_files=self.data_path("img_dir2/*-{*}.png"),
            format=spn.ImageFormat.RGB_FLOAT,
            num_epochs=1, batch_size=2, shuffle=False,
            ratio=1, crop=0, accurate=True,
            allow_smaller_final_batch=True)
        writer = spn.ImageDataWriter(
            path=self.out_path(self.cid(), "img%n-%l.png"),
            shape=dataset1.shape,
            normalize=False,
            num_digits=1)

        os.makedirs(self.out_path(self.cid()), exist_ok=True)
        data1 = dataset1.read_all()
        dataset1.write_all(writer)

        # Re-read
        dataset2 = spn.ImageDataset(
            image_files=self.out_path(self.cid(), "*-{*}.png"),
            format=spn.ImageFormat.RGB_FLOAT,
            num_epochs=1, batch_size=2, shuffle=False,
            ratio=1, crop=0, accurate=True,
            allow_smaller_final_batch=True)
        data2 = dataset2.read_all()

        # Compare
        np.testing.assert_allclose(data1[0], data2[0], atol=0.002)
        np.testing.assert_array_equal(data1[1], data2[1])

    def test_image_gray_int_image_gray_writeall(self):
        # Read and write
        dataset1 = spn.ImageDataset(
            image_files=self.data_path("img_dir1/*-{*}.png"),
            format=spn.ImageFormat.INT,
            num_epochs=1, batch_size=2, shuffle=False,
            ratio=1, crop=0, accurate=True,
            allow_smaller_final_batch=True)
        writer = spn.ImageDataWriter(
            path=self.out_path(self.cid(), "img%n-%l.png"),
            shape=dataset1.shape,
            normalize=False,
            num_digits=1)

        os.makedirs(self.out_path(self.cid()), exist_ok=True)
        data1 = dataset1.read_all()
        dataset1.write_all(writer)

        # Re-read
        dataset2 = spn.ImageDataset(
            image_files=self.out_path(self.cid(), "*-{*}.png"),
            format=spn.ImageFormat.INT,
            num_epochs=1, batch_size=2, shuffle=False,
            ratio=1, crop=0, accurate=True,
            allow_smaller_final_batch=True)
        data2 = dataset2.read_all()

        # Compare
        np.testing.assert_array_equal(data1[0], data2[0])
        np.testing.assert_array_equal(data1[1], data2[1])

    def test_image_rgb_rgbint_image_rgb_writeall(self):
        # Read and write
        dataset1 = spn.ImageDataset(
            image_files=self.data_path("img_dir2/*-{*}.png"),
            format=spn.ImageFormat.RGB_INT,
            num_epochs=1, batch_size=2, shuffle=False,
            ratio=1, crop=0, accurate=True,
            allow_smaller_final_batch=True)
        writer = spn.ImageDataWriter(
            path=self.out_path(self.cid(), "img%n-%l.png"),
            shape=dataset1.shape,
            normalize=False,
            num_digits=1)

        os.makedirs(self.out_path(self.cid()), exist_ok=True)
        data1 = dataset1.read_all()
        dataset1.write_all(writer)

        # Re-read
        dataset2 = spn.ImageDataset(
            image_files=self.out_path(self.cid(), "*-{*}.png"),
            format=spn.ImageFormat.RGB_INT,
            num_epochs=1, batch_size=2, shuffle=False,
            ratio=1, crop=0, accurate=True,
            allow_smaller_final_batch=True)
        data2 = dataset2.read_all()

        # Compare
        np.testing.assert_array_equal(data1[0], data2[0])
        np.testing.assert_array_equal(data1[1], data2[1])

    def test_image_gray_float_csv_writeall(self):
        # Read and write
        dataset1 = spn.ImageDataset(
            image_files=self.data_path("img_dir1/*-{*}.png"),
            format=spn.ImageFormat.FLOAT,
            num_epochs=1, batch_size=2, shuffle=False,
            ratio=1, crop=0, accurate=True,
            allow_smaller_final_batch=True)
        writer = spn.CSVDataWriter(
            path=self.out_path(self.cid() + ".csv"))

        data1 = dataset1.read_all()
        dataset1.write_all(writer)

        # Re-read
        dataset2 = spn.CSVFileDataset(
            files=self.out_path(self.cid() + ".csv"),
            num_vals=[None] * 25,
            defaults=[[b'']] + [[1.0] for _ in range(25)],
            num_epochs=1,
            batch_size=2,
            shuffle=False,
            num_labels=1,
            allow_smaller_final_batch=True)
        data2 = dataset2.read_all()

        # Compare
        np.testing.assert_allclose(data1[0], data2[0])
        np.testing.assert_array_equal(data1[1], data2[1])


if __name__ == '__main__':
    tf.test.main()
