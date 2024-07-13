from PIL import Image
import os

#function to extend frame
def extend_frame(image_path, factor):

    im = Image.open(image_path)#opening image
    
    #resizing image
    (original_width, original_height) = im.size
    new_width = int(original_width * factor)
    new_height = int(original_height * factor)
    
    new_im = Image.new("RGB", (new_width, new_height))
    
    x_offset = (new_width - original_width) // 2
    y_offset = (new_height - original_height) // 2
    
    #creating new image witth empty space
    new_im.paste(im, (x_offset, y_offset))
    #new_im.show()
    
    #felling empty space
    if y_offset > 0:
        top_edge_color = im.crop((0, 0, original_width, 1)).resize((new_width, y_offset))
        bottom_edge_color = im.crop((0, original_height - 1, original_width, original_height)).resize((new_width, new_height - y_offset - original_height))
        new_im.paste(top_edge_color, (0, 0))
        new_im.paste(bottom_edge_color, (0, y_offset + original_height))
    
    if x_offset > 0:
        left_edge_color = im.crop((0, 0, 1, original_height)).resize((x_offset, new_height))
        right_edge_color = im.crop((original_width - 1, 0, original_width, original_height)).resize((new_width - x_offset - original_width, new_height))
        new_im.paste(left_edge_color, (0, 0))
        new_im.paste(right_edge_color, (x_offset + original_width, 0))
    
    return new_im

#extended_image = extend_frame("test_images/highest_room.jpg", 1.2)
#extended_image.show()


def extend_frames(source_path):

    dir_name=os.path.dirname(source_path)
    destination_path =  os.path.join(dir_name,'frames_extended')
    os.makedirs(destination_path, exist_ok=True)

    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    for filename in os.listdir(source_path):
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            file_path = os.path.join(source_path, filename)
            extended_image = extend_frame(file_path, 1.1)
            save_path=os.path.join(destination_path, filename)
            extended_image.save(save_path)
    return destination_path

            
if __name__ == "__main__":            
    source_path = r""
    extend_frames(source_path)


