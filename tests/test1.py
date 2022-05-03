from nst import make_style_transfer
import timeit
from threading import Thread


def test_passing():
    assert (1, 2, 3) == (1, 2, 3)


def test_nst_threads_test():
    start = timeit.timeit()
    # make_style_transfer(content_image_path='../pics_for_test_NST/content.jpg', style_image_path='../pics_for_test_NST/style.png', content_blending_ratio=0.01, path_save_final_img='../pics_for_test_NST/final_img.jpg')

    thread1 = Thread(target=make_style_transfer, args=('../pics_for_test_NST/content.jpg', '../pics_for_test_NST/style.png', 0.01, '../pics_for_test_NST/final_img1.jpg'))
    thread2 = Thread(target=make_style_transfer, args=('../pics_for_test_NST/content2.png', '../pics_for_test_NST/style2.jpg', 0.01, '../pics_for_test_NST/final_img2.jpg'))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    end = timeit.timeit()
    print(f'time: {end - start}')

