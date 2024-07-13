# Advanced Video Stabilization without content loss

## Problem
Major consumer-wide video stabilization programs zoom/crop to readjust for the camera movement to get to a stable footage. But that results in loss of content and data.

## Our Solution
We work on each frame individually. We extract all the frames, and recompensate for the lost data while stabilization using outpainting, diffusion models and extrapolation.

## Feature given by mentor to implement
After stablizing a video with moviepy, vidgear there are black edges that represent lost data. Our task was to fill that sections on each frame. We solved it by using diffusion.

                                          INPUT VIDEO:
![INPUT VIDEO:](https://github.com/amBITion-24/byte_me/assets/108250604/9a509f4c-8e02-41a8-b636-f9ab68fdd7ba)

                            STABILISED VIDEO WITH PRIMITIVE STABILISATION:
![STABILISED VIDEO WITH PRIMITIVE STABILISATION:](https://github.com/amBITion-24/byte_me/assets/108250604/407a7146-91c5-4bb3-b47e-638a2f0401d7)


                                STABILISED VIDEO WITH FILLED EDGES:
![STABILISED VIDEO WITH FILLED EDGED:](https://github.com/amBITion-24/byte_me/assets/108250604/7e6f49a1-f500-4022-ae4b-ac9206df9d69)



## Additional Feature
FPS interpolation to increase frame rate to a defined rate.















