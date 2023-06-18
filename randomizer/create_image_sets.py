from django.core.management.base import BaseCommand
from randomizer.models import ImageSet
import os


class Command(BaseCommand):
    help = 'Loads image sets into the database'

    def handle(self, *args, **options):
        image_sets = [
            {'name': 'Imageset1', 'image': '1.jpg', 'color1': '#6a3a21', 'color2': '#a34f1f', 'color3': '#2e1507', 'color4': '#ffd4b8','color5': '#dd5410','color6': '#2e1507','color7': '#e3926a'},
            {'name': 'Mountain', 'image': 'mountain.jpg', 'color1': '#2b580c', 'color2': '#c2d91f'},
            {'name': 'City', 'image': 'city.jpg', 'color1': '#8d1010', 'color2': '#30486f'},
            {'name': 'Forest', 'image': 'forest.jpg', 'color1': '#5f2c0e', 'color2': '#95c11f'},
        ]

        for image_set in image_sets:
            image_path = os.path.join('images', 'image_sets', image_set['image'])
            ImageSet.objects.create(name=image_set['name'], image=image_path, color1=image_set['color1'], color2=image_set['color2'])

        self.stdout.write(self.style.SUCCESS('Successfully loaded image sets.'))


from randomizer.models import ImageSet

# Create ImageSet 1
image_path = 'images/image_sets/1.jpg'
color1 = '#6a3a21'
color2 = '#a34f1f'
color3 = '#2e1507'
color4 = '#ffd4b8'
color5 = '#dd5410'
color6 = '#2e1507'
color7 = '#e3926a'
name = 'Imageset1'
ImageSet.objects.create(image=image_path, color1=color1, color2=color2, color3=color3, color4=color4, color5=color5, color6=color6, color7=color7, name=name)

# Create ImageSet 2
image_path = 'images/image_sets/2.jpg'
color1 = '#267493'
color2 = '#2e9386'
color3 = '#07232f'
color4 = '#ccfffc'
color5 = '#0fb6ee'
color6 = '#07232f'
color7 = '#5bece9'
name = 'Imageset2'
ImageSet.objects.create(image=image_path, color1=color1, color2=color2, color3=color3, color4=color4, color5=color5, color6=color6, color7=color7, name=name)

# Create ImageSet 3
image_path = 'images/image_sets/3.jpg'
color1 = '#2f53a2'
color2 = '#c97f29'
color3 = '#221803'
color4 = '#d1e3ff'
color5 = '#62c5ff'
color6 = '#240a04'
color7 = '#ffc343'
name = 'Imageset3'
ImageSet.objects.create(image=image_path, color1=color1, color2=color2, color3=color3, color4=color4, color5=color5, color6=color6, color7=color7, name=name)

# Create ImageSet 4
image_path = 'images/image_sets/4.jpg'
color1 = '#62282b'
color2 = '#b96451'
color3 = '#240a04'
color4 = '#ffcbc2'
color5 = '#171618'
color6 = '#ffffff'
color7 = '#f8876e'
name = 'Imageset4'
ImageSet.objects.create(image=image_path, color1=color1, color2=color2, color3=color3, color4=color4, color5=color5, color6=color6, color7=color7, name=name)

# Create ImageSet 5
image_path = 'images/image_sets/5.jpg'
color1 = '#393740'
color2 = '#767285'
color3 = '#171618'
color4 = '#f3ecff'
color5 = '#2cff92'
color6 = '#171618'
color7 = '#ece6f1'
name = 'Imageset5'
ImageSet.objects.create(image=image_path, color1=color1, color2=color2, color3=color3, color4=color4, color5=color5, color6=color6, color7=color7, name=name)

# Create ImageSet 6
image_path = 'images/image_sets/6.jpg'
color1 = '#165452'
color2 = '#853939'
color3 = '#05160e'
color4 = '#c7ffe2'
color5 = '#ebbb2e'
color6 = '#05160e'
color7 = '#1fad90'
name = 'Imageset6'
ImageSet.objects.create(image=image_path, color1=color1, color2=color2, color3=color3, color4=color4, color5=color5, color6=color6, color7=color7, name=name)

# Create ImageSet 7
image_path = 'images/image_sets/7.jpg'
color1 = '#695213'
color2 = '#a5801b'
color3 = '#1e1604'
color4 = '#fff5c3'
color5 = '#603eda'
color6 = '#1e1604'
color7 = '#f6f03d'
name = 'Imageset7'
ImageSet.objects.create(image=image_path, color1=color1, color2=color2, color3=color3, color4=color4, color5=color5, color6=color6, color7=color7, name=name)

# Create ImageSet 8
image_path = 'images/image_sets/8.jpg'
color1 = '#463c6b'
color2 = '#752e2e'
color3 = '#150c26'
color4 = '#e8d4ff'
color5 = '#aae505'
color6 = '#150c26'
color7 = '#7d78e0'
name = 'Imageset8'
ImageSet.objects.create(image=image_path, color1=color1, color2=color2, color3=color3, color4=color4, color5=color5, color6=color6, color7=color7, name=name)

# Create ImageSet 9
image_path = 'images/image_sets/9.jpg'
color1 = '#a0681a'
color2 = '#537412'
color3 = '#151e04'
color4 = '#ffeacc'
color5 = '#9ae505'
color6 = '#151e04'
color7 = '#f6f03d'
name = 'Imageset9'
ImageSet.objects.create(image=image_path, color1=color1, color2=color2, color3=color3, color4=color4, color5=color5, color6=color6, color7=color7, name=name)
