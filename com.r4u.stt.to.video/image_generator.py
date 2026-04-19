from PIL import Image, ImageDraw, ImageFont
import os

class ImageGenerator:
    def __init__(self, output_dir='generated_images', width=1280, height=720):
        self.output_dir = output_dir
        self.width = width
        self.height = height
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def create_text_image(self, text, image_name='image.png', bg_color=(255, 255, 255), 
                         text_color=(0, 0, 0), font_size=60):
        """
        Create an image with text overlay
        """
        # Create blank image
        img = Image.new('RGB', (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position (center)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        # Draw text
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Save image
        image_path = os.path.join(self.output_dir, image_name)
        img.save(image_path)
        
        return image_path

    def create_gradient_image(self, text, image_name='gradient.png', color1=(0, 0, 255), 
                             color2=(255, 0, 0), text_color=(255, 255, 255), font_size=60):
        """
        Create an image with gradient background and text
        """
        img = Image.new('RGB', (self.width, self.height))
        
        # Create gradient
        for y in range(self.height):
            r = int(color1[0] + (color2[0] - color1[0]) * y / self.height)
            g = int(color1[1] + (color2[1] - color1[1]) * y / self.height)
            b = int(color1[2] + (color2[2] - color1[2]) * y / self.height)
            for x in range(self.width):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        # Draw text with outline
        outline_width = 2
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill=(0, 0, 0))
        
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Save image
        image_path = os.path.join(self.output_dir, image_name)
        img.save(image_path)
        
        return image_path

if __name__ == '__main__':
    gen = ImageGenerator()
    gen.create_text_image('Hello World', 'text_image.png')
    gen.create_gradient_image('Learning Video', 'gradient_image.png')