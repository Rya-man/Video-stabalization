from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
from vidgear.gears.stabilizer import Stabilizer
import os


def stablize_full(input_video_path):
   
    dir_name=os.path.dirname(input_video_path)
    output_video_path =  os.path.join(dir_name,'vid.mp4')
    stream = VideoGear(source=input_video_path).start()
    stabilizer = Stabilizer(smoothing_radius=50, border_type='reflect')
    writer = WriteGear(output=output_video_path)

    while True:
        frame = stream.read()
        if frame is None:
            break


        stabilized_frame = stabilizer.stabilize(frame)


        writer.write(stabilized_frame)


    stream.stop()
    writer.close()

def stablize_normal(input_video_path):
   
    dir_name=os.path.dirname(input_video_path)
    output_video_path =  os.path.join(dir_name,'vid.mp4')
    stream = VideoGear(source=input_video_path).start()
    stabilizer = Stabilizer(smoothing_radius=100, border_type='red')
    writer = WriteGear(output=output_video_path)

    while True:
        frame = stream.read()
        if frame is None:
            break


        stabilized_frame = stabilizer.stabilize(frame)


        writer.write(stabilized_frame)


    stream.stop()
    writer.close()

#input_video_path = './sample.mp4'
#output = './sampleoutput5.mp4'