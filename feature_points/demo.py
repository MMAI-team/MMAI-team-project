from sift_matcher import SiftMatcher

sift_matcher = SiftMatcher()

image_1_path = './research/data/2_1.jpg'
image_2_path = './research/data/2_3.jpg'

is_same = sift_matcher.predict(image_1_path, image_2_path)

if is_same:
    print('Same whale')
else:
    print('Different whale')
