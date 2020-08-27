from paz.pipelines import AugmentImage
from paz.abstract import SequentialProcessor
from paz.backend.image import show_image, load_image
import paz.processors as pr
from tensorflow.keras.preprocessing.image import ImageDataGenerator

augment = SequentialProcessor()
augment.add(pr.RandomContrast())
augment.add(pr.RandomBrightness())
augment.add(pr.RandomSaturation())

for _ in range(5):
    image = load_image('image.jpg')
    image = augment(image)
    show_image(image)


# Putting something new somewhere in this case in the first function (index 0).
augment.insert(0, pr.LoadImage())
for _ in range(5):
    image = augment('image.jpg')
    show_image(image)

# Adding new processor at the end to have a single function.
augment.add(pr.ShowImage())
for _ in range(5):
    image = augment('image.jpg')

# We can also pop the last processor added.
augment.pop()

# We now create another processor for geometric augmentation.
# Note: We can instantiate a new SequentialProcessor using a list of processors
transform = SequentialProcessor([pr.RandomRotation(), pr.RandomTranslation()])

# We can call both of our processors separately and sequentially:
for _ in range(5):
    image = transform(augment('image.jpg'))
    show_image(image)

# But since processors are just functions we can simply add it as a processor:
augment.add(transform)
for _ in range(5):
    image = augment('image.jpg')
    show_image(image)

# We can also use the Keras ImageDataGenerator
# We first instantiate a generator
generator = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True)

# We can add it by using our processor/wrapper ImageDataProcessor:
augment = SequentialProcessor()
augment.add(pr.LoadImage())
augment.add(pr.ImageDataProcessor(generator))
augment.add(pr.ShowImage())
for _ in range(5):
    image = augment('image.jpg')
